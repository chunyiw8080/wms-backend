FROM python:3.12.4
WORKDIR /app
COPY requirements.txt ./
RUN pip config set global.index-url https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
RUN pip install cryptography
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ARG CONTAINER_PORT=8000
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV CONTAINER_PORT=${CONTAINER_PORT}
EXPOSE 8000
ENTRYPOINT ["sh", "-c", "gunicorn app:app --workers 2 --bind 0.0.0.0:${CONTAINER_PORT}"]

# 运行：docker build -t chunyiwang/wms-backend:1 -f ./Dockerfile .