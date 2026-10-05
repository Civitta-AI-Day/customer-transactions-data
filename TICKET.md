# CIV-5: Export a customer's transactions as CSV

Linear: https://linear.app/civitta-ai-day/issue/CIV-5/export-a-customers-transactions-as-csv

## What

Account managers need to download a customer's transactions as a CSV file for reconciliation.

Add `GET /api/customers/{customer_id}/transactions/export/`.

## Requirements

- **Filters:** `from` and `to` dates (both required, `YYYY-MM-DD`, `to` not before `from`, at most 366 days apart) and an optional `status` (`completed`, `pending`, `failed`).
- **CSV columns, in this order:** `id`, `date`, `type`, `amount`, `currency`, `status`, `reference`.
  - `date` is the transaction's `created_at` as an ISO 8601 UTC timestamp.
  - `amount` comes from `amount_cents`, formatted with exactly 2 decimals (for example `-2.50`).
- **Large exports:** some customers have tens of thousands of transactions. Stream the response and read rows from the database in chunks of 1,000. Do not load everything into memory.
- **Access:** only users allowed to view the customer may export. Use the existing customer permission.
- **Audit:** write an audit log entry for every successful export: user, customer, filters and row count.
- **Rate limit:** at most 5 exports per minute per user.
- **Response:** `Content-Type: text/csv`, downloaded as `customer-{id}-transactions-{from}-{to}.csv`.

## Tests

Feature tests for at least: a successful export, a user without access, invalid dates, and an empty result.

## Out of scope

Excel format, emailing the file, background jobs.
