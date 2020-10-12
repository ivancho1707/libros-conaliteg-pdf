# VERSION 1.0
FROM jbarlow83/ocrmypdf

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends python3-distutils

RUN mkdir /conaliteg/

COPY main.py /conaliteg/
COPY requirements.txt /conaliteg/
COPY assets/ /conaliteg/assets/

RUN pip3 install -r /conaliteg/requirements.txt

WORKDIR /conaliteg

ENTRYPOINT ["/usr/bin/python3", "/conaliteg/main.py"]