FROM ubuntu:20.04

# Step 2: Set environment variables (optional but often useful)
ENV DEBIAN_FRONTEND=noninteractive  

# Step 3: Install dependencies and any necessary packages
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    valgrind \
    curl \
    git \
    vim && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

CMD ["bash"]
