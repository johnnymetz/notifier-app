FROM python:3.9
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# install requirements
COPY requirements.txt ./
RUN pip install --upgrade pip && \
  pip install -r requirements.txt

# copy source code
COPY . .

# make port available to other containers
EXPOSE 8000

# run app when the container launches
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
