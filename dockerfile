FROM alpine

WORKDIR /solis2mqtt

COPY * ./

RUN apk update
RUN apk add python3 py3-pip
RUN pip install --no-cache-dir -r dependencies

#CMD [ "python", "./solis2mqtt.py" ]
