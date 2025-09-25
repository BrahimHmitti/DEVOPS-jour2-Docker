# Première étape: Build
FROM golang:1.18 AS builder

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o guestbook .

# Deuxième étape: Image finale légère
FROM scratch

COPY --from=builder /app/guestbook /app/guestbook
# Copier les fichiers statiques depuis public au lieu de ui
COPY --from=builder /app/public /app/public

WORKDIR /app
EXPOSE 3000

CMD ["/app/guestbook"]