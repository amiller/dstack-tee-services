FROM ubuntu:jammy AS builder

RUN apt-get update
RUN apt-get install -y git wget

# Install pre-built Intel DCAP local repo
WORKDIR /
RUN wget https://download.01.org/intel-sgx/sgx-dcap/1.21/linux/distro/ubuntu22.04-server/sgx_debian_local_repo.tgz 
RUN tar -xzf /sgx_debian_local_repo.tgz
RUN echo "deb [trusted=yes arch=amd64] file:/sgx_debian_local_repo jammy main" >> /etc/apt/sources.list

RUN apt-get update
RUN apt-get -y install sgx-pck-id-retrieval-tool libsgx-dcap-default-qpl tdx-qgs libtdx-attest
RUN apt-get -y install python3-pip cmake
RUN pip install sgx-dcap-quote-verify-python

# Try building some sample program for verifying a quote

WORKDIR /root/
RUN git clone https://github.com/intel/SGX-TDX-DCAP-QuoteVerificationLibrary
WORKDIR SGX-TDX-DCAP-QuoteVerificationLibrary/Src
# RUN ./release

WORKDIR /root/
RUN pip install flask requests eth_account
ADD main.py ./

# Define entrypoint
EXPOSE 5003
ENTRYPOINT []
CMD ["python3", "main.py"]

