# Base image
FROM ubuntu:20.04

# Install required packages
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
      git \
      build-essential \
      make \
      libssl-dev \
      ca-certificates \
      python3 \
      python3-pip \
    && python3 -m pip install pandas matplotlib \
    && rm -rf /var/lib/apt/lists/*

# Clone Dilithium repository
WORKDIR /dilithium
RUN git clone https://github.com/pq-crystals/dilithium.git .

# Build Dilithium shared libraries
WORKDIR /dilithium/ref
RUN make shared

# Copy custom C source files
COPY *.py ./
COPY *.c /dilithium/ref/
COPY run_analysis_dil.sh /run_analysis_dil.sh

# Set runtime library path
ENV LD_LIBRARY_PATH=/dilithium/ref

# Make the analysis script executable
RUN chmod +x /run_analysis_dil.sh

# Run the analysis script with the specified mode
CMD ["/bin/sh", "-c", "/run_analysis_dil.sh $MODE"]

# Expose results directory
VOLUME ["/results"]
