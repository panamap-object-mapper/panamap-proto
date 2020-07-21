#!/bin/sh
set -ex

PROTOC_VERSION=3.12.3
ARCHIVE=protoc-${PROTOC_VERSION}-linux-x86_64.zip

wget https://github.com/protocolbuffers/protobuf/releases/download/v${PROTOC_VERSION}/${ARCHIVE}
unzip -o ${ARCHIVE} -d . bin/protoc
rm -f ${ARCHIVE}
