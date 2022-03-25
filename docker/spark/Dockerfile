FROM jupyter/all-spark-notebook:spark-3.1.1

WORKDIR /home/jovyan/work

RUN pip install flask flask-cors kafka-python sseclient

CMD chmod -R 777 api csv json notebooks app