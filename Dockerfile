# Première étape: Build
FROM golang:1.18 AS builder

WORKDIR /build

COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o app .

# Deuxième étape: Image finale légère
FROM scratch

# Copier le binaire compilé à la racine
COPY --from=builder /build/app /app
# Copier les fichiers statiques dans /public
COPY --from=builder /build/public /public

EXPOSE 3000

# Lancer l'application 
CMD ["/app"]