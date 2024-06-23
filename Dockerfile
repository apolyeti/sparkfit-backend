FROM node:20

# Create app directory
WORKDIR /usr/src/app

# Copy app source code
COPY app .

# Install app dependencies
RUN npm install --production --ignore-scripts --lockfile-version 3 --package-lock-only

# Expose the port the app runs in
RUN npm run build

CMD ["npm", "start"]
