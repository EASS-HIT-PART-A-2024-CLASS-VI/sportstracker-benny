FROM python:3.10

# Create working directory
WORKDIR /app

# Copy your test-specific requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Default command: run tests
CMD ["pytest", "integration_tests/test_system_e2e.py"]