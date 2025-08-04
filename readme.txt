<!-- HTML for Confluence Documentation -->
<h1>📘 Jenkins Pipeline Self-Service Guide for Microservices</h1>

<p>This pipeline allows developers to perform diagnostic and review actions on microservices deployed in OpenShift, in a controlled, secure, and self-managed way.</p>

<hr/>

<h2>✅ What can this pipeline do?</h2>
<ul>
  <li>Retrieve logs from the main microservice pod.</li>
  <li>Query the current configuration (Deployment YAML).</li>
  <li>Describe the active pod.</li>
  <li>View consumed resources and namespace quotas.</li>
  <li>List all pods in the namespace.</li>
  <li>Retrieve secrets and configmaps of the microservice.</li>
  <li>Restart the pod and monitor its behavior after restart.</li>
  <li>Validate country-based access.</li>
  <li>Automatically mask sensitive information.</li>
  <li>Send the results via email to the executor.</li>
</ul>

<h2>🔧 Pipeline Parameters</h2>
<table>
  <tr><th>Parameter</th><th>Type</th><th>Options</th><th>Description</th></tr>
  <tr><td><b>NOMBRE</b></td><td>string</td><td>-</td><td>Exact microservice name as listed in the CSV file.</td></tr>
  <tr><td><b>AMBIENTE</b></td><td>choice</td><td>dev, uat, prd, drs</td><td>Target environment for the selected action.</td></tr>
  <tr><td><b>ACCION</b></td><td>choice</td><td>none, get logs, get deployment, describe pod, get quota, get pods, get secrets, get configmaps, restart pod</td>
    <td>Action to perform. If <i>none</i>, no operation is executed.</td></tr>
</table>

<h2>🌍 Internal Environment Variables</h2>
<table>
  <tr><th>Variable</th><th>Description</th></tr>
  <tr><td><b>REPO_URL</b></td><td>Git repository URL for the CSV file.</td></tr>
  <tr><td><b>REPO_CREDENTIALS</b></td><td>Jenkins credential ID used for Git authentication.</td></tr>
  <tr><td><b>SERVER_INTERNAL</b></td><td>OpenShift internal cluster URL (dev/uat).</td></tr>
  <tr><td><b>SERVER_EXTERNAL</b></td><td>External OpenShift cluster URL (prd).</td></tr>
  <tr><td><b>SERVER_DRS</b></td><td>Disaster Recovery Site (DRS) cluster URL.</td></tr>
  <tr><td><b>SENSITIVE_WORDS</b></td><td>Keywords that trigger masking: password, token, secret, etc.</td></tr>
</table>

<h2>🔄 Pipeline Flow</h2>
<ol>
  <li>Clones the Git repository containing the CSV file.</li>
  <li>Reads and selects the microservice configuration based on <code>NOMBRE</code>.</li>
  <li>Validates country of executor against microservice's country.</li>
  <li>Performs <code>oc login</code> to the appropriate OpenShift cluster using the correct token.</li>
  <li>Executes the selected action.</li>
  <li>Masks sensitive data, if applicable.</li>
  <li>Sends an email report to the executing user.</li>
</ol>

<h2>🔐 Country-Based Access Control</h2>
<p>The pipeline checks that the microservice belongs to the same country as the executor by comparing:</p>
<ul>
  <li>The <b>country</b> field from the CSV.</li>
  <li>The folder in the Jenkins workspace path (e.g., <code>/colombia/project/</code>).</li>
</ul>
<p>If they do not match, the pipeline stops with an error.</p>


<h2>📝 Variable Format</h2>
<p>When entering values for <code>configmap</code> or <code>secret</code>, make sure to follow this format:</p>

<pre>
VARIABLE_NAME=value
</pre>

<p><b>Rules:</b></p>
<ul>
  <li>Each line must contain a single assignment in the form <code>variable=value</code>.</li>
  <li>Do not use quotes or spaces around the <code>=</code> symbol.</li>
  <li>If the value contains spaces, ensure it is properly encoded or escaped.</li>
  <li>Valid example:</li>
</ul>

<pre>
DB_USER=admin
DB_PASSWORD=Secret123
API_URL=https://api.example.com
</pre>

<p>This format will be parsed by the pipeline and automatically transformed into a <code>configmap</code> or <code>secret</code>, depending on the action selected.</p>


