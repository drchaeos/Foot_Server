FROM node:16

# Create app directory
WORKDIR /app
ADD . /app/

# global install & update
RUN yarn
RUN yarn build

EXPOSE 9999

# set app serving to permissive / assigned
ENV NUXT_HOST=0.0.0.0

# set app port
ENV NUXT_PORT=9999

# start command
CMD [ "yarn", "start" ]
