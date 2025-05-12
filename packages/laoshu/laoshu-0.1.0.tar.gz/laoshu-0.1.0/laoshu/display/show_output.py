from typing import List, Dict
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax
from laoshu.data import PromptCluster, InputData, FeedbackData, FeedbackItem


def show_output(
    input_data: InputData,
    feedback_data: FeedbackData,
    prompt_clusters: List[PromptCluster],
):
    prompt_clusters = sorted(prompt_clusters, key=lambda x: x.cluster_id)
    console = Console()

    console.print("\n[bold]Prompt Template:[/bold]")
    syntax = Syntax(
        input_data.prompt_template, "jinja2", theme="light", line_numbers=True
    )
    console.print(Panel(syntax))

    feedback_map: Dict[str, FeedbackItem] = {
        item.id: item for item in feedback_data.feedback
    }

    for cluster in prompt_clusters:
        console.print(
            f"\n[bold]Cluster {cluster.cluster_id}:[/bold] {cluster.description}"
        )

        table = Table(show_header=True, header_style="bold")

        table.add_column("Session ID")
        table.add_column("User Input")
        table.add_column("Prompt Output")
        table.add_column("Is Correct")
        table.add_column("Feedback")
        table.add_column("Expected Output")

        for session_id in cluster.session_ids:
            session = next((s for s in input_data.sessions if s.id == session_id), None)
            if not session:
                continue

            feedback = feedback_map.get(session_id)

            table.add_row(
                session_id,
                str(session.user_input),
                session.prompt_output,
                str(feedback.is_correct) if feedback else "",
                feedback.message if feedback else "",
                feedback.expected_output if feedback else "",
            )

        console.print(table)
