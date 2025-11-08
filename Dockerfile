# Use an official lightweight Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the dependency file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Command to run the application's CLI by default
# The -u flag ensures that prints go directly to the terminal
CMD ["python", "-u", "-m", "src.main"]