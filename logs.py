import sys
import re

def log_to_html(input_path, html_path, microservice, ambiente, tipo):
    with open(input_path, 'r') as f:
        lines = f.readlines()

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
            margin-top: 15px;
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
            current_section = ''
            for line in lines:
                esc = line.strip()
                if not esc:
                    continue
                if not line.startswith(" "):
                    current_section = esc
                    html.write(f'<div class="section">📌 {esc}</div>\n')
                else:
                    html.write(f'<div class="line normal">{esc}</div>\n')

        elif tipo in ['secrets', 'configmaps']:
            label = {
                'secrets': '🔐 Secrets',
                'configmaps': '🧾 ConfigMaps'
            }[tipo]
            html.write(f'<div class="log-title">{label}</div>\n')

            key = None
            for line in lines:
                stripped = line.strip()
                if stripped.startswith("#"):
                    key = stripped[1:].strip()
                elif key is not None:
                    valor = stripped
                    combined = f"{key}={valor}".replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                    html.write(f'<div class="line normal">{combined}</div>\n')
                    key = None

        elif tipo == 'env':
            html.write('<div class="log-title">🌱 Variables de entorno (.env)</div>')
            for line in lines:
                esc = line.strip()
                if '=' in esc:
                    key, value = esc.split('=', 1)
                    key = key.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                    value = value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                    html.write(f'<div class="section">🔑 {key}</div>\n')
                    html.write(f'<div class="line normal">{value}</div>\n')

        elif tipo in ['deployment', 'quota']:
            label = {
                'deployment': '📦 Despliegue YAML',
                'quota': '📊 Cuotas de Recursos',
            }[tipo]
            html.write(f'<div class="log-title">{label}</div>')
            yaml_block = "".join(lines)
            esc = yaml_block.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            html.write(f'<div class="yaml">{esc}</div>\n')

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
    log_to_html(input_path, 'reporte.html', microservice, ambiente, tipo)
