FROM python:3.11.2-bullseye

RUN apt update

RUN pip install Flask==3.0.0

RUN mkdir /app
WORKDIR /app

COPY . /app

# Partie variable d'environnement URLs
ENV URL_VNC="https://vnc.insa-cvl.com/"
ENV URL_VDI="https://vdi.insa-cvl.com/"
ENV URL_API="https://api.insa-cvl.com/"


EXPOSE 5000

CMD ["/bin/bash", "entrypoint.sh"]