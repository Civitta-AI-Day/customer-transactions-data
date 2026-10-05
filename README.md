# transactions-service

A small Django REST API for the **AI Day backend workshop**. Everything runs on your laptop:
SQLite database, fake data, no external services.

## Run it locally

You need **Python 3.11 or newer** and `make` (included on macOS and Linux).

```bash
make setup   # virtualenv, dependencies, .env, database (about 1 minute)
make seed    # fake data: 3 users, 300 customers, 200,000 transactions (about 15 seconds)
make run     # API on http://127.0.0.1:8000
```

Try it in another terminal:

```bash
curl -H "Authorization: Token alice-token" http://127.0.0.1:8000/api/customers/
```

Other commands: `make test`, `make lint`, `make format`, `make reset` (fresh database).

<details>
<summary>Without make (Windows)</summary>

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py seed
python manage.py runserver
```
</details>

## Users

| User | Token | Sees |
| --- | --- | --- |
| alice | `alice-token` | Her customers (even ids), including #1 Acme Logistics with about 60,000 transactions |
| bob | `bob-token` | His customers (odd ids) |
| carol | `carol-token` | Everything (staff) |

Password for all three: `workshop`.

## API

| Method | Path | What it returns |
| --- | --- | --- |
| GET | `/api/customers/` | Customers you may see. Filters: `q`, `country` |
| GET | `/api/customers/{id}/` | One customer |
| GET | `/api/customers/{id}/transactions/` | Paginated transactions, newest first. Filter: `status` |

Authentication: `Authorization: Token <token>` header.

## Project layout

```
config/            settings and root URLs
apps/core/         pagination, money helpers, seed command
apps/customers/    Customer model, permissions, list and detail endpoints
apps/transactions/ Transaction model, list endpoint
apps/audit/        AuditLog model and the record() service
tests/             pytest tests
TICKET.md          the workshop ticket (CIV-5)
```

## The workshop task

The ticket is CIV-5 in Linear (a copy is in `TICKET.md`). Implement it with Claude Code and the
team's toolkit plugin, which lives in its own repo, **ai-toolkit**, and works in any project.

1. Clone both repos side by side and set this project up (`make setup && make seed`).
2. Start Claude Code in this project: `cd customer-transactions-data && claude`
3. Install the toolkit from your ai-toolkit clone:

   ```
   /plugin marketplace add ~/Desktop/code/ai-toolkit
   /plugin install backend-toolkit@ai-toolkit
   ```

   Restart Claude Code, then check `/agents`, `/hooks` and `/mcp`. Once the plugin has its Linear server,
   pick `linear` in `/mcp` and sign in to Linear (once; the browser opens).
   When the plugin changes in your ai-toolkit clone, run `/reload-plugins`.
4. If there is no CLAUDE.md yet, ask: "Onboard this project." Review what it writes.
5. Work on your own branch: "Implement Linear ticket CIV-5."

To compare with plain Claude Code: `/plugin disable backend-toolkit@ai-toolkit`
(and `/plugin enable ...` to turn it back on).
