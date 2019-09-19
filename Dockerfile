# This is Github Action docker-based image.
# It can still be used as a raw image for your own containers.
# See `action.yml` in case you want to learn more about Github Actions.

FROM python:3.7-alpine

ENV WPS_VERSION='0.12.3'

RUN apk add --no-cache bash
RUN pip install "wemake-python-styleguide==$WPS_VERSION"
RUN python --version && pip --version && flake8 --version

COPY ./scripts/entrypoint.sh /
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
