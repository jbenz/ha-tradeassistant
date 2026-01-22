ARG BUILD_FROM
FROM $BUILD_FROM

ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1

RUN apk add --no-cache python3 python3-dev py3-pip gcc musl-dev libffi-dev openssl-dev curl

WORKDIR /app
COPY rootfs/app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY rootfs/app/ .

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8898/health || exit 1

CMD ["python3", "main.py"]
