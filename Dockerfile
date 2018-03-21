FROM ubuntu:16.04
RUN apt update && apt install -y python2.7 python-cups 
ADD zebra /www/zebra
ADD server.py /www
WORKDIR /www
EXPOSE 8000
CMD ["python", "server.py"]
