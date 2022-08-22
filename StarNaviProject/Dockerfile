FROM python:3.7


ARG SQL_USER
ENV SQL_USER=${SQL_USER}

ARG MYSQL_ROOT_PASSWORD
ENV MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}

ARG SQL_HOST
ENV SQL_HOST=${SQL_HOST}

ARG SQL_DATABASE
ENV SQL_DATABASE=${SQL_DATABASE}

WORKDIR /src

COPY requirements.txt /src/
RUN pip install -r requirements.txt

COPY app /src/app/
COPY main.py /src/main.py

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]