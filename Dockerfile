# 1. Use an official, lightweight Python base image to keep the container small.
FROM python:3.11-slim

# 2. Set the working directory inside the virtual container.
WORKDIR /app

# 3. Copy only the requirements file first.
COPY requirements.txt .

# 4. Install the Python dependencies. 
# We use --no-cache-dir to prevent pip from saving temporary files, keeping the image small.
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your application code into the container.
COPY . .

# 6. Expose the port the app runs on.
EXPOSE 8000

# 7. Start the Uvicorn server.
CMD ["uvicorn", "npc_server:app", "--host", "0.0.0.0", "--port", "8000"]