FROM python:3.13-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

RUN python -m src.planninghub_coding_challenge.components.utils.schema_generator

# Change this if you want to run on a different port
# Make sure to change the port in the .env file and docker-compose.yml file too if you do
EXPOSE 8080 

CMD ["python", "-m", "src.planninghub_coding_challenge.main"]
