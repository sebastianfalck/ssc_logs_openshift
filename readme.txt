<!-- HTML para documentación Confluence -->
<h1>📘 Guía de uso del Pipeline Jenkins para Autosoporte de Microservicios</h1>

<p>Este pipeline permite a los desarrolladores ejecutar acciones de diagnóstico y revisión sobre microservicios desplegados en OpenShift, de manera controlada, segura y autogestionada.</p>

<hr/>

<h2>✅ ¿Qué permite hacer este pipeline?</h2>
<ul>
  <li>Obtener logs del pod principal del microservicio.</li>
  <li>Consultar la configuración actual (Deployment YAML).</li>
  <li>Describir el pod activo.</li>
  <li>Ver recursos consumidos y cuotas del namespace.</li>
  <li>Listar pods.</li>
  <li>Obtener secretos y configmaps del microservicio.</li>
  <li>Reiniciar el pod y observar su comportamiento post-reinicio.</li>
  <li>Validar acceso por país.</li>
  <li>Proteger automáticamente información sensible.</li>
  <li>Enviar por correo los resultados al ejecutor.</li>
</ul>

<h2>🔧 Parámetros del pipeline</h2>
<table>
  <tr><th>Parámetro</th><th>Tipo</th><th>Opciones</th><th>Descripción</th></tr>
  <tr><td><b>NOMBRE</b></td><td>string</td><td>-</td><td>Nombre exacto del microservicio según el archivo CSV.</td></tr>
  <tr><td><b>AMBIENTE</b></td><td>choice</td><td>dev, uat, prd, drs</td><td>Ambiente sobre el cual se ejecuta la acción.</td></tr>
  <tr><td><b>ACCION</b></td><td>choice</td><td>none, get logs, get deployment, describe pod, get quota, get pods, get secrets, get configmaps, restart pod</td>
    <td>Acción a ejecutar. Si es <i>none</i>, no se realiza ninguna operación.</td></tr>
</table>

<h2>🌍 Variables de entorno internas</h2>
<table>
  <tr><th>Variable</th><th>Descripción</th></tr>
  <tr><td><b>REPO_URL</b></td><td>URL del repositorio Git del archivo CSV.</td></tr>
  <tr><td><b>REPO_CREDENTIALS</b></td><td>Credencial Jenkins para autenticación al repo.</td></tr>
  <tr><td><b>SERVER_INTERNAL</b></td><td>URL del OpenShift interno (dev/uat).</td></tr>
  <tr><td><b>SERVER_EXTERNAL</b></td><td>URL del OpenShift externo (prd).</td></tr>
  <tr><td><b>SERVER_DRS</b></td><td>URL del clúster DRS (contingencia).</td></tr>
  <tr><td><b>SENSITIVE_WORDS</b></td><td>Palabras clave que activan censura: password, token, secret, etc.</td></tr>
</table>

<h2>🔄 Flujo general del pipeline</h2>
<ol>
  <li>Clona el repositorio con el archivo CSV.</li>
  <li>Lee y selecciona la configuración del microservicio (NOMBRE).</li>
  <li>Verifica el país del ejecutor vs el del microservicio.</li>
  <li>Realiza <code>oc login</code> al clúster correcto con el token adecuado.</li>
  <li>Ejecuta la acción seleccionada.</li>
  <li>Censura la información sensible si aplica.</li>
  <li>Envía el reporte por correo al usuario ejecutor.</li>
</ol>

<h2>🔐 Control de acceso por país</h2>
<p>El pipeline valida que el microservicio pertenezca al país del usuario que lo ejecuta, comparando:</p>
<ul>
  <li>El campo <b>country</b> del CSV.</li>
  <li>La carpeta en la ruta del workspace Jenkins (ejemplo: <code>/colombia/proyecto/</code>).</li>
</ul>
<p>Si no coinciden, el pipeline se detiene con error.</p>

