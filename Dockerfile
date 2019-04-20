# 基础镜像
FROM python:3.3.6-alpine
# 维护者信息
MAINTAINER Sergey Khruschak <sergey.khruschak@gmail.com>
# 标签
LABEL version="0.1"
# 安装依赖
RUN pip install docker python-etcd
# 拷贝文件
COPY register.py /
# 执行命令
CMD ["python", "-u", "/register.py"]

# 如果是使用 docker-machine 的情形，当前就处于一个集群节点中 并且安装了 python 环境
# 也可以 ssh 进入一个虚拟机，然后在其中通过 Dockerfile 起一个进程
