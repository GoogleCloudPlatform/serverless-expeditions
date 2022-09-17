FROM node:slim
RUN mkdir /app
WORKDIR "/app"
COPY package*.json /app/
COPY . /app/
RUN npm install
CMD [ "npm", "start" ]
