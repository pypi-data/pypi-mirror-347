#!/usr/bin/env python3
import os
import re
import sys
import click
from pathlib import Path
from jinja2 import Environment, DictLoader, select_autoescape

def discover_project_root(start_path=None):
    path = Path(start_path or os.getcwd()).resolve()
    for parent in [path] + list(path.parents):
        if (parent / 'manage.py').is_file():
            return str(parent)
    return None

def find_project_name(root):
    manage = Path(root) / 'manage.py'
    pattern = re.compile(r"DJANGO_SETTINGS_MODULE\s*=\s*['\"]([\w\.]+)['\"]")
    for line in manage.read_text(encoding='utf-8').splitlines():
        m = pattern.search(line)
        if m:
            return m.group(1).rsplit('.', 1)[0]
    candidates = [d.name for d in Path(root).iterdir() if d.is_dir() and (d/'settings.py').is_file()]
    if len(candidates) == 1:
        return candidates[0]
    if candidates:
        click.echo(f"[WARN] Multiple candidates for settings.py: {candidates}. Using '{candidates[0]}'", err=True)
        return candidates[0]
    raise RuntimeError("Could not determine project name (no DJANGO_SETTINGS_MODULE or settings.py)")

def sanitize_path(p):
    p = p.replace('\\', '/')
    if ' ' in p:
        return f'"{p}"'
    return p

NGINX_TEMPLATE = r"""
# GLOBAL PERFORMANCE & SECURITY
worker_processes auto;
worker_rlimit_nofile 65535;
error_log /var/log/nginx/error.log warn;
pid /run/nginx.pid;
include /etc/nginx/modules-enabled/*.conf;

events {
    worker_connections 10240;
    multi_accept on;
    use epoll;
}

http {
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65s;
    include /etc/nginx/mime.types;
    default_type application/octet-stream;
    server_tokens off;

    # Upstream
    resolver 127.0.0.11 valid=30s;
    upstream django {
        server {{ backend }};
        keepalive 16;
    }

    # Caching
    proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:50m max_size=10g inactive=60m use_temp_path=off;
    proxy_cache_key "$scheme$request_method$host$request_uri";
    proxy_cache_use_stale error timeout updating;
    proxy_cache_background_update on;
    proxy_cache_lock on;

    # Compression
    brotli on;
    brotli_static on;
    brotli_comp_level 6;
    brotli_types text/plain text/css application/javascript application/json image/svg+xml;
    gzip on;
    gzip_vary on;
    gzip_min_length 256;
    gzip_proxied any;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml text/javascript;

    # Logging
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" "$http_user_agent" '
                    'rt=$request_time urt=$upstream_response_time';
    access_log /var/log/nginx/access.log main;
    access_log syslog:server=unix:/dev/log main;

    # Metrics
    server {
        listen 127.0.0.1:8090;
        allow 127.0.0.1; deny all;
        location /nginx_status { stub_status; access_log off; }
    }

    # Project‐specific servers
    {{ generated_server }}
}
"""

SERVER_BLOCK = r"""
{% if use_ssl %}
# HTTP → HTTPS redirect
server {
    listen 80;
    server_name {{ server_name }};
    return 301 https://$host$request_uri;
}

# HTTPS server
server {
    listen 443 ssl{% if http2 %} http2{% endif %};
    server_name {{ server_name }};

    ssl_certificate     {{ ssl_cert }};
    ssl_certificate_key {{ ssl_key }};
    ssl_protocols       TLSv1.2 TLSv1.3;
    ssl_ciphers         'ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
    ssl_prefer_server_ciphers on;
    ssl_session_cache   shared:SSL:10m;
    ssl_session_timeout 24h;
    ssl_session_tickets off;
    ssl_stapling        on;
    ssl_stapling_verify on;
    resolver            1.1.1.1 valid=300s;
    resolver_timeout    5s;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
{% else %}
# HTTP server only
server {
    listen 80;
    server_name {{ server_name }};
    {% if force_https_when_no_ssl %}
    return 301 https://$host$request_uri;
    {% endif %}
{% endif %}

    # Security headers
    add_header X-Frame-Options SAMEORIGIN always;
    add_header X-Content-Type-Options nosniff always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; object-src 'none'" always;
    add_header Permissions-Policy "geolocation=(), microphone=()" always;

    # Rate limit
    limit_req_zone $binary_remote_addr zone=one:10m rate=60r/m;
    limit_req zone=one burst=20 nodelay;
    client_max_body_size 50M;
    client_body_timeout 12s;
    client_header_timeout 12s;
    large_client_header_buffers 4 16k;

    # Static
    location {{ static_url }} {
        alias {{ static_root }};
        try_files $uri =404;
        expires 365d;
        add_header Cache-Control "public, max-age=31536000, immutable";
    }

    # Media
    location {{ media_url }} {
        alias {{ media_root }};
        expires 30d;
        add_header Cache-Control "public, max-age=2592000";
    }

    # Admin
    location {{ admin_url }} {
        auth_basic "Admin Area";
        auth_basic_user_file /etc/nginx/.htpasswd;
        proxy_pass http://django;
    }

    # API
    location {{ api_url }} {
        add_header Access-Control-Allow-Origin "*";
        proxy_pass http://django;
        proxy_cache my_cache;
        proxy_cache_valid 200 10s;
    }

    # WebSockets
    location {{ ws_url }} {
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_pass http://django;
    }

    # Health
    location = /healthz/ {
        allow 127.0.0.1; deny all;
        proxy_pass http://django/healthz/;
        proxy_cache my_cache;
        proxy_cache_valid 200 5s;
    }

    # Error pages
    error_page 404 /404.html;
    location = /404.html { root {{ web_root }}; internal; }
    error_page 500 502 503 504 /50x.html;
    location = /50x.html { root {{ web_root }}; internal; }

    # Fallback
    location / {
        proxy_set_header Host $host;
        {% if use_x_forwarded_host %}proxy_set_header X-Forwarded-Host $host;{% endif %}
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_pass http://django;
    }
}
"""

