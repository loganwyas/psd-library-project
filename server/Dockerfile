FROM python:3.8-alpine

COPY ./requirements.txt /server/requirements.txt

WORKDIR /server

RUN pip install -r requirements.txt

COPY . /server

EXPOSE 5001
ENV PORT 5001
ENV HOSTNAME "0.0.0.0"

CMD /server/run_prod_server.sh