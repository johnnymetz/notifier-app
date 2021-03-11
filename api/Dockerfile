FROM python:3.9
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_WATCHMAN_TIMEOUT=20

ARG WM_VERSION=v2021.03.01.00

# install watchman
# hadolint ignore=SC2039,DL3003
RUN wget https://github.com/facebook/watchman/releases/download/$WM_VERSION/watchman-$WM_VERSION-linux.zip && \
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

# make port available to other containers
EXPOSE 8000

# run app when the container launches
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
