FROM node:14
WORKDIR /usr/src/app
COPY package.json package*.json ./
RUN npm ci --only=production
COPY . .
CMD [ "npm", "start" ]
