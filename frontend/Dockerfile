# Use Node.js base image
FROM node:16

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json (if present)
COPY package*.json ./

# Install dependencies
RUN npm install

# Create the necessary directories for npm cache if they do not exist
RUN mkdir -p /app/.npm && \
    mkdir -p /app/node_modules/.cache && \
    chown -R node:node /app && \
    chmod -R 755 /app/node_modules && \
    chmod -R 755 /app/.npm && \
    chmod -R 755 /app/node_modules/.cache

# Switch to the node user
USER node

# Copy the app files
COPY . .

# Expose port 8080
EXPOSE 8080

# Start the development server
CMD ["npm", "run", "dev"]
