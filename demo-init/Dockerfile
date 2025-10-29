FROM python:3.12-slim

RUN pip install argon2-cffi
WORKDIR /app
COPY init.py .
CMD ["python", "init.py"]

