# Manooch Server Migration — PRD + Step-by-Step Runbook

> **Goal:** Move the entire `manooch` project (backend + CMS + frontends, with all
> databases, uploaded files, SSL certificates and config) from the OLD server to the
> NEW server with zero data loss and minimal downtime.

---

## 1. PRD (Product Requirements Document)

### 1.1 Objective
Fully migrate the production `manooch` stack from the current (OLD) server to a new
(TARGET) server so that everything runs identically on the target, and the OLD server
can be decommissioned.

### 1.2 Scope

**In scope:**
- Project source/config files (`docker-compose*.yml`, `.env` files)
- PostgreSQL database (all databases)
- WordPress database
- All Docker named volumes (uploads, DB data, Caddy data & config)
- SSL certificates (Caddy data)
- Caddy reverse-proxy configuration
- DNS cutover to the new server IP

**Out of scope:**
- Code changes / feature development
- Infrastructure changes beyond Docker (e.g. changing the reverse proxy)
- Email, firewall, or OS-level hardening beyond Docker installation

### 1.3 Current (OLD) server structure

```
/home/effect/manooch/
├── manooch-backend/
│   ├── docker-compose.yml
│   ├── docker-compose.prod.yml
│   └── .env                    ← 🔑 important
├── manooch-cms/
│   ├── docker-compose.yml
│   ├── docker-compose.prod.yml
│   └── .env                    ← 🔑 important
└── manooch-fronts/
    └── docker-compose.prod.yml
```

### 1.4 Known containers & volumes

| Container | Service |
|-----------|---------|
| `manooch-postgres` | PostgreSQL |
| `manooch-api` | Backend API |
| `manooch-cms` | CMS |
| `manooch-caddy` | Reverse proxy / SSL |

| Volume | Contents |
|--------|----------|
| `manooch-backend_manooch_pg` | PostgreSQL data |
| `manooch-backend_manooch_uploads` | API uploads |
| `manooch-backend_caddy_data` | SSL certificates |
| `manooch-backend_caddy_config` | Caddy config |
| `manooch-cms_manooch_cms_uploads` | CMS uploads |
| `manooch-cms_manooch_wp_db` | WordPress DB |

### 1.5 Success criteria
1. All containers on the NEW server are `Up` and healthy.
2. PostgreSQL and WordPress databases are restored and queryable.
3. All uploaded files are present and accessible.
4. HTTPS works with valid certificates.
5. DNS points to the NEW server IP and sites load normally.
6. OLD server can be turned off without any user impact.

### 1.6 Risks & mitigations
| Risk | Mitigation |
|------|------------|
| Data loss during backup | Do a full `pg_dumpall` AND volume tar backups (belt & suspenders) |
| Downtime during DNS switch | Set a low TTL on DNS records before cutover |
| SSL certificate issues | Restore `caddy_data` volume; let Caddy re-issue if needed |
| Wrong `.env` secrets | Verify `.env` files copied correctly before starting |

---

## 2. Pre-flight (do this BEFORE anything else)

On the OLD server, run these to confirm the environment matches the plan:

```bash
# Confirm who you are and where you are
whoami
pwd
echo $HOME

# Confirm Docker is present
docker --version
docker compose version

# Confirm the project folder exists
ls -la ~/manooch
ls -la ~/manooch/manooch-backend
ls -la ~/manooch/manooch-cms
ls -la ~/manooch/manooch-fronts

# List running containers (check names match the plan)
docker ps -a

# List all volumes (check names match the plan)
docker volume ls

# Check the .env files are present
cat ~/manooch/manooch-backend/.env
cat ~/manooch/manooch-cms/.env
```

> ⚠️ **If any container/volume name differs** from the plan (e.g. the project lives in a
> different folder, or volume names have a different prefix), write the REAL names down
> and substitute them throughout this runbook. Do NOT guess.

---

## 3. STEP 1 — Create Complete Backup (on OLD server)

### 3.1 Create the backup directory

```bash
BACKUP_DIR=~/backups/$(date +%Y%m%d)
mkdir -p $BACKUP_DIR
echo "Backup directory: $BACKUP_DIR"
```

> Save the printed directory name — you will need the date part later on the NEW server.

### 3.2 Backup project files (compose + .env)

```bash
cp -r ~/manooch $BACKUP_DIR/manooch-project
ls -la $BACKUP_DIR/manooch-project/
```

### 3.3 Backup PostgreSQL (all databases)

```bash
docker exec manooch-postgres \
    pg_dumpall -U postgres \
    > $BACKUP_DIR/postgres-full-backup.sql

# Verify the dump is valid (should start with -- PostgreSQL...)
ls -lh $BACKUP_DIR/postgres-full-backup.sql
head -3 $BACKUP_DIR/postgres-full-backup.sql
```

