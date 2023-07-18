FROM python:3-slim
MAINTAINER Julian-Samuel Gebühr

ENV DOCKER_BUILD=true

ENV VIRTUAL_ENV=/var/ilmo/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY src/requirements.txt requirements.txt
RUN pip install -r requirements.txt
WORKDIR /var/ilmo
COPY . .
RUN pip install -e .  # Without the -e the library static folder will not be copied by collectstatic!
RUN mkdir /ilmo
RUN mkdir /ilmo/static
RUN ilmo-manage collectstatic --noinput -v 2

COPY docker/ilmo.bash $VIRTUAL_ENV/bin/ilmo

EXPOSE 8345
CMD ["ilmo"]
