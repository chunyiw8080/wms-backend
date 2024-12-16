FROM python:3.12.4
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
CMD ["gunicorn", "app:app", "--workers", "4", "--bind", "0.0.0.0:8000"]

# 运行：docker build -t chunyiwang/wms-backend:1 -f ./Dockerfile .