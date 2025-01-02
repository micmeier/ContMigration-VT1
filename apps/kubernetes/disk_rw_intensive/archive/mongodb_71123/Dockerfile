FROM python:3.9
RUN pip install pymongo
WORKDIR /disk_rw_intensive
COPY . .
CMD ["python3", "./diskrw_intensive_mongodb.py"]
