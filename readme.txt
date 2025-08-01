h1. 🧰 Jenkins Pipeline de Autosoporte para Microservicios

Este pipeline permite a los desarrolladores ejecutar acciones de diagnóstico y revisión sobre microservicios desplegados en OpenShift, de forma controlada, segura y autogestionada.

---

h2. ✅ ¿Qué puedes hacer con este pipeline?

* Obtener logs del pod principal del microservicio.
* Ver la configuración actual del deployment.
* Describir el estado completo de un pod.
* Ver el uso y límites de recursos (quotas).
* Listar pods activos en el namespace.
* Obtener secretos (con aprobación en ambientes críticos).
* Ver configmaps con sanitización automática.
* Recibir el resultado por correo automáticamente.
* Validación del entorno y país.

---

h2. 🔧 Parámetros del pipeline

|| Parámetro || Tipo || Opciones || Descripción ||
| *NOMBRE*   | string | libre     | Nombre exacto del microservicio según CSV |
| *AMBIENTE* | choice | dev, uat, prd, drs | Entorno en el que se encuentra el microservicio |
| *ACCION*   | choice | none, get logs, get deployment, describe pod, get quota, get pods, get secrets, get configmaps | Acción que deseas ejecutar sobre el microservicio |

---

h2. 🌍 Variables de entorno utilizadas

|| Variable || Descripción ||
| *REPO_URL*         | URL del repositorio Git con el archivo CSV de configuración |
| *REPO_CREDENTIALS* | ID de la credencial Jenkins para acceso Git |
| *SERVER_INTERNAL*  | OpenShift interno (`dev`, `uat`) |
| *SERVER_EXTERNAL*  | OpenShift externo (`prd`) |
| *SERVER_DRS*       | Clúster DRS (contingencia) |
| *SENSITIVE_WORDS*  | Palabras clave para censura: _password, username, user, token, secret_ |

---

h2. 🔄 Flujo del pipeline

#1. _Checkout_ del repositorio (se espera el archivo ProjectsJenkinsCardifCSV.csv).  
#2. Lectura del archivo CSV y búsqueda del microservicio por nombre.  
#3. Validación del país del microservicio contra la ruta de ejecución.  
#4. Autenticación con `oc login` al clúster correspondiente.  
#5. Ejecución de la acción seleccionada.  
#6. Sanitización automática (si aplica).  
#7. Envío del resultado por correo al ejecutor.

---

h2. 🔐 Validación por país

El pipeline valida que el microservicio pertenezca al mismo país del desarrollador, comparando:

* Columna `country` del CSV
* Nombre del subdirectorio en la ruta Jenkins (`env.WORKSPACE`)

Si no coinciden, se aborta la ejecución con un mensaje de advertencia.

---

h2. ⚙️ Acciones disponibles

|| Acción || Requiere Aprobación || Censura datos || Detalles ||
| *get logs*       | No  | No  | Logs en tiempo real del pod. Útil para detectar errores, fallas de conexión, trazabilidad de eventos. |
| *get deployment* | No  | No  | YAML del deployment. Incluye imagen, variables, probes, volúmenes, recursos, etc. |
| *describe pod*   | No  | No  | Describe el pod completo. Incluye estado, eventos, reinicios, volúmenes, probes. |
| *get quota*      | No  | No  | Consulta `ResourceQuota` y `LimitRange`. Muestra uso/consumo de CPU, memoria, objetos. |
| *get pods*       | No  | No  | Lista todos los pods con estado, edad, IP, imagen, reinicios, nodo, etc. |
| *get secrets*    | Sí (qa/prd) | Sí (qa/prd) | Extrae secretos (tokens, contraseñas, etc.). Requiere aprobación y censura automática. |
| *get configmaps* | No  | Sí  | Muestra configmaps. Incluye propiedades (`application.yml`, `.properties`) con sanitización. |

---

h3. 🧼 Ejemplo de sanitización

Los valores sensibles serán ocultados si la clave contiene alguna palabra definida en _SENSITIVE_WORDS_.

*Entrada original:*
{code}
database.password=SuperSecret123
api-token: abcd1234
<entry key="db.user">admin</entry>
{code}

*Salida censurada:*
{code}
database.password=****
api-token: ****
<entry key="db.user">****</entry>
{code}

---

h2. 📧 Envío por correo

* El resultado de la acción se guarda como _reporte.html_
* Se envía automáticamente al ejecutor (`BUILD_USER_EMAIL`)
* Asunto: _ACCION NOMBRE - AMBIENTE_
* Ejemplo: `get logs cliente-ms - dev`

---

h2. 📁 Estructura del CSV de configuración

El archivo `ProjectsJenkinsCardifCSV.csv` debe estar delimitado por punto y coma (`;`) y contener:

|| Columna || Descripción ||
| appName       | Nombre del microservicio |
| country       | País asociado |
| usage         | Tipo de uso (`internal`, `external`, etc.) |
| NameSpaceDev  | Namespace para `dev` |
| TokenDev      | Token para `dev` |
| NameSpaceUat  | Namespace para `uat` |
| TokenUat      | Token para `uat` |
| NameSpacePrd  | Namespace para `prd` |
| TokenPrd      | Token para `prd` |
| ...           | Otros ambientes si aplica |

---

h2. 🧠 Notas adicionales

* Si el microservicio no está en el CSV, el pipeline fallará.
* Si el país del microservicio y el del workspace no coinciden, la ejecución se aborta.
* En `qa` y `prd`, la acción `get secrets` solo puede ser aprobada por usuarios específicos.
* El campo `TOKEN` es sensible y no debe imprimirse directamente.
* El pipeline es autosoportado, pero tiene controles para evitar accesos indebidos.

---

h2. 📎 Contacto

Para soporte de este pipeline, contacta al equipo DevOps o crea un ticket en Jira con etiqueta: *soporte-jenkins-microservicios*.

