docker run --rm \
  -v "$(pwd)/requirements.in:/run/requirements.in" \
  -v "$(pwd):/run" \
  python:3.10.11 \
  /bin/sh -c "pip install pip-tools && pip-compile /run/requirements.in > /run/requirements.txt"
