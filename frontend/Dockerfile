FROM node:14
WORKDIR /app

# install dependencies
COPY package*.json ./
RUN npm install --silent

# copy source code
COPY . .

RUN npm run build

CMD ["npm", "start"]
