#create a requirements.txt which contains all the dependancies required for my application
#base image 
FROM python:3.9-slim



#Set working directory inside the container
WORKDIR /app

## Copy the requirements file to the working directory
COPY requirements.txt .

# Install the dependencies from the requirements file
RUN pip install gunicorn
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the working directory
COPY . .

EXPOSE 5000 

# Command to run the application
CMD [ "gunicorn", "--bind", "0.0.0.0:5000", "main:app" ]