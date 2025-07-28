import sys

def log_to_html(log_path, nombre, ambiente, tipo):
    html_path = "reporte.html"

    with open(log_path, 'r') as log_file:
        lines = log_file.readlines()

    with open(html_path, 'w') as html_file:
        html_file.write(f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Reporte - {nombre} - {ambiente}</title>
    <style>
        body {{
            font-family: 'Courier New', Courier, monospace;
            padding: 20px;
            background-color: #f9f9f9;
            color: #222;
        }}
        .log-title, .pods-title, .kv-title, .configmap-title, .secrets-title {{
            font-size: 18px;
            font-weight: bold;
            margin-top: 25px;
        }}
        .log-title       {{ color: #1e1e1e; }}
        .pods-title      {{ color: #28a745; }}
        .kv-title        {{ color: #2c7be5; }}
        .configmap-title {{ color: #2c7be5; }}
        .secrets-title   {{ color: #ff9800; }}

        .log-line {{
            background-color: #e8e8e8;
            padding: 4px;
            margin: 2px 0;
            border-radius: 4px;
        }}
        .pods-table, .kv-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
            margin-bottom: 30px;
        }}
        .pods-table th, .pods-table td,
        .kv-table td {{
            border: 1px solid #ccc;
            padding: 6px 10px;
            text-align: left;
        }}
        .pods-table th {{
            background-color: #e6f4ea;
            font-weight: bold;
        }}
        .no-value td {{
            background-color: #f4f4f4;
            font-style: italic;
            color: #666;
        }}
    </style>
</head>
<body>
""")

        tipo_lower = tipo.lower()

        if tipo_lower == "logs":
            html_file.write(f'<div class="log-title">📄 <strong>LOG</strong></div>')
            for line in lines:
                html_file.write(f'<div class="log-line">{line.strip()}</div>')

        elif tipo_lower == "pods":
            html_file.write(f'<div class="pods-title">🧩 <strong>PODS</strong></div>')
            if lines:
                headers = lines[0].split()
                html_file.write('<table class="pods-table"><tr>')
                for header in headers:
                    html_file.write(f'<th>{header}</th>')
                html_file.write('</tr>')
                for line in lines[1:]:
                    cols = line.split()
                    html_file.write('<tr>')
                    for col in cols:
                        html_file.write(f'<td>{col}</td>')
                    html_file.write('</tr>')
                html_file.write('</table>')

        elif tipo_lower in ["deployment", "describe", "quota", "configmaps"]:
            titulo = {
                "deployment": "🚀 <strong>DEPLOYMENT</strong>",
                "describe": "🔍 <strong>DESCRIBE</strong>",
                "quota": "📊 <strong>QUOTA</strong>",
                "configmaps": "📦 <strong>CONFIGMAPS</strong>"
            }.get(tipo_lower, tipo.upper())

            clase = {
                "deployment": "kv-title",
                "describe": "kv-title",
                "quota": "kv-title",
                "configmaps": "configmap-title"
            }.get(tipo_lower, "kv-title")

            html_file.write(f'<div class="{clase}">{titulo}</div>')
            html_file.write('<table class="kv-table">')
            for line in lines:
                if ':' in line:
                    key, value = line.split(':', 1)
                    html_file.write(f'<tr><td>{key.strip()}</td><td>{value.strip()}</td></tr>')
                else:
                    html_file.write(f'<tr class="no-value"><td colspan="2">{line.strip()}</td></tr>')
            html_file.write('</table>')

        elif tipo_lower == "secrets":
            html_file.write('<div class="secrets-title">🔐 <strong>SECRETS</strong></div>')
            html_file.write('<table class="kv-table">')
            for line in lines:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    value = value if value else "<em>(oculto)</em>"
                    html_file.write(f'<tr><td>{key}</td><td>{value}</td></tr>')
                else:
                    html_file.write(f'<tr class="no-value"><td colspan="2">{line.strip()}</td></tr>')
            html_file.write('</table>')

        else:
            html_file.write('<div class="log-title">⚠️ Tipo no reconocido</div>')
            for line in lines:
                html_file.write(f'<div class="log-line">{line.strip()}</div>')

        html_file.write("""
</body>
</html>
""")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Uso: python logs.py <ruta_log> <nombre> <ambiente> <tipo>")
        print("Ejemplo: python logs.py pods.txt ms-app dev pods")
    else:
        log_to_html(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
