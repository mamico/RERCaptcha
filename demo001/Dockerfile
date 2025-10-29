FROM python:3.11-slim
#RUN apt-get update && apt-get install -y --no-install-recommends \
#    build-essential curl \
#    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
RUN pip install --no-cache-dir flask requests
COPY app.py /app/app.py
COPY static/ /app/
EXPOSE 5000
CMD ["python", "app.py"]
