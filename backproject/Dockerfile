FROM python:3.11-slim

ARG DOCKER_UID=2000

RUN useradd -u "$DOCKER_UID" -U -s /bin/false -M appuser


RUN mkdir -p /var/log/backserver && \
    chown -R appuser:appuser /var/log/backserver && \
    chmod -R 755 /var/log/backserver

RUN mkdir -p /var/log/backend && \
    chown -R appuser:appuser /var/log/backend && \
    chmod -R 755 /var/log/backend

WORKDIR /app

COPY --chown=appuser:appuser . .
RUN chmod -R 755 /app

# 需要root权限安装依赖
RUN pip install -r requirements.txt
# COPY entrypoint.sh /entrypoint.sh
# RUN chmod +x /entrypoint.sh

# ENTRYPOINT ["/entrypoint.sh"]
USER appuser
# 声明容器将监听的端口
EXPOSE 8000

# 修正 gunicorn 命令格式
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
# CMD ["celery", "-A", "backproject", "worker", "--loglevel=info"]
# CMD ["gunicorn", "--workers=4", "--bind=0.0.0.0:8000", "--log-level=info", "--error-logfile=/var/log/backserver/gunicorn_error.log", "--access-logfile=/var/log/backserver/gunicorn_access.log", "backproject.wsgi:application"]
CMD ["gunicorn", "--workers=4", "--bind=0.0.0.0:8000", "--log-level=info", "--access-logfile", "-", "--error-logfile", "-", "backproject.wsgi:application"]

# 