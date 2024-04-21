BASEDIR=$(cd -P -- "$(dirname -- "${0}")" && pwd -P)

rm -rf "${BASEDIR}/keys"
rm -rf "${BASEDIR}/data"
rm -rf "${BASEDIR}/../src/tech_challenge_001.egg-info"

docker build \
    --progress=plain \
    -f "${BASEDIR}/../containers/tech01.dockerfile" \
    -t "ivanpfalcao/tech-challenge-001:1.0.0" \
    "${BASEDIR}/.."