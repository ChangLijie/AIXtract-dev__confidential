FROM python:3.11-slim-bookworm

# Set working directory
WORKDIR /ws

# Copy AIxtract so packages to /opt/AIxtract
COPY packages/AIXtract /opt/AIXtract

# Add /opt/AIxtract to Python path and linker path
ENV PYTHONPATH="/opt/AIXtract:$PYTHONPATH"
ENV LD_LIBRARY_PATH="/opt/AIXtract:$LD_LIBRARY_PATH"

# Copy example and data folders into /ws
COPY example /ws/example
COPY data /ws/data
COPY README.md /ws/README.md
COPY CHANGELOG.md /ws/CHANGELOG.md

# Install Python requirements
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# install pdftohtml（in poppler-utils）
RUN apt-get update && \
    apt-get install -y --no-install-recommends poppler-utils && \
    apt-get install -y --no-install-recommends pdftohtml && \
    rm -rf /var/lib/apt/lists/*
