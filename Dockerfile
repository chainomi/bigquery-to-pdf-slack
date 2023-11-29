FROM python:3.10-slim-bullseye

RUN apt-get update 

# Make dir app
RUN mkdir /app

WORKDIR /app

# Copy the source from the current directory to the Working Directory inside the container
COPY app/ .

# remove the line below - added for testing only - do not use in production
# COPY useful-circle-358120-5ebbc15b4e95.json .  

#install dependencies
RUN pip install -r requirements.txt


# add flask-user to run app
RUN adduser --disabled-password app-user

# change working directory --disabled-passwordownership to flask-user
RUN chown app-user /app

USER app-user 

# Run the executable
CMD ["python", "app.py"]