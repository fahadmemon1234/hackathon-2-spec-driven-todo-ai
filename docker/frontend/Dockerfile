# ---------- Build Stage ----------
FROM node:20-alpine AS builder

WORKDIR /app

# copy package files from frontend folder
COPY frontend/package*.json ./

RUN npm ci

# copy frontend source code
COPY frontend .

# build nextjs app
RUN npm run build


# ---------- Runtime Stage ----------
FROM node:20-alpine

WORKDIR /app

ENV NODE_ENV=production
ENV PORT=3000

# copy build output
COPY --from=builder /app ./

EXPOSE 3000

CMD ["npm", "start"]
