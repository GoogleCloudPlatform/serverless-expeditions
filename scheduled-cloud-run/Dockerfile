FROM node:15
WORKDIR /usr/src/app
COPY package.json package*.json ./
RUN npm install
COPY . .
CMD [ "npm", "start" ]
