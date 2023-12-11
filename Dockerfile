FROM python:3.12
LABEL maintainer="Adam Barcan <abarcan@gmail.com>"

ENV APP_HOME /usr/src/app/
ENV REDIS_HOST 'redis'

WORKDIR $APP_HOME
COPY . $APP_HOME

RUN \
    pip install poetry \ 
    && poetry config virtualenvs.create false \
    && poetry install

EXPOSE 5000

CMD ["poetry", "run", "flask", "--app", "json_counter_py", "run", "--host=0.0.0.0"]
