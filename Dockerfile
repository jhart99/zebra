FROM ubuntu:16.04
RUN apt update && apt install -y python2.7 python-cups 
ADD cgi-bin /www/cgi-bin
WORKDIR /www
EXPOSE 8000
CMD ["python", "-m", "CGIHTTPServer"]
