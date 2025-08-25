<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Diagrama con Mermaid</title>
  <!-- Cargar Mermaid desde CDN -->
  <script type="module">
    import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
    mermaid.initialize({ startOnLoad: true });
  </script>
</head>
<body>
  <h2>Ejemplo de diagrama de flujo con Mermaid</h2>

  <!-- Aquí va el diagrama -->
  <div class="mermaid">
    flowchart TD
      A([Inicio]) --> B[Entrada de datos]
      B --> C{¿Condición?}
      C -- Sí --> D[Acción 1]
      C -- No --> E[Acción 2]
      D --> F[Proceso intermedio]
      E --> F
      F --> G[Salida de resultados]
      G --> H([Fin])
  </div>
</body>
</html>
