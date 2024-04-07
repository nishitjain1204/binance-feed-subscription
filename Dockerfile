# pull official base image
FROM python:3.9-slim-buster

# set work directory
WORKDIR .

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
# copy project
COPY . .
RUN pip install -r requirements.txt
RUN chmod +x entrypoint.sh
# Run app.py when the container launches
ENTRYPOINT ["sh","entrypoint.sh"]

