FROM python:3-slim
WORKDIR /python/Cloud-Computing-Tarea1
RUN pip3 install flask
COPY . .
RUN python3 db.py
CMD [ "python3", "./app.py" ]