### 3.4 Backup all Docker volumes

Run the following blocks one at a time. Each uses a temporary `alpine` container to
tar the volume's contents into the backup directory.

```bash
echo "Backing up PostgreSQL volume..."
docker run --rm \
    -v manooch-backend_manooch_pg:/data \
    -v $BACKUP_DIR:/backup \
    alpine tar czf /backup/vol-pg.tar.gz /data
ls -lh $BACKUP_DIR/vol-pg.tar.gz

echo "Backing up API uploads..."
docker run --rm \
    -v manooch-backend_manooch_uploads:/data \
    -v $BACKUP_DIR:/backup \
    alpine tar czf /backup/vol-api-uploads.tar.gz /data
ls -lh $BACKUP_DIR/vol-api-uploads.tar.gz

echo "Backing up CMS uploads..."
docker run --rm \
    -v manooch-cms_manooch_cms_uploads:/data \
    -v $BACKUP_DIR:/backup \
    alpine tar czf /backup/vol-cms-uploads.tar.gz /data
ls -lh $BACKUP_DIR/vol-cms-uploads.tar.gz

echo "Backing up WordPress DB volume..."
docker run --rm \
    -v manooch-cms_manooch_wp_db:/data \
    -v $BACKUP_DIR:/backup \
    alpine tar czf /backup/vol-wp-db.tar.gz /data
ls -lh $BACKUP_DIR/vol-wp-db.tar.gz

echo "Backing up Caddy SSL certificates..."
docker run --rm \
    -v manooch-backend_caddy_data:/data \
    -v $BACKUP_DIR:/backup \
    alpine tar czf /backup/vol-caddy-data.tar.gz /data
ls -lh $BACKUP_DIR/vol-caddy-data.tar.gz

echo "Backing up Caddy config..."
docker run --rm \
    -v manooch-backend_caddy_config:/data \
    -v $BACKUP_DIR:/backup \
    alpine tar czf /backup/vol-caddy-config.tar.gz /data
ls -lh $BACKUP_DIR/vol-caddy-config.tar.gz
```

### 3.5 Verify the full backup

```bash
echo "Final backup contents:"
ls -lh $BACKUP_DIR/
du -sh $BACKUP_DIR/
```

You should see:
- `manooch-project/` (folder)
- `postgres-full-backup.sql`
- `vol-pg.tar.gz`, `vol-api-uploads.tar.gz`, `vol-cms-uploads.tar.gz`,
  `vol-wp-db.tar.gz`, `vol-caddy-data.tar.gz`, `vol-caddy-config.tar.gz`

---

## 4. STEP 2 — Transfer backup to the NEW server

Run on the OLD server. Replace `NEW_SERVER_IP` with the actual IP, and `effect` with
the username on the NEW server if it differs.

```bash
rsync -avz --progress \
    ~/backups/ \
    effect@NEW_SERVER_IP:~/backups/
```

If `rsync` is not available, use `scp`:

```bash
scp -r ~/backups/ effect@NEW_SERVER_IP:~/backups/
```

> Tip: for very large volumes this may take a while. Run inside `screen` or `tmux`
> so the transfer isn't interrupted if your SSH session drops.

---

## 5. STEP 3 — Restore on the NEW server

> All commands in this section run **on the NEW server**.

### 5.1 Install Docker

```bash
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER
# Log out and back in (or use the next line to refresh group without re-login)
newgrp docker
docker --version
docker compose version
```

### 5.2 Restore project files

```bash
BACKUP_DATE=YYYYMMDD          # ← replace with your actual backup date (e.g. 20260816)
BACKUP_DIR=~/backups/$BACKUP_DATE

mkdir -p ~/manooch
cp -r $BACKUP_DIR/manooch-project/* ~/manooch/

# Verify
ls ~/manooch/
cat ~/manooch/manooch-backend/.env
cat ~/manooch/manooch-cms/.env
```

### 5.3 Create the volumes

```bash
docker volume create manooch-backend_manooch_pg
docker volume create manooch-backend_manooch_uploads
docker volume create manooch-backend_caddy_data
docker volume create manooch-backend_caddy_config
docker volume create manooch-cms_manooch_cms_uploads
docker volume create manooch-cms_manooch_wp_db

docker volume ls
```

### 5.4 Restore each volume

