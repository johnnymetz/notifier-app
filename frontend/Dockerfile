FROM node:16
WORKDIR /app

# install dependencies
COPY package*.json ./
RUN npm install --silent

# copy source code
COPY . .

RUN npm run build

HEALTHCHECK CMD curl --fail http://localhost:3000 || exit 1

CMD ["npm", "start"]
