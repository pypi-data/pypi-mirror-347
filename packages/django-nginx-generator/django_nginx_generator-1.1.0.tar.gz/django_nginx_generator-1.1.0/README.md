
[![PyPI version](https://img.shields.io/pypi/v/django-nginx-generator)](https://pypi.org/project/django-nginx-generator/)  
[![License](https://img.shields.io/pypi/l/django-nginx-generator)](LICENSE)  
[![Python Versions](https://img.shields.io/pypi/pyversions/django-nginx-generator)](https://pypi.org/project/django-nginx-generator/)  

A CLI tool to auto-generate production-grade Nginx configurations for Django projects—featuring SSL/TLS hardening, Brotli/Gzip compression, proxy caching, observability, and Django-aware location blocks.

---

## Table of Contents

- [Features](#features)  
- [Installation](#installation)  
- [Usage](#usage)  
- [Options](#options)  
- [Example](#example)  
- [Contributing](#contributing)  
- [License](#license)  

---

## Features

- **Project Discovery**: Automatically locates your Django project root by finding `manage.py`.  
- **Django-Aware URLs**: Reads `STATIC_URL`, `MEDIA_URL`, `FORCE_SCRIPT_NAME`, and `USE_X_FORWARDED_HOST` to generate accurate `location` blocks.  
- **Global Tuning**: Includes `worker_processes auto;`, `sendfile on;`, `tcp_nopush on;`, `tcp_nodelay on;`, and `use epoll` for high concurrency.  
- **SSL/TLS Hardening**: Supports OCSP stapling, session caching, strong ECC ciphers, and HSTS, with optional Let’s Encrypt ACME hooks.  
- **Caching & Compression**: Implements multi-level proxy caching and Brotli + Gzip compression for static and dynamic content.  
- **Observability**: Exposes `stub_status` for Prometheus, custom `log_format`, and syslog integration.  
- **Security Headers & Rate-Limiting**: Adds `X-Frame-Options`, `Content-Security-Policy`, and rate-limits (`limit_req_zone`) to mitigate abuse.  
- **Specialized Blocks**: Auto-generates `location` for `/static/`, `/media/`, `/admin/`, `/api/`, `/ws/`, and health-check endpoints.  

---

## Installation

Install from PyPI for immediate use:

```bash
pip install django-nginx-generator
````

This command installs the tool and its dependencies (`click`, `jinja2`, `Django`) into your active environment.

---

## Usage

Run `generate_nginx` anywhere—project root is auto-discovered, or override with `--project-root`.

```bash
generate_nginx \
  --ssl-cert /etc/letsencrypt/live/example.com/fullchain.pem \
  --ssl-key  /etc/letsencrypt/live/example.com/privkey.pem \
  --http2 \
  --enable-certbot \
  --socket-path /run/gunicorn.sock \
  --output /etc/nginx/sites-available/example.com.conf
```

Use `generate_nginx --help` to view all options and examples.

---

## Options

| Flag                                     | Required | Default                       | Description                                                     |
| ---------------------------------------- | -------- | ----------------------------- | --------------------------------------------------------------- |
| `--project-root PATH`                    | no       | auto-discover                 | Directory containing `manage.py`.                               |
| `--ssl-cert PATH`                        | no       | none                          | SSL certificate file (`fullchain.pem`).                         |
| `--ssl-key PATH`                         | no       | none                          | SSL private key file (`privkey.pem`).                           |
| `--http2 / --no-http2`                   | no       | `--no-http2`                  | Enable HTTP/2 on port 443.                                      |
| `--enable-certbot / --no-enable-certbot` | no       | `--no-enable-certbot`         | Include ACME challenge block for Let’s Encrypt.                 |
| `--socket-path PATH`                     | no       | fall back to `127.0.0.1:8000` | Unix socket for Gunicorn/Uvicorn or TCP address for dev server. |
| `--force-https-when-no-ssl / --no-force` | no       | `--no-force`                  | Redirect HTTP→HTTPS even without certs (useful in staging).     |
| `--output PATH`                          | no       | `./<project>_nginx.conf`      | Path to write the generated Nginx configuration.                |

---

## Example

Below is an excerpt from a generated config for `example.com` (static files served from `/srv/myproject/static`):

```nginx
server {
    listen 80;
    server_name example.com www.example.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name example.com www.example.com;

    ssl_certificate     /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    ssl_protocols       TLSv1.2 TLSv1.3;
    ssl_ciphers         'ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
    ssl_stapling        on;
    add_header Strict-Transport-Security "max-age=31536000; preload" always;

    location /static/ {
        alias /srv/myproject/static;
        try_files $uri =404;
        expires 365d;
        add_header Cache-Control "public, max-age=31536000, immutable";
    }

    location / {
        proxy_pass http://django;
        include proxy_params;
    }
}
```

This config demonstrates HTTP→HTTPS redirect, SSL/TLS hardening, immutable caching for static assets, and proxying to your Django backend.

---

## Contributing

Contributions are welcome! Please:

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/x`)
3. Commit your changes (`git commit -m "Add feature"`)
4. Push to your branch (`git push origin feature/x`)
5. Open a Pull Request

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for more details.

---

## License

This project is licensed under the **MIT License** – see [LICENSE](LICENSE) for details.
