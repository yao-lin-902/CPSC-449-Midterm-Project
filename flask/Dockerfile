FROM tiangolo/uwsgi-nginx-flask:python3.8


ENV STATIC_URL /static
ENV STATIC_PATH /app/app/static
COPY ./requirements.txt /var/www/requirements.txt

RUN python -m pip install --upgrade pip
RUN pip install -r /var/www/requirements.txt
