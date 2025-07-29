oc get secret <nombre-del-secret> -o json | jq -r '.data | to_entries[] | "\(.key)=\(.value | @base64d)"'



oc get configmap <nombre-del-configmap> -o json | jq -r '.data | to_entries[] | "\(.key)=\(.value)"'

