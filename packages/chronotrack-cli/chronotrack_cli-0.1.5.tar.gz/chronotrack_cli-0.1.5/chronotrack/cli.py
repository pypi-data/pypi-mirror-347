import typer
from chronotrack.tracker import (
    start_session, stop_session, log_sessions,
    export_data, tags_view, week_log, resume_session, pause_session
)

app = typer.Typer(help="🕒 ChronoTrack — A simple CLI-based time tracker for developers and creators.")

# ---------------------------- Commands ----------------------------

@app.command()
def start(
    task: str = typer.Argument(..., help="Task name or description (in quotes if multi-word)"),
    tag: str = typer.Argument("General", help="Tag to categorize the task (default: General)")
):
    """
    🟢 Start tracking a new task.
    """
    start_session(task, tag)


@app.command()
def stop():
    """
    🔴 Stop the most recent active task.
    """
    stop_session()


@app.command()
def log(
    time_range: str = typer.Argument("today", help="Time window: today, yesterday, week, or all")
):
    """
    📜 Show a log of tracked tasks.
    """
    log_sessions(time_range)


@app.command()
def export(
    format: str = typer.Argument("json", help="Export format: json or csv")
):
    """
    💾 Export your task log to a file.
    """
    export_data(format)


@app.command()
def tags(
    tag_filter: str = typer.Argument(None, help="(Optional) View stats for a specific tag only")
):
    """
    🏷️  View tag-based summaries.
    """
    tags_view(tag_filter)


@app.command()
def week():
    """
    📊 View a 7-day summary of your work.
    """
    week_log()



@app.command()
def pause():
    """⏸️  Pause the active task to take a break."""
    pause_session()




@app.command()
def play():
    """▶️  Resume the task after a break."""
    resume_session()





# ------------------------------------------------------------------

if __name__ == "__main__":
    app()
