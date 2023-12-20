FROM python:3.9
RUN pip3 install redis
WORKDIR /mem_intensive
COPY ./mem_intensive.py .
CMD ["python3", "./mem_intensive.py"]
