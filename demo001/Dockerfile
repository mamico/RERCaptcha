FROM python:3.11-slim
#RUN apt-get update && apt-get install -y --no-install-recommends \
#    build-essential curl \
#    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt -c constraints.txt
EXPOSE 5000
CMD ["python", "app.py"]
