BASEDIR=$(cd -P -- "$(dirname -- "${0}")" && pwd -P)

pushd "${BASEDIR}/.."
pip install .
popd