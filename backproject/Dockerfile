FROM python:3.11-slim

ARG DOCKER_UID=1000
ARG DOCKER_GID=1000

RUN groupadd -r appuser -g ${DOCKER_GID} && \
    useradd -r -u ${DOCKER_UID} -g appuser -s /bin/false appuser



RUN mkdir -p /var/log/gunicorn && \
    chown -R appuser:appuser /var/log/gunicorn

WORKDIR /app

COPY --chown=appuser:appuser . .
RUN chmod -R 777 /app

# 需要root权限安装依赖
RUN pip install -r requirements.txt
# COPY entrypoint.sh /entrypoint.sh
# RUN chmod +x /entrypoint.sh

# ENTRYPOINT ["/entrypoint.sh"]

# 声明容器将监听的端口
EXPOSE 8000

# 修正 gunicorn 命令格式

# CMD ["celery", "-A", "backproject", "worker", "--loglevel=info"]
CMD ["gunicorn", "--workers=4", "--bind=0.0.0.0:8000", "--access-logfile=/var/log/gunicorn/access.log", "--error-logfile=/var/log/gunicorn/error.log", "backproject.wsgi:application"]

# 