import csv
from pathlib import Path

BASE = Path.home() / "replife-backend"
OUT = BASE / "templates" / "microsoft-lists"

OUT.mkdir(parents=True, exist_ok=True)

TEMPLATES = {
    "implementation_day_tracker.csv": [
        "Day / Section",
        "Business Workstream",
        "Commands Completed?",
        "Manual Test Passed Twice?",
        "Dry Run Reviewed?",
        "Git Commit Made?",
        "Microsoft Lists Updated?",
        "Cron/API Enabled?",
        "Notes / Error",
        "Next Safe Step",
    ],
    "automation_scripts.csv": [
        "Script Name",
        "Purpose",
        "Business Workstream",
        "Touches Commerce?",
        "Manual Test Passed?",
        "Dry Run Exists?",
        "Ruff Passed?",
        "py_compile Passed?",
        "Cron Enabled?",
        "Better Stack Heartbeat?",
        "Log Path",
        "Disable Command",
        "Last Reviewed",
    ],
    "content_calendar.csv": [
        "Planned Date",
        "Business Workstream",
        "Platform",
        "Content Type",
        "Topic / Hook",
        "Asset Needed",
        "Draft Status",
        "Approval Status",
        "Approval Stage",
        "Postiz Queue Status",
        "Notes",
    ],
    "replife_show_episodes.csv": [
        "Episode",
        "Theme",
        "Recording Date",
        "Transcript File",
        "Clip Ideas Created?",
        "Website Draft Created?",
        "Social Package Created?",
        "Approval Stage",
        "Postiz Queue Created?",
        "Notes",
    ],
    "shakeum_content_ideas.csv": [
        "Song / Campaign",
        "Theme",
        "Content Angle",
        "Platform",
        "Asset Needed",
        "Outreach Draft Needed?",
        "Approval Status",
        "Approval Stage",
        "Scheduled?",
        "Notes",
    ],
    "product_prompt_drafts.csv": [
        "Theme",
        "Prompt Idea",
        "Design Direction",
        "Business Tie-In",
        "Draft Status",
        "Approval Stage",
        "Human Approved?",
        "Used Outside VPS?",
        "Notes",
    ],
    "website_drafts.csv": [
        "Title",
        "Source Transcript",
        "Business Workstream",
        "Draft File",
        "Matomo Review Notes",
        "Approval Stage",
        "Copied to WordPress Manually?",
        "Published Manually?",
        "Notes",
    ],
    "postiz_schedules.csv": [
        "Scheduling Block",
        "Platform",
        "Integration ID Confirmed?",
        "Queue File",
        "Approved Rows",
        "Approval Stage",
        "Media Uploaded?",
        "Loader Used?",
        "Manual Postiz Verification?",
        "Notes",
    ],
    "social_approval_ladder.csv": [
        "Approval Stage",
        "Meaning",
        "Allowed Next Action",
        "Human Review Required?",
    ],
    "weekly_operations_reviews.csv": [
        "Week Starting",
        "Wins",
        "Best Content",
        "Blocked Items",
        "Failed Jobs",
        "Disk Usage",
        "AI Usage",
        "Postiz Review",
        "Approval Stage Review",
        "Next Week Priorities",
    ],
}

APPROVAL_LADDER_ROWS = [
    [
        "Idea",
        "Raw idea or theme only.",
        "Draft content or assign owner.",
        "Yes",
    ],
    [
        "Drafted",
        "Text, outline, or prompt exists but has not been reviewed.",
        "Review draft and attach media needs.",
        "Yes",
    ],
    [
        "Media Validated",
        "Related media passed filename and media-spec validation.",
        "Build package.",
        "Yes",
    ],
    [
        "Packaged",
        "Platform-specific package exists.",
        "Review caption and settings.",
        "Yes",
    ],
    [
        "Caption Reviewed",
        "Caption and platform notes were reviewed by a human.",
        "Build Postiz queue.",
        "Yes",
    ],
    [
        "Queue Built",
        "approved_postiz_queue.csv row exists.",
        "Lint settings and decide approval.",
        "Yes",
    ],
    [
        "Approved for Postiz",
        "Human approved queue row for scheduling.",
        "Upload media or schedule in Postiz.",
        "Yes",
    ],
    [
        "Uploaded to Postiz",
        "Media was uploaded and queue row has media ID/path.",
        "Preview loader or manually schedule.",
        "Yes",
    ],
    [
        "Scheduled in Postiz",
        "Post is visible in Postiz calendar.",
        "Wait for post or verify scheduled date.",
        "Yes",
    ],
    [
        "Posted / Complete",
        "Post is live or manually marked complete.",
        "Archive output and record results.",
        "Yes",
    ],
    [
        "Archived",
        "Working files were moved to archive/backup location.",
        "Use for reports only.",
        "No",
    ],
]

for filename, columns in TEMPLATES.items():
    path = OUT / filename

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(columns)

        if filename == "social_approval_ladder.csv":
            writer.writerows(APPROVAL_LADDER_ROWS)

    print(f"Created {path}")