# Existing n8n Reuse Plan

The VPS already has n8n running. RepLife setup must reuse the existing n8n.

Do not deploy a new n8n Compose stack from this repository. The active n8n Compose file belongs wherever the current VPS n8n was originally installed.

A reference-only n8n Compose example is archived at `docs/reference/n8n-new-install-reference.yml` for future disaster recovery planning. It is not part of the current setup path.

## RepLife Workflow Rules

Inside existing n8n:

1. Create a tag named `RepLife`.
2. Prefix workflow names with `RepLife - `.
3. Use n8n for reminders, checks, and notifications.
4. Keep production code in tested Python scripts.

Allowed nodes:

- Schedule Trigger
- Manual Trigger
- HTTP Request
- IF
- Set/Edit Fields
- notification nodes

Not allowed for RepLife production workflows:

- Code node
- Python Code node
- Execute Command node
- Read/write local file nodes
- heavy loops
- queue mode changes
- external task-runner changes

## Beginner Workflow List

| Workflow | Trigger | Action |
|---|---|---|
| RepLife - Weekly Planning Reminder | Weekly schedule | Remind owner to choose monthly/weekly theme and backlog. |
| RepLife - Postiz Review Reminder | Before publishing window | Remind owner to review queue rows in Postiz. |
| RepLife - Publishing Window Reminder | Scheduled posting window | Remind owner to check live/scheduled posts. |
| RepLife - Backup Review Reminder | Monthly schedule | Remind owner to confirm backup and restore test. |

## Safety Check

After adding workflows, confirm existing non-RepLife workflows are still present and unchanged.
