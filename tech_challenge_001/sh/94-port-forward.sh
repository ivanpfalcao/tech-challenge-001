#!/bin/bash
BASEDIR=$(cd -P -- "$(dirname -- "${0}")" && pwd -P)

NAMESPACE="tech-challenge-001"


kubectl -n "${NAMESPACE}" port-forward svc/tech-challenge-001-service 8000:8000 --address=0.0.0.0