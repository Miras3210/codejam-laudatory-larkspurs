#############################
# Single-stage Python image #
#############################
FROM python:3.12-slim

LABEL org.opencontainers.image.title="good-image-terminal" \
	  org.opencontainers.image.description="A simple yet interesting image editor." \
	  org.opencontainers.image.licenses="MIT"

ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1 \
	PORT=8000

# Set the working directory
WORKDIR /app

# Copy project files
COPY build.py pyproject.toml README.md uv.lock* ./
RUN pip install --no-cache-dir . 

COPY public ./public
COPY src ./src

# Build at container start so edits can be picked up by rebuilding container only.

EXPOSE 8000

CMD ["bash", "-c", "python build.py --serve --port ${PORT}"]

#########################################
# Usage
#   docker build -t good-image-terminal:latest .
#   docker run --rm --name good-image-terminal -e PORT=8000 -p 8000:8000 good-image-terminal:latest
# App: http://localhost:8000
#########################################
