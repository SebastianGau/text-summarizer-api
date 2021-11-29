FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

WORKDIR /app

# Copy and install requirements
COPY requirements.txt /app
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000

# Copy contents from your local to your docker container
COPY ./app /app

# execution is handled by the base image
# CMD ["python","main.py"]
EXPOSE 80