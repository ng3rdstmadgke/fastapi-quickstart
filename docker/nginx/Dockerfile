FROM nginx:1.21.5

#ENV http_proxy http://xxx.jp:7080
#ENV https_proxy http://xxx.jp:7080
#ENV NO_PROXY 169.254.169.254

RUN apt update && \
    apt install locales -y
#    apt install -y iputils-ping net-tools

RUN echo 'ja_JP.UTF-8 UTF-8' >> /etc/locale.gen && \
    locale-gen && \
    update-locale LANG=ja_JP.UTF-8

RUN ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime

COPY ./docker/nginx/config/nginx.conf /etc/nginx/nginx.conf
COPY ./docker/nginx/config/default.conf /etc/nginx/conf.d/default.conf

RUN mkdir -p /opt/app
COPY . /opt/app