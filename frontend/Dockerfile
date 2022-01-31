FROM node:16
WORKDIR /app

# install dependencies
COPY package*.json ./
RUN npm install --silent

# copy source code
COPY . .

ARG NEXT_PUBLIC_API_HOST
ENV NEXT_PUBLIC_API_HOST=${NEXT_PUBLIC_API_HOST}

RUN npm run build

CMD ["npm", "run", "start"]
