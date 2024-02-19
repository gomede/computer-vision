# Use the official Python image as a base image
FROM python:3.9

# Set the working directory in the container to /risk_manager
WORKDIR /risk_manager

# Copy the dependencies file to the working directory and install dependencies
COPY requirements.txt /risk_manager/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files into the container
COPY . /risk_manager/

# Expose the port Django runs on
EXPOSE 8000

# Define the default command to run the Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
