# SmartLMS Production Deployment on Ubuntu VPS

This guide deploys SmartLMS with Docker Compose, Gunicorn, PostgreSQL, WhiteNoise, and an Nginx reverse proxy.

## Architecture

```text
Internet -> Nginx (80/443) -> SmartLMS web (127.0.0.1:8000) -> PostgreSQL (Docker network only)
```

The PostgreSQL container has a named volume. It is not published to the VPS host. The application container runs as a non-root user and uses Gunicorn, not Django `runserver`.

## 1. Install Docker on Ubuntu

Install Docker Engine and the Compose plugin using the official Docker instructions, then verify:

```bash
docker --version
docker compose version
```

## 2. Clone the repository

```bash
git clone <your-repository-url> smartlms_uas
cd smartlms_uas
```

## 3. Create the production environment file

Create `.env` on the VPS. Do not commit it:

```bash
cp .env.example .env
chmod 600 .env
nano .env
```

Set at least these values:

```dotenv
DJANGO_SECRET_KEY=<long-random-secret>
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=app.example.com
DJANGO_CSRF_TRUSTED_ORIGINS=https://app.example.com
DJANGO_SECURE_SSL_REDIRECT=True
DJANGO_SECURE_HSTS_SECONDS=31536000
DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS=True
DJANGO_SECURE_HSTS_PRELOAD=True

POSTGRES_DB=smart_lms
POSTGRES_USER=smart_lms_user
POSTGRES_PASSWORD=<strong-database-password>
POSTGRES_HOST=db
POSTGRES_PORT=5432

RUN_MIGRATIONS=False
RUN_COLLECTSTATIC=True
GUNICORN_WORKERS=3
GUNICORN_TIMEOUT=120
APP_BIND_ADDRESS=127.0.0.1
APP_PORT=8000
```

Use a real random value for `DJANGO_SECRET_KEY`, and a unique strong password for PostgreSQL. Never put either value in Git, the Dockerfile, or README.

## 4. Build and start containers

```bash
docker compose config --quiet
docker compose build
docker compose up -d
```

The web container is bound to `127.0.0.1:8000` for Nginx. PostgreSQL is reachable only by the web container on the internal Compose network.

## 5. Run migrations and collect static files

```bash
docker compose exec web python manage.py migrate --noinput
docker compose exec web python manage.py collectstatic --noinput
```

Do not run `makemigrations` on production unless a reviewed model change is being deployed.

## 6. Create an administrator

```bash
docker compose exec web python manage.py createsuperuser
```

This is optional if an administrator already exists.

## 7. Verify the deployment

```bash
docker compose ps
docker compose logs --tail=100 web
docker compose logs --tail=100 db
curl http://127.0.0.1:8000/health/
```

The health endpoint should return `{"status": "ok"}`. The Compose health status should show both `web` and `db` as healthy.

Run application checks inside the container:

```bash
docker compose exec web python manage.py check --deploy
docker compose exec web python manage.py test
```

## 8. Nginx reverse proxy

Install Nginx and create a site configuration such as `/etc/nginx/sites-available/smartlms`:

```nginx
server {
    listen 80;
    server_name app.example.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
```

Enable and test it:

```bash
sudo ln -s /etc/nginx/sites-available/smartlms /etc/nginx/sites-enabled/smartlms
sudo nginx -t
sudo systemctl reload nginx
```

Replace `app.example.com` with the real domain. Do not put that domain in application source code.

## 9. HTTPS

Point the DNS A record at the VPS, then use Certbot with the Nginx plugin:

```bash
sudo certbot --nginx -d app.example.com
```

After HTTPS is active, keep `DJANGO_CSRF_TRUSTED_ORIGINS` set to the HTTPS origin and leave the secure cookie/redirect settings enabled.

## 10. Updates and restart behavior

```bash
git pull
docker compose build
docker compose up -d
docker compose exec web python manage.py migrate --noinput
docker compose exec web python manage.py collectstatic --noinput
```

Both services use `restart: unless-stopped`, so they restart after crashes and Docker daemon/VPS restarts.

## 11. PostgreSQL backups

Create a compressed logical backup from the database container:

```bash
mkdir -p backups
docker compose exec -T db pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Fc > "backups/smartlms-$(date +%F).dump"
```

The command reads variables from the current shell. For a safer operational script, source the protected `.env` first without printing it. Copy backups to storage outside the VPS, encrypt them, and test restoration regularly:

```bash
cat backups/smartlms-YYYY-MM-DD.dump | docker compose exec -T db pg_restore -U "$POSTGRES_USER" -d "$POSTGRES_DB" --clean --if-exists
```

Never delete `postgres_data` as a troubleshooting shortcut. Removing that volume deletes the database.

## 12. Static and media files

Static files are collected into the image during build and served by WhiteNoise. Uploaded media is stored in the named `media_volume`.

Named volumes survive container replacement, but they are not a substitute for backups. Back up `media_volume` and PostgreSQL separately. For multi-server or highly durable deployments, move media to object storage.

## Useful commands

```bash
docker compose ps
docker compose logs -f web
docker compose logs -f db
docker compose restart web
docker compose down
docker compose exec web python manage.py shell
```

Do not use `docker compose down -v` in production unless you intentionally want to delete database and media volumes.
