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

# set mirrors
RUN mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.backup
RUN curl -o /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-8.repo
COPY pip.conf /etc/pip.conf

# install system packages
RUN yum install -y python3 git && yum clean all
# install pip packages
COPY requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt --no-cache-dir

# clean
RUN rm -rf /tmp/*

# cmd
CMD ["/bin/bash"]