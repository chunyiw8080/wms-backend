FROM python:3.12.4
WORKDIR /app
COPY requirements.txt ./
# RUN pip config set global.index-url https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
RUN pip install cryptography
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
EXPOSE 8000
ENTRYPOINT ["sh", "-c", "gunicorn app:app --workers 2 --bind 0.0.0.0:8000"]