<h2>⚙️ Available Actions</h2>
<table>
  <tr>
    <th>Action</th>
    <th>Approval Required?</th>
    <th>Data Masking?</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><b>get logs</b></td><td>No</td><td>No</td>
    <td>Retrieves logs from the main pod. Useful to inspect startup issues, stack traces, connection failures, etc.</td>
  </tr>
  <tr>
    <td><b>get deployment</b></td><td>No</td><td>No</td>
    <td>Returns the full Deployment YAML, including image, variables, probes, resources, volumes, deployment strategy.</td>
  </tr>
  <tr>
    <td><b>describe pod</b></td><td>No</td><td>No</td>
    <td>Equivalent to <code>oc describe pod</code>. Shows events, restarts, probe status, volumes, ports, assigned node, etc.</td>
  </tr>
  <tr>
    <td><b>get quota</b></td><td>No</td><td>No</td>
    <td>Displays namespace resource usage and limits (CPU, memory, object counts). Helps identify quota-based blocks.</td>
  </tr>
  <tr>
    <td><b>get pods</b></td><td>No</td><td>No</td>
    <td>Lists pods in the namespace. Includes status, restarts, IPs, age, container images, etc.</td>
  </tr>
  <tr>
    <td><b>get secrets</b></td><td>Yes (qa/prd)</td><td>Yes (qa/prd)</td>
    <td>Retrieves secrets (passwords, tokens, certs). Requires approval in critical environments. Output is masked automatically.</td>
  </tr>
  <tr>
    <td><b>get configmaps</b></td><td>No</td><td>Yes</td>
    <td>Retrieves config files (e.g., application.yml). Sensitive values are automatically masked.</td>
  </tr>
  <tr>
    <td><b>restart pod</b></td><td>No</td><td>No</td>
    <td>Deletes the main pod, waits 20 seconds, shows pod status with <code>oc get pods</code>, then retrieves logs of the new pod. Useful for recovering stuck or frozen services.</td>
  </tr>
</table>

<h2>🧼 Sensitive Data Masking</h2>
<p>Output is automatically sanitized when containing keys that match the <b>SENSITIVE_WORDS</b> list.</p>
<p>Supported formats:</p>
<ul>
  <li><code>key=value</code></li>
  <li><code>key: value</code></li>
  <li><code>&lt;entry key="key"&gt;value&lt;/entry&gt;</code></li>
</ul>
<p><b>Examples:</b></p>
<table>
  <tr><th>Original</th><th>Masked</th></tr>
  <tr><td>password=MyPass</td><td>password=****</td></tr>
  <tr><td>token: abc123</td><td>token: ****</td></tr>
  <tr><td>&lt;entry key="secret"&gt;1234&lt;/entry&gt;</td><td>&lt;entry key="secret"&gt;****&lt;/entry&gt;</td></tr>
</table>

<h2>📧 Email Report</h2>
<ul>
  <li>Result is saved as <code>reporte.html</code>.</li>
  <li>Automatically sent to the user who triggered the pipeline.</li>
  <li>Email subject: <code>{ACCION} {NOMBRE} - {AMBIENTE}</code></li>
</ul>

<h2>📁 CSV File Structure</h2>
<p>The file <code>ProjectsJenkinsCardifCSV.csv</code> should follow this format (semicolon-separated):</p>
<pre>
appName;country;usage;NameSpaceDev;TokenDev;NameSpaceUat;TokenUat;NameSpacePrd;TokenPrd
cliente-ms;colombia;internal;ns-cliente-dev;token123;ns-cliente-uat;token456;ns-cliente-prd;token789
</pre>

<h2>🧠 Important Notes</h2>
<ul>
  <li>The microservice must be listed in the CSV file.</li>
  <li>Country validation is mandatory.</li>
  <li><code>get secrets</code> in <code>qa</code> and <code>prd</code> requires manual approval.</li>
  <li>Masking applies to <code>secrets</code> and <code>configmaps</code> where appropriate.</li>
  <li><code>REPO_URL</code> must be configured in the Jenkins folder/project.</li>
</ul>

<h2>📎 Related Resources</h2>
<ul>
  <li><a href="https://docs.openshift.com/container-platform/latest/cli_reference/openshift_cli/developer-cli-commands.html">OpenShift CLI documentation</a></li>
  <li><a href="https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/">Kubernetes ConfigMap Guide</a></li>
  <li><a href="https://www.jenkins.io/doc/book/security/">Jenkins Security Guide</a></li>
</ul>
