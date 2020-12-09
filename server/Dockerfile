FROM python:3.8-slim
MAINTAINER OUMAR DIABY

# for start we copy the files in the local docker dir
RUN pip install pika

# Actually install the application
WORKDIR /usr/src/server
# It's only a single file.  It has to be in the same directory as the
# Dockerfile, or a subdirectory, but not a parent or sibling.
COPY server.py .

CMD ["python"]