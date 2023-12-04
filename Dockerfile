# ========================================
# =               Warning!               =
# ========================================
# This is Github Action docker-based image.
# It is not intended for local development!
#
# You can find docs about how to setup your own Github Action here:
# https://wemake-python-styleguide.rtfd.io/en/latest/pages/usage/integrations/github-actions.html
#
# It can still be used as a raw image for your own containers.
# See `action.yml` in case you want to learn more about GitHub Actions.
# See it live:
# https://github.com/wemake-services/wemake-python-styleguide/actions
#
# This image is also available on Dockerhub:
# https://hub.docker.com/r/wemakeservices/wemake-python-styleguide

FROM python:3.11.5-alpine

LABEL maintainer="mail@sobolevn.me"
LABEL vendor="wemake.services"

ENV WPS_VERSION='0.18.0'
ENV REVIEWDOG_VERSION='v0.15.0'

RUN apk add --no-cache bash git wget
RUN pip install "wemake-python-styleguide==$WPS_VERSION" \
  # Installing reviewdog to optionally comment on pull requests:
  && wget -O - -q 'https://raw.githubusercontent.com/reviewdog/reviewdog/master/install.sh' \
  | sh -s -- -b /usr/local/bin/ "$REVIEWDOG_VERSION"

# Custom configuration for this action:
COPY ./scripts/action-config.cfg /

# Entrypoint:
COPY ./scripts/entrypoint.sh /
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
