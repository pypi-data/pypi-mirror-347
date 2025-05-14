from datetime import datetime

def format_pretty_time(iso_str: str) -> str:
    dt = datetime.fromisoformat(iso_str)
    return dt.strftime("%I:%M %p")

def is_active_session(session: dict) -> bool:
    return "start" in session and "end" not in session

def is_paused_session(session: dict) -> bool:
    breaks = session.get("breaks", [])
    return bool(breaks and "end" not in breaks[-1])

def calculate_duration_minutes(start_iso: str, end_iso: str) -> float:
    start = datetime.fromisoformat(start_iso)
    end = datetime.fromisoformat(end_iso)
    return round((end - start).total_seconds() / 60, 2)

def start_break(session: dict):
    now = datetime.now().isoformat()
    if "breaks" not in session:
        session["breaks"] = []
    session["breaks"].append({"start": now})
    session["total_breaks"] = len(session["breaks"])

def end_break(session: dict):
    now = datetime.now().isoformat()
    last_break = session["breaks"][-1]
    last_break["end"] = now
    last_break["duration_minutes"] = calculate_duration_minutes(
        last_break["start"], last_break["end"]
    )
