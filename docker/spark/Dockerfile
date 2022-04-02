FROM jupyter/all-spark-notebook:spark-3.1.1

WORKDIR /home/jovyan/work/

USER root

COPY ./spark/notebooks /home/jovyan/work/notebooks
COPY ./spark/app /home/jovyan/work/app
COPY ./spark/api /home/jovyan/work/api    
COPY ./spark/csv /home/jovyan/work/csv
COPY ./spark/json /home/jovyan/work/json
COPY ./spark/secrets /etc/secrets

RUN chmod -R 777 /home/jovyan/ && pip install flask flask-cors kafka-python sseclient pyspark 

EXPOSE 8888