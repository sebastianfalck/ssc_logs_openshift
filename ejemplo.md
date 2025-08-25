```mermaid
flowchart LR
    A([Inicio]) --> B[Entrada de datos script:]
    B --> C{¿Condición?}
    C -- Sí --> D[Acción 1]
    C -- No --> E[Acción 2]
    D --> F[Proceso intermedio]
    E --> F
    F --> G[Salida de resultados]
    G --> H([Fin])
