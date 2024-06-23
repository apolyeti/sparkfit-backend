FROM node:20

# Create app directory
WORKDIR /usr/src/app

# Copy app source code
COPY . .

# Install app dependencies
RUN npm install --production

# Expose the port the app runs in
RUN npm run build

CMD ["npm", "run"]
