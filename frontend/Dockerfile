# frontend/Dockerfile

# Use a Node.js base image
FROM node:18-alpine

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Expose the port that the app runs on
EXPOSE 5173 3000

# Start the application
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]