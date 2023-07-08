# Pull base image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /Tableway

# Install dependencies
COPY requirements.txt /Tableway/
RUN pip install -r requirements.txt

# Copy project
COPY . /Tableway/

RUN rm -r accounts/tests.py
RUN rm -r bookings/tests.py
RUN rm -r payments/tests.py
