import csv
from pathlib import Path

base = Path.home() / "replife-backend"
out = base / "templates" / "account-access"
out.mkdir(parents=True, exist_ok=True)

rows = [
    ["Microsoft Lists", "Operations tracking", "Required", "", "", ""],
    ["GitHub", "Version control", "Required", "", "", ""],
    ["LobeHub", "Manual AI workspace", "Required", "", "", ""],
    ["GitHub Models", "Script AI provider", "Required", "", "", ""],
    ["Postiz", "Approved social scheduling", "Required", "", "", ""],
    ["Matomo", "Public content analytics", "Required", "", "", ""],
    ["Better Stack", "External monitoring and heartbeats", "Required", "", "", ""],
    ["Uptime Kuma", "Internal monitoring", "Required", "", "", ""],
    ["OneDrive", "Archive and backup target", "Required", "", "", ""],
    ["Facebook", "Social channel", "Required", "", "", ""],
    ["Instagram", "Social channel", "Required", "", "", ""],
    ["YouTube", "Social channel", "Required", "", "", ""],
    ["TikTok", "Social channel", "Required", "", "", ""],
    ["LinkedIn", "Optional social channel", "Optional", "", "", ""],
    ["X", "Optional social channel", "Optional", "", "", ""],
    ["Reddit", "Optional social channel", "Optional", "", "", ""],
    ["Medium", "Optional social channel", "Optional", "", "", ""],
]

path = out / "account_access_confirmation.csv"

with path.open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "Account",
        "VPS Purpose",
        "Required or Optional",
        "Login Confirmed",
        "Connected in Tool",
        "Notes",
    ])
    writer.writerows(rows)

print(path)