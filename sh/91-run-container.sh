BASEDIR=$(cd -P -- "$(dirname -- "${0}")" && pwd -P)

docker rm -f tech-challenge-001

docker run \
    -d \
    --name "tech-challenge-001" \
    -p 8000:8000 \
    -t "ivanpfalcao/tech-challenge-001:1.0.0"