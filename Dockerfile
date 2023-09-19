# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Install curl
RUN apt-get update && apt-get install -y curl

# Install Firefox and GeckoDriver
RUN apt-get update && apt-get install -y firefox-esr
RUN apt-get install -y wget
RUN apt-get install -y unzip
RUN apt-get install -y jq  # Install jq for JSON parsing
RUN GECKODRIVER_VERSION=$(curl -sS https://api.github.com/repos/mozilla/geckodriver/releases/latest | jq -r '.tag_name') && \
    wget https://github.com/mozilla/geckodriver/releases/download/$GECKODRIVER_VERSION/geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz && \
    tar -zxf geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz -C /usr/local/bin && \
    rm geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz


# Run your script when the container launches
CMD ["python", "weatherShop.py"]
