FROM node:slim

# Create the application directory
RUN mkdir /app_users

# Create the working environment
RUN mkdir -p /app_users/src /app_users/config
WORKDIR "/app_users"

# Deploy code
COPY package*.json /app_users/
COPY src/* /app_users/src/

RUN npm install
CMD [ "npm", "start" ]
