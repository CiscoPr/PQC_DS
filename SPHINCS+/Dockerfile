# Use a base image with a recent Ubuntu release
FROM ubuntu:20.04

# Install essential build tools and git
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
      build-essential \
      git \
      ca-certificates \
      make \
      libssl-dev \
      && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /sphincsplus

# Clone the SPHINCS+ repository from GitHub
RUN git clone https://github.com/sphincs/sphincsplus.git

# Change to the repository directory
WORKDIR /sphincsplus/sphincsplus/ref

# (Optional) If you need to modify parameters, you can copy a custom params.h file:
# COPY my_params.h ref/params/params-myparams.h
# And then modify the Makefile or set an environment variable to use it.

# Build the project (this will use the provided Makefile)
RUN make

# Run the test suite and output all messages to stdout.
# Using /bin/sh -c ensures that all output appears in container logs.
CMD ["/bin/sh", "-c", "make test 2>/dev/null"]
