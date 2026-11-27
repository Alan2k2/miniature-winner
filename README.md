# Alan Shaju’s portfolio

React and Vite power the public site. Django serves the same-origin API, production assets, and CMS. Use the existing checkout in each isolated Codex task.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
npm ci --prefix frontend
npm run build --prefix frontend
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open the site at `http://127.0.0.1:8000/` and sign in at `/admin/`. Edit the Profile or add and publish Projects. The admin also lists contact submissions and visits. To develop with hot reload, run `npm run dev --prefix frontend` alongside Django and use the Vite URL. Run backend checks with `python manage.py test`.

## Deploy to Render

1. In Render, create a Blueprint and connect this GitHub repository on `main`. The Blueprint builds the frontend, collects static files, runs migrations, and provisions PostgreSQL. Its starter plans are free. For long-term data storage, select a database plan with suitable retention. Render’s free PostgreSQL instances expire.
2. Set `RESEND_API_KEY` to your Resend API key, `DEFAULT_FROM_EMAIL` to a sender on your verified domain, and `CONTACT_RECIPIENT` to your inbox. For an SMTP deployment, unset `RESEND_API_KEY` and set `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, and `EMAIL_HOST_PASSWORD`; the SMTP provider and hosting plan must support outbound SMTP. Django uses its console email backend during local development. Submissions are retained for review in the CMS if delivery fails.
3. After deploy, create the first admin user with `python manage.py createsuperuser` from a Render shell if available. Alternatively, run that command locally with the database’s external connection URL and restrict external database access afterward. Sign in to `/admin/`, publish content, and submit a contact message to check delivery.
4. To enable location lookup, place a licensed MaxMind GeoLite2 City or GeoIP2 City database at a path readable by the app and set `GEOIP_PATH` to that file. On Render you can provision a persistent disk on a supported plan and store the database there. Restart the service after replacing the database.

The site logs the visitor IP, timestamp, browser user agent, language, referrer hostname, and approximate city, region, and country when a GeoIP database covers the address. Browser privacy signals and the footer’s opt-out prevent future visit logging in that browser. Use the Django admin to manage stored visit data and restrict access to authorized staff. For self-hosting, keep `TRUSTED_PROXY_HOPS` at zero unless the app is exclusively reachable through a trusted proxy chain. Set the hop count based on the entries that chain appends to `X-Forwarded-For`. Verify the recorded address with a real request after changing proxy configuration.