```bash
echo "Restoring PostgreSQL volume..."
docker run --rm \
    -v manooch-backend_manooch_pg:/data \
    -v $BACKUP_DIR:/backup \
    alpine tar xzf /backup/vol-pg.tar.gz -C /

echo "Restoring API uploads..."
docker run --rm \
    -v manooch-backend_manooch_uploads:/data \
    -v $BACKUP_DIR:/backup \
    alpine tar xzf /backup/vol-api-uploads.tar.gz -C /

echo "Restoring CMS uploads..."
docker run --rm \
    -v manooch-cms_manooch_cms_uploads:/data \
    -v $BACKUP_DIR:/backup \
    alpine tar xzf /backup/vol-cms-uploads.tar.gz -C /

echo "Restoring WordPress DB..."
docker run --rm \
    -v manooch-cms_manooch_wp_db:/data \
    -v $BACKUP_DIR:/backup \
    alpine tar xzf /backup/vol-wp-db.tar.gz -C /

echo "Restoring Caddy SSL certs..."
docker run --rm \
    -v manooch-backend_caddy_data:/data \
    -v $BACKUP_DIR:/backup \
    alpine tar xzf /backup/vol-caddy-data.tar.gz -C /

echo "Restoring Caddy config..."
docker run --rm \
    -v manooch-backend_caddy_config:/data \
    -v $BACKUP_DIR:/backup \
    alpine tar xzf /backup/vol-caddy-config.tar.gz -C /

echo "All volumes restored!"
```

> Note: the tars were created with absolute path `/data/...`, which is why we extract
> with `-C /` — the contents land back inside each volume's mount correctly.

### 5.5 Start all services (order matters)

```bash
# 1) Backend first (postgres + api + caddy)
cd ~/manooch/manooch-backend
docker compose -f docker-compose.prod.yml up -d

# Wait for postgres to become healthy
echo "Waiting for PostgreSQL..."
sleep 15
docker ps | grep postgres

# 2) CMS
cd ~/manooch/manooch-cms
docker compose -f docker-compose.prod.yml up -d

# 3) Frontends
cd ~/manooch/manooch-fronts
docker compose -f docker-compose.prod.yml up -d

# 4) Check everything
docker ps -a
```

> If any compose file name differs (e.g. only `docker-compose.yml` exists), use that
> file name instead.

---

## 6. STEP 4 — Verify everything works (on NEW server)

```bash
# All containers should be "Up"
docker ps

# Check logs for errors
docker logs manooch-postgres --tail=20
docker logs manooch-api --tail=20
docker logs manooch-cms --tail=20
docker logs manooch-caddy --tail=20

# Check networks
docker network ls
docker network inspect manooch_net
```

Also verify from a browser (or `curl`) using the NEW server's IP before switching DNS:

```bash
curl -I http://NEW_SERVER_IP
curl -k -I https://NEW_SERVER_IP
```

---

## 7. STEP 5 — DNS cutover

1. In your DNS provider, lower the TTL on the domain's A record(s) to ~300 seconds a
   few hours (ideally a day) before cutover.
2. Update the A record to point at the NEW server IP.
3. Wait for propagation (use `dig example.com` / `getent hosts`).
4. Confirm the live site loads over HTTPS.
5. Watch logs for a few minutes to catch any final issues.

```bash
dig +short yourdomain.com
curl -I https://yourdomain.com
```

---

## 8. Rollback plan (if anything goes wrong)

- **Before cutover:** nothing changed on the OLD server — just keep it running.
- **After cutover, if the NEW server fails:** point the DNS A record back at the OLD
  server IP. The OLD server is still intact and will resume serving immediately.
- Only shut down / decommission the OLD server **after** the NEW server has run
  correctly for a set period (e.g. 24–48 hours) with DNS fully switched.

---

## 9. Complete checklist

```
OLD SERVER
[ ] Pre-flight checks (containers + volumes + .env names confirmed)
[ ] mkdir backup dir
[ ] cp -r ~/manooch -> backup
[ ] pg_dumpall from postgres container
[ ] Backup all 6 volumes (tar.gz)
[ ] Verify backup contents
[ ] rsync/scp backups -> NEW server

NEW SERVER
[ ] Install Docker + docker compose
[ ] Restore project files + verify .env
[ ] Create 6 volumes
[ ] Restore all 6 volumes
[ ] docker compose up -d (backend -> cms -> fronts)
[ ] Verify all containers Up + logs clean
[ ] Test with NEW server IP (http/https)

DNS
[ ] Lower TTL
[ ] Update A record to NEW IP
[ ] Verify propagation + live site over HTTPS
[ ] Monitor logs
[ ] Decommission OLD server after 24-48h stable
```

---

## 10. Quick-start (run this first on the OLD server)

```bash
BACKUP_DIR=~/backups/$(date +%Y%m%d)
mkdir -p $BACKUP_DIR
cp -r ~/manooch $BACKUP_DIR/manooch-project
docker exec manooch-postgres pg_dumpall -U postgres > $BACKUP_DIR/postgres-full-backup.sql
ls -lh $BACKUP_DIR/
```

Paste the output back and continue with the volume backups in **Section 3.4**.
