FROM python:3-slim
MAINTAINER Julian-Samuel Gebühr

ENV VIRTUAL_ENV=/var/ilmo/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY src/requirements.txt requirements.txt
RUN pip install -r requirements.txt
WORKDIR /var/ilmo
COPY . .
RUN pip install .

COPY docker/ilmo.bash $VIRTUAL_ENV/bin/ilmo

EXPOSE 8345
CMD ["ilmo"]
