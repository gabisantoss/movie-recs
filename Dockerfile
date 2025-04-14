FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl iputils-ping net-tools && rm -rf /var/lib/apt/lists/*


COPY . .

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["python", "-m", "src.entrypoint"]