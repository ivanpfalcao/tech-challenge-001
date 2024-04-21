#!/bin/bash
BASEDIR=$(cd -P -- "$(dirname -- "${0}")" && pwd -P)

NAMESPACE="tech-challenge-001"
FILE_PATH="${BASEDIR}/keys"
FILE_NAME="${FILE_PATH}/api_keys_list.txt"

mkdir -p "${FILE_PATH}"
echo "gfsdgfdhghd" > ${FILE_NAME}
echo "hgdfhgfdjhf" >> ${FILE_NAME}

# Create the Kubernetes secret
kubectl create secret generic api-keys-secret \
    --from-file="${FILE_NAME}" \
    --namespace="${NAMESPACE}"