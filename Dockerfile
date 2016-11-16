FROM ubuntu:16.04

RUN apt-get update && apt-get install -y \
  python

# schema tool
RUN mkdir -p /usr/local/adnxs/schema-tool
WORKDIR /usr/local/adnxs/schema-tool
COPY schematool ./schematool/
COPY conf/ ./conf/

WORKDIR ./schematool

CMD ['/bin/bash', './schema.py']
