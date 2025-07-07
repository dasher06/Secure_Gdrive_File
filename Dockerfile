# Use the official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8080

# Run the Flask app
CMD ["python", "Encrypted_Link.py"]

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "Encrypted_Link:app"]
# Use gunicorn to serve the Flask app