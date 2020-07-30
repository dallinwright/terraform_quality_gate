FROM ubuntu:latest as install

RUN apt-get update
RUN apt-get install -y curl unzip wget

# Install terraform
RUN wget -O terraform.zip \
  https://releases.hashicorp.com/terraform/0.12.29/terraform_0.12.29_linux_amd64.zip && \
  unzip terraform.zip && \
  rm terraform.zip

# Install tflint
RUN curl -L \
  "$(curl -Ls https://api.github.com/repos/terraform-linters/tflint/releases/latest \
  | grep -o -E "https://.+?_linux_amd64.zip")" \
  -o tflint.zip && \
  unzip tflint.zip && \
  rm tflint.zip

FROM alpine:latest as prod

MAINTAINER "Dallin Wright"

RUN apk add --no-cache ca-certificates python3 py3-pip go git

COPY --from=install /tflint /usr/local/bin
COPY --from=install /terraform /usr/local/bin

# Copies repository and mounts it for docker
WORKDIR /github/workspace

RUN go get -v github.com/stretchr/testify/assert
RUN go get -v github.com/gruntwork-io/terratest/modules/terraform

# Copies your code file from your action repository to the filesystem path `/` of the container
COPY entrypoint.py /entrypoint.py

# Copies your code file from your action repository to the filesystem path `/` of the container
COPY modules /modules

# Code file to execute when the docker container starts up (`entrypoint.py`)
ENTRYPOINT ["/entrypoint.py"]