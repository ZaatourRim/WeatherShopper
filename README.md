# Weather Shopper Automation

This Python script automates the shopping process on the Weather Shop website based on the current temperature. It can automatically select and purchase either moisturizers or sunscreens, depending on the temperature. You can run this script using Docker to ensure consistent dependencies and environments.

## Table of Contents
- [Introduction](#introduction)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running with Docker](#running-with-docker)
  - [Running without Docker](#running-without-docker)


## Introduction

The Weather Shop Automation Script uses Selenium to interact with the Weather Shop website. It reads the current temperature and makes shopping decisions accordingly. If the temperature is below 19°C, it selects moisturizers, and if the temperature is above 34°C, it selects sunscreens.

## Getting Started

To use this script with Docker, follow the instructions below:

### Prerequisites

Before you begin, ensure that you have Docker installed on your system. You can download and install Docker from the official website: [Docker](https://www.docker.com/get-started).

### Installation

1. Clone this repository or download the project files.

### running-with-docker
  - run this command to build the Docker image everytime you change something in the code:

   ```docker build -t my-weather-shopper . ```
  - run this command to run the container in Docker, my-weather-shopper is the name of the image:

   ```docker run my-weather-shopper```
  
### running-without-docker
- make sure you have an updated firefox locally: you can download it from here:
https://www.mozilla.org/en-US/firefox/new/
- run this command to run the script on your local machine:

Make sure to comment the line 126 ```my_driver = webdriver.Firefox(firefox_options)``` in weatherShop.py and uncomment the line 128 ```my_driver = webdriver.Firefox()``` in weatherShop.py to navigate the GUI in firefox window.

- then, run the code locally with this command:

  ```python3 weatherShop.py```



   