<h2>⚙️ Acciones disponibles</h2>
<table>
  <tr>
    <th>Acción</th>
    <th>¿Requiere aprobación?</th>
    <th>¿Censura datos?</th>
    <th>Descripción</th>
  </tr>
  <tr>
    <td><b>get logs</b></td><td>No</td><td>No</td>
    <td>Extrae los logs del pod principal. Muestra errores de arranque, fallos funcionales, errores de conexión, trazas, etc.</td>
  </tr>
  <tr>
    <td><b>get deployment</b></td><td>No</td><td>No</td>
    <td>Devuelve el YAML completo del Deployment. Muestra imagen, variables, probes, recursos, volúmenes, estrategia de despliegue.</td>
  </tr>
  <tr>
    <td><b>describe pod</b></td><td>No</td><td>No</td>
    <td>Resultado de <code>oc describe pod</code>. Muestra eventos, reinicios, estado de probes, puertos, volúmenes y nodo.</td>
  </tr>
  <tr>
    <td><b>get quota</b></td><td>No</td><td>No</td>
    <td>Muestra límites y uso de recursos (CPU, memoria, objetos). Útil para detectar bloqueos por cuotas.</td>
  </tr>
  <tr>
    <td><b>get pods</b></td><td>No</td><td>No</td>
    <td>Lista los pods del namespace. Indica estado, IP, reinicios, tiempo de vida, imágenes usadas, etc.</td>
  </tr>
  <tr>
    <td><b>get secrets</b></td><td>Sí (qa/prd)</td><td>Sí (qa/prd)</td>
    <td>Extrae secretos (passwords, tokens, certificados, etc.). Requiere aprobación en ambientes críticos y aplica censura automática.</td>
  </tr>
  <tr>
    <td><b>get configmaps</b></td><td>No</td><td>Sí</td>
    <td>Extrae configuración externa. Muestra propiedades (application.yml, etc). Aplica censura automática a valores sensibles.</td>
  </tr>
  <tr>
    <td><b>restart pod</b></td><td>No</td><td>No</td>
    <td>Elimina el pod principal del microservicio, espera 20 segundos, muestra el estado de los pods y luego los logs del nuevo pod. Útil para desbloquear microservicios congelados o trabados.</td>
  </tr>
</table>

<h2>🧼 Censura de datos sensibles</h2>
<p>La salida es sanitizada automáticamente si contiene claves con las palabras definidas en <b>SENSITIVE_WORDS</b>.</p>
<p>Soporta los siguientes formatos:</p>
<ul>
  <li><code>clave=valor</code></li>
  <li><code>clave: valor</code></li>
  <li><code>&lt;entry key="clave"&gt;valor&lt;/entry&gt;</code></li>
</ul>
<p><b>Ejemplos:</b></p>
<table>
  <tr><th>Original</th><th>Censurado</th></tr>
  <tr><td>password=MyPass</td><td>password=****</td></tr>
  <tr><td>token: abc123</td><td>token: ****</td></tr>
  <tr><td>&lt;entry key="secret"&gt;1234&lt;/entry&gt;</td><td>&lt;entry key="secret"&gt;****&lt;/entry&gt;</td></tr>
</table>

<h2>📧 Correo con resultado</h2>
<ul>
  <li>El resultado se guarda como <code>reporte.html</code>.</li>
  <li>Se envía automáticamente al usuario que ejecutó el pipeline.</li>
  <li>El asunto del correo es: <code>{ACCION} {NOMBRE} - {AMBIENTE}</code></li>
</ul>

<h2>📁 Estructura del archivo CSV</h2>
<p>El archivo <code>ProjectsJenkinsCardifCSV.csv</code> debe tener el siguiente formato (separado por punto y coma):</p>
<pre>
appName;country;usage;NameSpaceDev;TokenDev;NameSpaceUat;TokenUat;NameSpacePrd;TokenPrd
cliente-ms;colombia;internal;ns-cliente-dev;token123;ns-cliente-uat;token456;ns-cliente-prd;token789
</pre>

<h2>🧠 Notas importantes</h2>
<ul>
  <li>El microservicio debe existir en el CSV.</li>
  <li>La validación por país es obligatoria.</li>
  <li><code>get secrets</code> en <code>qa</code> y <code>prd</code> requiere autorización.</li>
  <li>La censura se aplica a <code>secrets</code> y <code>configmaps</code> cuando corresponde.</li>
  <li><code>REPO_URL</code> debe estar definido en la configuración del proyecto/carpeta Jenkins.</li>
</ul>

<h2>📎 Recursos relacionados</h2>
<ul>
  <li><a href="https://docs.openshift.com/container-platform/latest/cli_reference/openshift_cli/developer-cli-commands.html">Documentación oc CLI</a></li>
  <li><a href="https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/">Guía ConfigMaps Kubernetes</a></li>
  <li><a href="https://www.jenkins.io/doc/book/security/">Seguridad en Jenkins</a></li>
</ul>
