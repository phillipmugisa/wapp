# Dockerfile for Node.js app

# Use the official Node.js image as the base image
FROM node:18

# Set environment variable
# ENV NODE_ENV=production

# Create and set the working directory
WORKDIR /code

# Install dependencies
COPY ./code/package.json .
COPY ./code/package-lock.json . 
RUN npm install 

# Copy the Node.js code files to the container
COPY ./code .
EXPOSE 3000

# Start the Node.js app
# CMD ["node", "server.js"]
