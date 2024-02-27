# Using python 3.10 slim image as the base image
FROM python:3.10.7-slim
# Defining working directory and copy the requirements file
WORKDIR /usr/src/myapp
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5005
CMD ["python3","inventory_service_server.py"]