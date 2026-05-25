import csv
from pathlib import Path


base = Path.home() / "replife-backend"
out = base / "templates" / "business-workflow"

out.mkdir(parents=True, exist_ok=True)

rows = [
    [
        "1",
        "RepLife Show",
        "Choose monthly theme",
        "Human",
        "Theme approved",
    ],
    [
        "2",
        "SHAKEUM",
        "Choose campaign/song tie-in",
        "Human + script support",
        "Campaign selected",
    ],
    [
        "3",
        "Product Prompting",
        "Generate internal creative concepts",
        "Python/LobeHub",
        "Draft concepts reviewed",
    ],
    [
        "4",
        "RepLife/SHAKEUM",
        "Validate approved media",
        "Python",
        "Media Validated",
    ],
    [
        "5",
        "RepLife/SHAKEUM",
        "Transcribe approved media",
        "Python faster-whisper",
        "Transcript created",
    ],
    [
        "6",
        "RepLife Show",
        "Create website draft",
        "Python",
        "Draft reviewed manually",
    ],
    [
        "7",
        "Social Media",
        "Build platform packages",
        "Python",
        "Packaged",
    ],
    [
        "8",
        "Social Media",
        "Lint captions and settings",
        "Python",
        "Caption Reviewed",
    ],
    [
        "9",
        "Social Media",
        "Build Postiz queue",
        "Python",
        "Queue Built",
    ],
    [
        "10",
        "Social Media",
        "Approve and schedule",
        "Human + Postiz",
        "Scheduled in Postiz",
    ],
    [
        "11",
        "Operations",
        "Review metrics and archive",
        "Python + OneDrive",
        "Archived",
    ],
]

path = out / "monthly_business_workflow.csv"

with path.open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    writer.writerow(
        [
            "Order",
            "Business Workstream",
            "Task",
            "System Used",
            "Completion Signal",
        ]
    )

    writer.writerows(rows)

print(path)