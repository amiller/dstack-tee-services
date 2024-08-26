FROM ubuntu:jammy AS builder

RUN apt-get update && apt-get install -y libssl-dev libcurl4-openssl-dev cmake rustc cargo vim
RUN apt-get install -y git wget

# RUN git clone https://github.com/intel/SGX-TDX-DCAP-QuoteVerificationLibrary/
# WORKDIR SGX-TDX-DCAP-QuoteVerificationLibrary/Src
# RUN apt-get install -y build-essential ocaml ocamlbuild automake autoconf libtool wget python-is-python3 libssl-dev git cmake perl

# Install pre-built Intel DCAP local repo
WORKDIR /
RUN wget https://download.01.org/intel-sgx/sgx-dcap/1.21/linux/distro/ubuntu22.04-server/sgx_debian_local_repo.tgz 
RUN tar -xzf /sgx_debian_local_repo.tgz
RUN echo "deb [trusted=yes arch=amd64] file:/sgx_debian_local_repo jammy main" >> /etc/apt/sources.list

RUN apt-get update
RUN apt-get -y install sgx-pck-id-retrieval-tool libsgx-dcap-default-qpl tdx-qgs libtdx-attest

# Try building some sample program for verifying a quote

# WORKDIR /
# RUN git clone https://github.com/intel/SGXDataCenterAttestationPrimitives

# Define entrypoint
ENTRYPOINT []
CMD ["bash"]

