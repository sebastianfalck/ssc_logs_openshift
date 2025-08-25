{html}
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

<script type="module">
  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
  mermaid.initialize({ startOnLoad: true });
</script>
{html}

