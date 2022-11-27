FROM python:3.11
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_WATCHMAN_TIMEOUT=20

# https://github.com/facebook/watchman/releases
# get the release that has an asset named watchman-<VERSION>-linux.zip
ARG WM_VERSION=v2022.01.03.00

RUN apt-get update && \
  apt-get -y upgrade && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

# install watchman: https://stackoverflow.com/questions/66513668/error-installing-watchman-into-a-python-docker-container
# hadolint ignore=SC2039,SC3009,DL3003
RUN wget -nv https://github.com/facebook/watchman/releases/download/$WM_VERSION/watchman-$WM_VERSION-linux.zip && \
  unzip watchman-*-linux.zip && \
  cd watchman-*-linux && \
  mkdir -p /usr/local/{bin,lib} /usr/local/var/run/watchman && \
  cp bin/* /usr/local/bin && \
  cp lib/* /usr/local/lib && \
  chmod 755 /usr/local/bin/watchman && \
  chmod 2777 /usr/local/var/run/watchman && \
  cd .. && \
  rm -rf watchman-*-linux.zip watchman-*-linux

WORKDIR /app

# install requirements
COPY requirements.txt ./
# hadolint ignore=DL3013
RUN pip install --upgrade --no-cache-dir pip && \
  pip install --no-cache-dir -r requirements.txt

# copy source code
COPY . .

# HEALTHCHECK CMD curl --fail http://localhost:8000 || exit 1

# run app when the container launches
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
