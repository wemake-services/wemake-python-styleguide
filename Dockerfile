# ========================================
# =               Warning!               =
# ========================================
# This is Github Action docker-based image.
# It is not intended for local development!
#
# It can still be used as a raw image for your own containers.
# See `action.yml` in case you want to learn more about Github Actions.
# See it live:
# https://github.com/wemake-services/wemake-python-styleguide/actions

# This image is also available on Dockerhub:
# https://hub.docker.com/r/wemakeservices/wemake-python-styleguide

FROM python:3.7-alpine

LABEL maintainer="sobolevn@wemake.services"
LABEL vendor="wemake.services"

ENV WPS_VERSION='0.12.5'

RUN apk add --no-cache bash
RUN pip install "wemake-python-styleguide==$WPS_VERSION"

COPY ./scripts/entrypoint.sh /
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
