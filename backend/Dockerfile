# Start with a lightweight Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install poetry
RUN pip install poetry

# Copy only the dependency files to leverage Docker layer caching
COPY poetry.lock pyproject.toml /app/

# Install dependencies
RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi

# Copy the rest of the application code
COPY . /app/

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
