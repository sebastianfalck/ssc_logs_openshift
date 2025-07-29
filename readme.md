oc get secret springbootproject -o json | jq -r '.data | to_entries[] | "\(.key)=\(.value | @base64d)"'




oc get configmap springbootproject -o json | jq -r '.data | to_entries[] | "\(.key)=\(.value)"'


