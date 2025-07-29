oc get secret <nombre-del-secret> -o jsonpath="{.data}" | jq
oc get configmap <nombre-del-configmap> -o jsonpath="{.data}" | jq
