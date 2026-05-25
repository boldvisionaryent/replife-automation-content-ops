# Environment Variable Index

Use `templates/env/master.env.example` as the master map of possible
values. Each service still keeps its own private `.env` file inside its
service folder.

## Rules
1. Never commit real `.env` files.
2. Never paste real tokens into markdown documents.
3. Never create WordPress, WooCommerce, Gelato, Stripe, payment, order,
customer, shipping, refund, coupon, tax, checkout, or fulfillment
variables on the VPS.
4. Keep `POSTIZ_API_ENABLED=no` unless a supervised optional loader
session is happening.
5. Replace `/root` with the real home path printed by `echo
$HOME`.
6. Recheck this file monthly before the first weekly queue build.

## Service ownership
- Matomo variables support public content analytics only.
- Postiz variables support approved social scheduling only.
- GitHub Models variables support repeatable text drafting and reports.
- Better Stack variables support monitored scheduled jobs.
- OneDrive/restic variables support archive and backup only.
- Product Prompting variables keep Product Prompting as draft support
unless manually approved for public social.