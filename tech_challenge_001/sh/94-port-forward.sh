#!/bin/bash

BASEDIR=$(cd -P -- "$(dirname -- "${0}")" && pwd -P)
NAMESPACE="tech-challenge-001"

while true; do
	kubectl -n "${NAMESPACE}" port-forward svc/tech-challenge-001-service 8000:8000 --address=0.0.0.0
	echo "kubectl port-forward terminated. Restarting in 1 seconds..."
	sleep 1
done