@click.command()
@click.option('--project-root', default=None, help='Django project root (dir with manage.py).')
@click.option('--ssl-cert',     help='SSL certificate (fullchain.pem).')
@click.option('--ssl-key',      help='SSL key (privkey.pem).')
@click.option('--http2/--no-http2', default=False, help='Enable HTTP/2 on HTTPS.')
@click.option('--enable-certbot/--no-enable-certbot', default=False, help='Add ACME challenge location.')
@click.option('--force-https-when-no-ssl/--no-force', default=False,
              help='Redirect HTTP→HTTPS even if no cert provided.')
@click.option('--socket-path',  help='Unix socket for Gunicorn/Uvicorn (e.g. /run/gunicorn.sock).')
@click.option('--output',       help='Output filepath for the generated config.')
def main(project_root, ssl_cert, ssl_key, http2,
         enable_certbot, force_https_when_no_ssl,
         socket_path, output):

    # 1) Discover project
    root = project_root or discover_project_root()
    if not root:
        click.echo("[ERROR] manage.py not found. Use --project-root.", err=True); sys.exit(1)

    # 2) Infer project name
    try:
        project = find_project_name(root)
    except RuntimeError as e:
        click.echo(f"[ERROR] {e}", err=True); sys.exit(1)

    # 3) Load Django settings
    sys.path.insert(0, root)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{project}.settings')
    try:
        import django; django.setup()
        from django.conf import settings
    except Exception as e:
        click.echo(f"[ERROR] Loading Django settings: {e}", err=True); sys.exit(1)

    # 4) Values from settings
    hosts       = [h for h in settings.ALLOWED_HOSTS if h and h != '0.0.0.0']
    if not hosts:
        hosts = ['localhost']
    server_name = ' '.join(hosts)
    static_url  = settings.STATIC_URL.rstrip('/') + '/'
    media_url   = settings.MEDIA_URL.rstrip('/') + '/'
    admin_url   = (settings.FORCE_SCRIPT_NAME or '') + '/admin/'
    api_url     = (settings.FORCE_SCRIPT_NAME or '') + '/api/'
    ws_url      = (settings.FORCE_SCRIPT_NAME or '') + '/ws/'
    web_root    = root

    # 5) Determine backend
    if socket_path:
        backend = f'unix:{socket_path}'
    else:
        backend = '127.0.0.1:8000'
        click.echo("[WARN] No --socket-path; falling back to 127.0.0.1:8000", err=True)

    # 6) SSL logic
    use_ssl = bool(ssl_cert and ssl_key)
    if use_ssl:
        ssl_cert = ssl_cert
        ssl_key  = ssl_key
    else:
        click.echo("[INFO] No SSL cert/key—HTTP only (or redirect if forced).", err=True)

    # 7) Sanitize file paths
    static_root = sanitize_path(settings.STATIC_ROOT or '/var/www/static/')
    media_root  = sanitize_path(settings.MEDIA_ROOT  or '/var/www/media/')

    # 8) Render templates
    env = Environment(loader=DictLoader({
        'base': NGINX_TEMPLATE,
        'server': SERVER_BLOCK
    }), autoescape=select_autoescape())
    server_block = env.get_template('server').render(
        server_name=server_name, backend=backend,
        static_url=static_url, media_url=media_url,
        static_root=static_root, media_root=media_root,
        admin_url=admin_url, api_url=api_url, ws_url=ws_url,
        web_root=web_root, use_x_forwarded_host=True,
        ssl_cert=ssl_cert, ssl_key=ssl_key,
        http2=http2, enable_certbot=enable_certbot,
        use_ssl=use_ssl, force_https_when_no_ssl=force_https_when_no_ssl
    )
    full_conf = env.get_template('base').render(backend=backend, generated_server=server_block)

    # 9) Output
    out_path = output or f"{project}_nginx.conf"
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(full_conf)
    click.echo(f"[✓] Nginx config generated at {out_path}")

if __name__ == '__main__':
    main()
