FROM fishtownanalytics/dbt:1.0.0

WORKDIR /root/.dbt
COPY profiles.yml /root/.dbt
COPY .env /root/.dbt

# Project
WORKDIR /usr/app
COPY . /usr/app

RUN pip install dbt-bigquery

ENTRYPOINT ["dbt"]
