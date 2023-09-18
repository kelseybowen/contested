FROM python:3.11

RUN pip install flask pymysql python-dotenv flask_bcrypt

COPY Pipfile /Pipfile

COPY server.py /server.py

COPY flask_app/ /flask_app/

COPY DigiCertGlobalRootCA.pem /DigiCertGlobalRootCA.pem 

COPY .env /.env

CMD ["python3", "server.py"]