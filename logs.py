import sys
import re

def log_to_html(input_path, html_path, microservice, ambiente, tipo):
    with open(input_path, 'r') as f:
        lines = f.readlines()

    with open(html_path, 'w') as html:
        html.write(f"""<!DOCTYPE html>
<html lang=\"es\">\n<head>\n    <meta charset=\"UTF-8\">\n    <title>Reporte de {tipo.upper()} - {microservice}</title>\n    <style>\n        body {{ font-family: 'Segoe UI', sans-serif; background-color: #f4f4f4; padding: 30px; color: #333; }}\n        .card {{ background: #ffffff; border-radius: 10px; padding: 25px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }}\n        h1 {{ background-color: #00a79d; color: white; padding: 15px; border-radius: 8px 8px 0 0; margin-top: 0; text-align: center; }}\n        .section-title {{ font-size: 1.2em; margin: 20px 0 10px; color: #00a79d; border-bottom: 2px solid #00a79d; padding-bottom: 5px; }}\n        .error {{ color: #cc0000; font-weight: bold; }}\n        .warning {{ color: #ff8800; }}\n        .info {{ color: #006699; }}\n        .normal {{ color: #333; }}\n        .line {{ white-space: pre-wrap; margin: 2px 0; }}\n        table.pods-table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}\n        table.pods-table th, table.pods-table td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}\n        table.pods-table th {{ background-color: #00a79d; color: white; }}\n        table.kv-table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}\n        table.kv-table th, table.kv-table td {{ border: 1px solid #ddd; padding: 8px; text-align: left; vertical-align: top; }}\n        table.kv-table th {{ background-color: #00a79d; color: white; }}\n        .no-value {{ background-color: #f9f9f9; font-style: italic; }}\n    </style>\n</head>\n<body>\n<div class=\"card\">\n    <h1>Reporte de {tipo.upper()} de {microservice} en {ambiente.upper()}</h1>\n""")

        t = tipo.lower()
        # Logs section
        if t in ['logs', 'get logs']:
            html.write('<div class="section-title">📋 Logs de aplicación</div>\n')
            for line in lines:
                esc = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                if 'ERROR' in line:
                    html.write(f'<div class="line error">❌ {esc}</div>\n')
                elif 'WARNING' in line:
                    html.write(f'<div class="line warning">⚠️ {esc}</div>\n')
                elif 'INFO' in line:
                    html.write(f'<div class="line info">ℹ️ {esc}</div>\n')
                else:
                    html.write(f'<div class="line normal">• {esc}</div>\n')

        # Pods section
        elif t in ['pods', 'get pods']:
            html.write('<div class="section-title">🧩 Lista de Pods</div>\n')
            if lines:
                headers = lines[0].split()
                html.write('<table class="pods-table"><tr>' + ''.join(f"<th>{h}</th>" for h in headers) + '</tr>\n')
                for line in lines[1:]:
                    if not line.strip(): continue
                    cols = line.split()
                    html.write('<tr>' + ''.join(f"<td>{c}</td>" for c in cols) + '</tr>\n')
                html.write('</table>\n')

        # Key-Value table for deployment, describe, quota
        elif t in ['deployment', 'get deployment', 'describe', 'describe pod', 'quota', 'get quota']:
            html.write(f'<div class="section-title">📊 Detalle {tipo.title()}</div>\n')
            html.write('<table class="kv-table">\n  <tr><th>Variable</th><th>Valor</th></tr>\n')
            for line in lines:
                esc = line.strip()
                if not esc:
                    continue
                if ':' in esc:
                    key, value = [p.strip() for p in esc.split(':', 1)]
                    if value:
                        html.write(f'  <tr><td>{key}</td><td>{value}</td></tr>\n')
                    else:
                        html.write(f'  <tr class="no-value"><td colspan=\"2\">{esc}</td></tr>\n')
                else:
                    html.write(f'  <tr class="no-value"><td colspan=\"2\">{esc}</td></tr>\n')
            html.write('</table>\n')

        # Fallback general content
        else:
            html.write('<div class="section-title">📄 Contenido General</div>\n')
            for line in lines:
                esc = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').strip()
                html.write(f'<p>{esc}</p>\n')

        html.write("""\n</div>\n</body>\n</html>""")

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("Uso: python logs.py <input_path> <microservice> <ambiente> <tipo>")
        sys.exit(1)

    _, input_path, microservice, ambiente, tipo = sys.argv
    log_to_html(input_path, 'reporte.html', microservice, ambiente, tipo)
