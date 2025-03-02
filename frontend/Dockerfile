# Use Node.js base image
FROM node:16

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json (if present)
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the app files
COPY . .

# Create the necessary directories and fix permissions
# This needs to happen AFTER copying all files
RUN mkdir -p /app/.npm && \
    mkdir -p /app/node_modules/.cache && \
    chown -R node:node /app && \
    chmod -R 777 /app/node_modules/.cache

# Switch to the node user
USER node

# Expose port 8080
EXPOSE 8080

# Start the development server
CMD ["npm", "run", "dev"]