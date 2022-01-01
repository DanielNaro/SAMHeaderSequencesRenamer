FROM ubuntu:20.04
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Moscow
RUN apt-get update && apt-get install -y curl git samtools python3 python3-pip
RUN git clone https://github.com/DanielNaro/SAMHeaderSequencesRenamer.git
RUN pip3 install pysam
ENV PATH="/SAMHeaderSequencesRenamer:${PATH}"
