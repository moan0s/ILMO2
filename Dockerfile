FROM python:3-slim
MAINTAINER Julian-Samuel Gebühr

RUN python -m venv /var/ilmo/venv
COPY src/requirements.txt requirements.txt
RUN /var/ilmo/venv/bin/pip install -r requirements.txt
WORKDIR /var/ilmo
COPY . .
RUN /var/ilmo/venv/bin/pip install .

CMD ["/var/ilmo/venv/bin/gunicorn", "ilmo.wsgi", "--bind=0.0.0.0:8345"]
