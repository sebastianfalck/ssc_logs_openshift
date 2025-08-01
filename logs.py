import sys
import re
import os

def sanitize_line(line, sensitive_words):
    if '=' in line:
        key, value = line.split('=', 1)
        for word in sensitive_words:
            if re.search(re.escape(word), key, re.IGNORECASE):
                return f"{key}=******"
        return f"{key}={value}"
    return line

def log_to_html(input_path, html_path, microservice, ambiente, tipo, sensitive_words=None):
    with open(input_path, 'r') as f:
        lines = f.readlines()

    should_sanitize = tipo.lower() in ['secrets', 'configmaps', 'env'] and ambiente.lower() != 'dev'

    with open(html_path, 'w') as html:
        html.write(f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Reporte de {tipo.upper()} - {microservice}</title>
    <style>
        body {{
            font-family: 'Segoe UI', sans-serif;
            background-color: #f4f4f4;
            padding: 30px;
            color: #333;
        }}
        .card {{
            background: #ffffff;
            border-radius: 10px;
            padding: 25px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            background-color: #00a79d;
            color: white;
            padding: 15px;
            border-radius: 8px 8px 0 0;
            margin-top: 0;
            text-align: center;
        }}
        .log-title {{
            font-size: 1.2em;
            margin: 20px 0 10px;
            color: #00a79d;
            border-bottom: 2px solid #00a79d;
            padding-bottom: 5px;
        }}
        .error {{ color: #cc0000; font-weight: bold; }}
        .warning {{ color: #ff8800; }}
        .info {{ color: #006699; }}
        .normal {{ color: #333; }}
        .section {{ margin-top: 15px; font-weight: bold; color: #00a79d; }}
        .line {{ white-space: pre-wrap; margin: 2px 0; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }}
        th {{
            background-color: #00a79d;
            color: white;
        }}
        .yaml {{
            background-color: #f9f9f9;
            border-left: 4px solid #00a79d;
            padding: 10px;
            margin: 10px 0;
            font-family: monospace;
            white-space: pre-wrap;
        }}
    </style>
</head>
<body>
<div class="card">
    <h1>Reporte de {tipo.upper()} de {microservice} en {ambiente.upper()}</h1>
""")

        tipo = tipo.lower()

        if tipo == 'logs':
            html.write('<div class="log-title">📋 Logs de aplicación</div>')
            for line in lines:
                esc = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                if 'ERROR' in line:
                    html.write(f'<div class="line error">❌ {esc}</div>\n')
                elif 'WARNING' in line:
                    html.write(f'<div class="line warning">⚠️ {esc}</div>\n')
                elif 'INFO' in line:
                    html.write(f'<div class="line info">ℹ️ {esc}</div>\n')
                else:
                    html.write(f'<div class="line normal">• {esc}</div>\n')

        elif tipo == 'describe':
            html.write('<div class="log-title">🔍 Detalle del Pod</div>')
            for line in lines:
                esc = line.strip()
                if not esc:
                    continue
                if not line.startswith(" "):
                    html.write(f'<div class="section">📌 {esc}</div>\n')
                else:
                    html.write(f'<div class="line normal">{esc}</div>\n')

        elif tipo in ['secrets', 'configmaps', 'env']:
            label = {
                'secrets': '🔐 Secrets',
                'configmaps': '🧾 ConfigMaps',
                'env': '🌱 Variables de entorno (.env)'
            }[tipo]
            html.write(f'<div class="log-title">{label}</div>\n')
            for line in lines:
                esc = line.strip()
                if sensitive_words and should_sanitize:
                    esc = sanitize_line(esc, sensitive_words)
                if '=' in esc:
                    key, value = esc.split('=', 1)
                    key = key.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                    value = value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                    html.write(f'<div class="section">🔑 {key}</div>\n')
                    html.write(f'<div class="line normal">{value}</div>\n')

        elif tipo == 'deployment':
            html.write('<div class="log-title">📦 Detalles del Deployment</div>\n')

            metadata = {}
            spec = {}
            containers = []
            current_container = {}
            current_path = []

            for line in lines:
                raw = line.rstrip()
                indent = len(line) - len(line.lstrip())
                stripped = line.strip()

                if not stripped or ':' not in stripped:
                    continue

                key, _, val = stripped.partition(':')
                key, val = key.strip(), val.strip()

                # Controlar profundidad
                while len(current_path) * 2 > indent:
                    current_path.pop()

                current_path.append(key)

                path = '/'.join(current_path)

                if path.endswith('metadata/name'):
                    metadata['name'] = val
                elif path.endswith('metadata/namespace'):
                    metadata['namespace'] = val
                elif path.endswith('spec/replicas'):
                    spec['replicas'] = val
                elif path.endswith('containers/name'):
                    if current_container:
                        containers.append(current_container)
                    current_container = {'name': val}
                elif path.endswith('containers/image'):
                    current_container['image'] = val
                elif path.endswith('ports/containerPort'):
                    current_container.setdefault('ports', []).append(val)
                elif 'resources/limits' in path:
                    current_container.setdefault('limits', {})[key] = val
                elif 'resources/requests' in path:
                    current_container.setdefault('requests', {})[key] = val

            if current_container:
                containers.append(current_container)

            # Mostrar metadata y replicas
            html.write(f'<div class="section">🧾 Información General</div>\n')
            html.write('<table><tr><th>Campo</th><th>Valor</th></tr>\n')
            for k, v in metadata.items():
                html.write(f'<tr><td>{k.capitalize()}</td><td>{v}</td></tr>\n')
            for k, v in spec.items():
                html.write(f'<tr><td>{k.capitalize()}</td><td>{v}</td></tr>\n')
            html.write('</table>\n')

            # Mostrar contenedores
            for c in containers:
                html.write(f'<div class="section">📦 Contenedor: <strong>{c.get("name", "")}</strong></div>\n')
                html.write('<table><tr><th>Propiedad</th><th>Valor</th></tr>\n')
                html.write(f'<tr><td>Imagen</td><td>{c.get("image", "")}</td></tr>\n')

                if 'ports' in c:
                    html.write(f'<tr><td>Puertos</td><td>{", ".join(c["ports"])}</td></tr>\n')

                if 'limits' in c:
                    limits = ', '.join(f'{k}: {v}' for k, v in c["limits"].items())
                    html.write(f'<tr><td>Límites</td><td>{limits}</td></tr>\n')

                if 'requests' in c:
                    reqs = ', '.join(f'{k}: {v}' for k, v in c["requests"].items())
                    html.write(f'<tr><td>Requests</td><td>{reqs}</td></tr>\n')

                html.write('</table>\n')


        elif tipo == 'quota':
            html.write('<div class="log-title">📊 Detalles de Quotas</div>')
            current_section = ""
            data_section = {}

            for line in lines:
                esc = line.rstrip()
                if not esc.strip():
                    continue

                if re.match(r'^\s*\w+:$', esc):  # Sección (hard:, used:, etc)
                    current_section = esc.strip().replace(':', '')
                    data_section[current_section] = []
                    continue

                if re.match(r'^\s{2,}\w', line):
                    key_val = esc.strip().split(':', 1)
                    if len(key_val) == 2 and current_section:
                        key, val = key_val
                        data_section[current_section].append((key.strip(), val.strip()))

            for section, rows in data_section.items():
                html.write(f'<div class="section">📂 {section.capitalize()}</div>\n')
                html.write('<table>\n<thead><tr><th>Recurso</th><th>Valor</th></tr></thead><tbody>\n')
                for key, val in rows:
                    html.write(f'<tr><td>{key}</td><td>{val}</td></tr>\n')
                html.write('</tbody></table>\n')

        elif tipo == 'pods':
            html.write('<div class="log-title">🧩 Lista de Pods</div>')
            headers = lines[0].split()
            html.write('<table><tr>' + ''.join(f"<th>{h}</th>" for h in headers) + '</tr>\n')
            for line in lines[1:]:
                if not line.strip():
                    continue
                cols = line.split()
                html.write('<tr>' + ''.join(f"<td>{c}</td>" for c in cols) + '</tr>\n')
            html.write('</table>')

        else:
            html.write('<div class="log-title">📄 Contenido General</div>')
            for line in lines:
                esc = line.strip()
                if sensitive_words and should_sanitize:
                    esc = sanitize_line(esc, sensitive_words)
                html.write(f'<div class="line normal">{esc}</div>\n')

        html.write("""
</div>
</body>
</html>
""")

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("Uso: python logs.py <input_path> <microservice> <ambiente> <tipo>")
        sys.exit(1)

    _, input_path, microservice, ambiente, tipo = sys.argv

    sensitive_env = os.getenv("SENSITIVE_WORDS", "")
    sensitive_words = [word.strip() for word in sensitive_env.split(",") if word.strip()]

    log_to_html(input_path, 'reporte.html', microservice, ambiente, tipo, sensitive_words)
