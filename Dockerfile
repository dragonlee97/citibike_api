FROM python:3.10-buster

WORKDIR /citibike_api

COPY . .
RUN pip install --no-cache-dir --upgrade -r /citibike_api/requirements.txt
ENV GOOGLE_APPLICATION_CREDENTIALS="/application_default_credentials.json"
CMD ["uvicorn", "main:api", "--reload", "--host", "0.0.0.0"]
EXPOSE 8080