# Most of this file comes from https://cloud.google.com/run/docs/quickstarts/build-and-deploy/shell
# The installation of the gcloud command-line tool has been added.
FROM golang:1.14-buster as builder
WORKDIR /app
COPY go.* ./
RUN go mod download
COPY invoke.go ./
RUN go build -mod=readonly -v -o server
FROM debian:buster-slim
RUN set -x && apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    --no-install-recommends \
    ca-certificates && \
    rm -rf /var/lib/apt/lists/*
# Install the gcloud command-line tool, so script.sh can use it.
# For details, see https://cloud.google.com/sdk/docs/install#deb.
RUN apt-get update && \
    apt-get install -y curl gnupg && \
    echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg  add - && \
    apt-get update -y && \
    apt-get install google-cloud-sdk -y
COPY --from=builder /app/server /app/server
COPY script.sh ./
CMD ["/app/server"]
