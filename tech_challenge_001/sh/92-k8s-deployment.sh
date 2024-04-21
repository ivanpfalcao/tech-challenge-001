BASEDIR=$(cd -P -- "$(dirname -- "${0}")" && pwd -P)

NAMESPACE="tech-challenge-001"

kubectl create namespace "${NAMESPACE}"

kubectl -n "${NAMESPACE}" delete deployment tech-challenge-001
kubectl -n "${NAMESPACE}" apply -f "${BASEDIR}/tech-challenge-dpl.yaml"