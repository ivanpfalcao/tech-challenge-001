BASEDIR=$(cd -P -- "$(dirname -- "${0}")" && pwd -P)

docker build \
    --progress=plain \
    -f "${BASEDIR}/../containers/tech01.dockerfile" \
    -t "ivanpfalcao/tech-challenge-001:1.0.0" \
    "${BASEDIR}/.."