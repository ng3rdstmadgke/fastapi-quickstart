FROM python:3.8.12-slim-bullseye

#ENV http_proxy http://xxx.jp:7080
#ENV https_proxy http://xxx.jp:7080
#ENV NO_PROXY 169.254.169.254

RUN apt update && \
    apt install -y locales gcc libmariadb-dev
#    apt install -y iputils-ping net-tools default-mysql-client

RUN echo 'ja_JP.UTF-8 UTF-8' >> /etc/locale.gen && \
    locale-gen && \
    update-locale LANG=ja_JP.UTF-8

#RUN cd /tmp && \
#    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64-2.0.30.zip" -o "awscliv2.zip" && \
#    unzip awscliv2.zip && \
#    ./aws/install && \
#    rm -r aws awscliv2.zip

RUN ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime

RUN mkdir -p /opt/app
WORKDIR /opt/app
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .

COPY docker/app/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh
COPY docker/app/uvicorn.sh /usr/local/bin/uvicorn.sh
RUN chmod +x /usr/local/bin/uvicorn.sh
CMD ["/usr/local/bin/entrypoint.sh"]