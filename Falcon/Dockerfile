# Base Ubuntu 22.04 image
FROM ubuntu:22.04

# Install dependencies (gcc, make, curl, unzip)
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    make \
    libssl-dev \
    unzip \
    curl \
 && rm -rf /var/lib/apt/lists/*

# Create Falcon working directory
WORKDIR /falcon

# Download Falcon Round-3 submission archive
RUN curl -L -o falcon.zip https://falcon-sign.info/falcon-round3.zip

# Unzip Falcon files and remove the zip archive
RUN unzip falcon.zip && rm falcon.zip

# Set working directory to Falcon KAT implementation directory
WORKDIR /falcon/falcon-round3/Reference_Implementation/falcon512/falcon512int

# Build KAT generator for Falcon (kat512int executable)
RUN make clean && make

# Prepare the results directory
RUN mkdir -p /results

# Create a script to run KAT generation and move results to /results
RUN echo '#!/bin/bash\n\
./build/kat512int\n\
mv *.req *.rsp /results/' > /run_kat.sh \
 && chmod +x /run_kat.sh

# Default command to run when container starts
CMD ["/run_kat.sh"]
