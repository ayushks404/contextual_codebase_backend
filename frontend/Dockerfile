FROM node:20

WORKDIR /app

COPY frontend/package*.json ./
RUN rm -rf node_modules package-lock.json && npm install

COPY frontend/ ./

EXPOSE 5173

CMD ["npm", "run", "dev"]
