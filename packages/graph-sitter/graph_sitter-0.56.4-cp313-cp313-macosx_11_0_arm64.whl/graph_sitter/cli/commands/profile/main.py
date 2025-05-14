import rich
import rich_click as click
from rich import box
from rich.panel import Panel

from graph_sitter.cli.auth.decorators import requires_auth
from graph_sitter.cli.auth.session import CodegenSession
from graph_sitter.cli.workspace.decorators import requires_init


@click.command(name="profile")
@requires_auth
@requires_init
def profile_command(session: CodegenSession):
    """Display information about the currently authenticated user."""
    repo_config = session.config.repository
    rich.print(
        Panel(
            f"[cyan]Name:[/cyan]  {repo_config.user_name}\n[cyan]Email:[/cyan] {repo_config.user_email}\n[cyan]Repo:[/cyan]  {repo_config.repo_name}",
            title="🔑 [bold]Current Profile[/bold]",
            border_style="cyan",
            box=box.ROUNDED,
            padding=(1, 2),
        )
    )
