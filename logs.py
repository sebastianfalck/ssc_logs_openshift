import sys

def log_to_html(input_path, html_path, microservices_name, ambiente, tipo):
    with open(input_path, 'r') as f:
        lines = f.readlines()

    with open(html_path, 'w') as html_file:
        html_file.write("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Log Report</title>
    <style>
        body {
            font-family: monospace;
            background-color: #f0f0f0;
            display: flex;
            justify-content: center;
            padding: 40px;
        }
        .container {
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            max-width: 90%;
            word-wrap: break-word;
            white-space: pre-wrap;
        }
        .info { color: blue; }
        .error { color: red; font-weight: bold; }
        .warning { color: orange; }
        .normal { color: #333; }
        h1 { color: #33cc33; text-align: center; }
    </style>
</head>
<body>
<div class="container">
""")
        html_file.write(f"<h1 class=\"title\">{tipo.upper()} de {microservices_name} en el ambiente {ambiente}</h1>\n")

        for line in lines:
            escaped = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            if 'ERROR' in line:
                html_file.write(f'<div class="error">{escaped}</div>\n')
            elif 'WARNING' in line:
                html_file.write(f'<div class="warning">{escaped}</div>\n')
            elif 'INFO' in line:
                html_file.write(f'<div class="info">{escaped}</div>\n')
            else:
                html_file.write(f'<div class="normal">{escaped}</div>\n')

        html_file.write("""
</div>
</body>
</html>
""")


if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("Uso: python logs.py <input_path> <nombre_microservicio> <ambiente> <tipo>")
        sys.exit(1)

    log_to_html(sys.argv[1], 'reporte.html', sys.argv[2], sys.argv[3], sys.argv[4])
