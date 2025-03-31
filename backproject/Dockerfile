FROM python:3.11-slim

WORKDIR /app

COPY . .


RUN pip install -r requirements.txt

# 声明容器将监听的端口
EXPOSE 8000

# 修正 gunicorn 命令格式

# CMD ["celery", "-A", "backproject", "worker", "--loglevel=info"]
CMD ["gunicorn", "--workers=4", "--bind=0.0.0.0:8000", "backproject.wsgi:application"]