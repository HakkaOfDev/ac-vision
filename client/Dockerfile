FROM node:alpine

RUN mkdir -p /app
ENV PORT 3000

WORKDIR /app

COPY package.json /app

RUN yarn config set network-timeout 1000000 -g
RUN yarn install

COPY . /app

RUN yarn build

EXPOSE 3000
CMD [ "yarn", "start" ]