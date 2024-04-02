ARG BASE_REGISTRY

FROM ${BASE_REGISTRY}python:3.12-alpine3.19 as base

ENV TZ="Europe/Paris"

RUN --mount=type=cache,target=/var/cache/apk \
    apk update --no-cache && \
    apk upgrade --no-cache && \
    apk add --no-cache --update \
    git \
    curl \
    bash \
    jq \
    yq \
    moreutils \
    util-linux \
    ca-certificates \
    tzdata && \
    cp /usr/share/zoneinfo/${TZ} /etc/localtime

RUN --mount=type=cache,target=/var/cache/apk \
    apk add --no-cache --update --repository="http://dl-cdn.alpinelinux.org/alpine/edge/community" \
    helm \
    github-cli