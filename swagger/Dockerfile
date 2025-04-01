FROM python:3.9
WORKDIR /app
COPY app.py swagger.yml requirements.txt /app/
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
