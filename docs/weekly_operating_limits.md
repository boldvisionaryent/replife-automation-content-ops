Use these limits for the first year unless a future written upgrade plan changes them.

## Weekly content limits
- 1 RepLife Show weekly content package.
- 1 SHAKEUM weekly content package.
- 1 Product Prompting concept batch.
- 1 website draft batch.
- 1 active approved_postiz_queue.csv.
- 6 maximum rows per optional Postiz loader run.
- 6 maximum upload_ready= yes media rows at one time.
- 0 unsent approved rows allowed before creating a new weekly queue unless the previous queue is intentionally archived.

## Stop conditions
Stop new packaging if disk usage is high, capacity_backlog_report.py warns, Postiz platform connections are missing, the previous queue still has unsent approved rows, or the Postiz API smoke test fails.