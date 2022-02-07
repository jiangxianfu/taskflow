# base images
FROM centos:8
# author
LABEL author="jiangxf@ctrip.com"
# set env
ENV LANG=en_US.UTF-8
ENV PYTHONIOENCODING=utf8
ENV DOCKER_HOST=LOCAL
# set timezone
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
# make work dir
RUN mkdir -p /taskflow /var/log/supervisor /var/log/taskflow
# set work dir
WORKDIR /taskflow
# install system packages
RUN yum install -y python3 git telnet && yum clean all
# install pip packages
COPY requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt --no-cache-dir

# clean
RUN rm -rf /tmp/*

# cmd
CMD ["/bin/bash"]