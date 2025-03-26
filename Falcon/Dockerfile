# Use an official Ubuntu image as the base.
FROM ubuntu:22.04

# Install required packages: git, build-essential (for gcc, make, etc.), and libssl-dev for OpenSSL.
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    make \
    libssl-dev \
    unzip \
    clang \
    curl \
 && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container.
WORKDIR /falcon

# Download the FALCON submission zip file.
RUN curl -L -o falcon.zip https://falcon-sign.info/falcon-round3.zip

# Unzip the downloaded archive and remove the zip file.
# This should create directories like Reference_Implementation, Optimized_Implementation, KAT, Supporting_Documentation, and Extra.
RUN unzip falcon.zip && rm falcon.zip


# Change directory to the unified C implementation.
# If the archive extracts to a folder named "falcon", then the unified C implementation is likely at:
WORKDIR /falcon/falcon-round3/Extra/c

# Build the Falcon unified C implementation.
RUN make

# By default, run the self-test tool.
#CMD ["./test_falcon"]