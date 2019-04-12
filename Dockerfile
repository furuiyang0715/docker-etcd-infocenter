FROM python:3.3.6-alpine
MAINTAINER Sergey Khruschak <sergey.khruschak@gmail.com>
LABEL version="0.1"

# 安装了 docker 和 python-etcd 可以这么写？？
RUN pip install docker python-etcd
COPY register.py /

CMD ["python", "-u", "/register.py"]
