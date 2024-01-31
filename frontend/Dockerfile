FROM node:18-alpine as build-stage

# make the 'app' folder the current working directory
WORKDIR /app

# copy both 'package.json' and 'package-lock.json' (if available)
COPY package*.json ./

# install project dependencies
RUN npm install

# copy project files and folders to the current working directory (i.e. 'app' folder)
COPY . .

# build app for production with minification
RUN npm run build

CMD [ "npm", "run", "dev" ]

# Nginx
FROM nginx as production-stage
EXPOSE 3000
RUN mkdir /app
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build-stage /app/dist /app