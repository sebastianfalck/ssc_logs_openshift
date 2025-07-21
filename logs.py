import sys

def log_to_html(input_path, html_path, microservice, ambiente, tipo):
    # Leer todas las líneas del archivo de entrada
    with open(input_path, 'r') as f:
        lines = f.readlines()

    # Crear el HTML de salida con estilos para distintos niveles de log
    with open(html_path, 'w') as html:
        html.write("""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Reporte de {} - {}</title>
    <style>
        body {{ font-family: monospace; background: #f0f0f0; padding: 40px; }}
        .container {{ background: #fff; padding: 20px; border-radius: 8px;
                      box-shadow: 0 0 10px rgba(0,0,0,0.1); white-space: pre-wrap; }}
        .error {{ color: red; font-weight: bold; }}
        .warning {{ color: orange; }}
        .info {{ color: blue; }}
        .normal {{ color: #333; }}
        h1 {{ color: #33cc33; text-align: center; }}
    </style>
</head>
<body>
<div class="container">
""".format(tipo.upper(), microservice))

        # Título dinámico
        html.write(f"<h1>{tipo.upper()} de {microservice} en {ambiente}</h1>\n\n")

        # Procesar cada línea y asignar clase según nivel
        for line in lines:
            esc = (line
                   .replace("&", "&amp;")
                   .replace("<", "&lt;")
                   .replace(">", "&gt;"))
            if 'ERROR' in line:
                html.write(f'<div class="error">{esc}</div>\n')
            elif 'WARNING' in line:
                html.write(f'<div class="warning">{esc}</div>\n')
            elif 'INFO' in line:
                html.write(f'<div class="info">{esc}</div>\n')
            else:
                html.write(f'<div class="normal">{esc}</div>\n')

        # Cerrar contenedores HTML
        html.write("""
</div>
</body>
</html>
""")

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("Uso: python logs.py <input_path> <microservice> <ambiente> <tipo>")
        sys.exit(1)

    # Llamada principal con parámetros de línea de comandos
    _, input_path, microservice, ambiente, tipo = sys.argv
    log_to_html(input_path, 'reporte.html', microservice, ambiente, tipo)
