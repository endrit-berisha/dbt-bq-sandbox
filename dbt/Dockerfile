FROM ghcr.io/dbt-labs/dbt-bigquery:1.8.1

RUN apt-get update && apt-get install -y curl
RUN curl -O https://dl.google.com/dl/clou1dsdk/channels/rapid/downloads/google-cloud-cli-478.0.0-linux-x86_64.tar.gz \
    && tar -xf google-cloud-cli-478.0.0-linux-x86_64.tar.gz \
    && ./google-cloud-sdk/install.sh

WORKDIR /root/.dbt
COPY profiles.yml  /root/.dbt
COPY .env  /root/.dbt

# Project
WORKDIR /.dbt
COPY . /.dbt
RUN pip install dbt-bigquery==1.0.0
