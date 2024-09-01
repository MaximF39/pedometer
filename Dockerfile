FROM python:3.12-alpine

WORKDIR /service

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=60

COPY req.txt req.txt
RUN python -m pip install --upgrade pip
RUN pip install -r req.txt

COPY alembic.ini .
COPY alembic alembic
COPY src src
COPY main.py main.py
# alembic upgrade head
CMD ["alembic", "upgrade", "head"]

ENTRYPOINT ["python", "main.py"]
