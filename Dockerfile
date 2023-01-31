FROM python:3.9-alpine

WORKDIR /com-piler
COPY . .
RUN pip install -r requirements.txt

CMD ["python", "app.py"]

# docker build -t com-piler .
# docker run -d --name com-piler --restart always -p 5010:5010 com-piler:latest