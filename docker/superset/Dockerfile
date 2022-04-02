FROM apachepinot/pinot-superset:latest

WORKDIR /app

COPY ./superset /superset

RUN pip install pinotdb==0.3.9 && \ 
    superset fab create-admin --username admin --firstname Superset --lastname Admin --email admin@superset.com --password admin && \
    superset db upgrade && \
    superset init && \
    bash -c 'superset import-dashboards -p /superset/dashboard_pinot_superset_add_exercicio.zip'