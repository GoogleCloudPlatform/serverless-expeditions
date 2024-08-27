ARG NODE_VERSION=20.12.0

# Builds a 1120 MB image
# FROM node:${NODE_VERSION}

# Builds a 225 MB image
# FROM node:${NODE_VERSION}-slim

# Builds a 159 MB image
FROM node:${NODE_VERSION}-alpine

# Use production node environment by default.
ENV NODE_ENV production

WORKDIR /app

RUN chown node:node ./

# Run the application as a non-root user.
USER node

# Copy the rest of the source files into the image.
COPY . .

# Expose the port that the application listens on.
EXPOSE 8080

# RUN npm ci --omit=dev && npm cache clean
RUN npm ci --omit=dev

# Run the application.
CMD ["node", "./bin/www"]
