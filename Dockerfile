# The packaged 'uwsgi-python3' is compiled on python 3.7.5, so this can't be
# changed. If needs to change, you need to install and compile UWSGI from pip.
FROM python:3.7.5-alpine3.10

# Set woking directory
WORKDIR /usr/src/app

# Install dependencies (uwsgi 2.0.18)
RUN apk add uwsgi-python3 uwsgi-http

# Add 'site-packages' to PYTHONPATH
ENV PYTHONPATH=${PYTHONPATH}:/usr/local/lib/python3.7/site-packages

COPY requirements.txt .

RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

EXPOSE 8000

COPY static static
COPY templates templates
COPY wsgi.py server.ini ./

ENTRYPOINT [ "uwsgi" ] 

CMD [ "--ini", "server.ini" ]
