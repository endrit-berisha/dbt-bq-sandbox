FROM fishtownanalytics/dbt:1.0.0

WORKDIR /root/.dbt
COPY profiles.yml  /root/.dbt
COPY .env  /root/.dbt

# Project
WORKDIR /.dbt
COPY . /.dbt
RUN pip install dbt-bigquery
