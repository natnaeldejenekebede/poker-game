# Use an official Node runtime as the base image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json (or yarn.lock)
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the NextJS app
RUN npm run build

# Expose port 3000 for the NextJS app
EXPOSE 3000

# Start the app
CMD ["npm", "start"]