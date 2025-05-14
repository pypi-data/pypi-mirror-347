import os
import shutil
import click
import lamini
from importlib import resources
import pathlib
import subprocess
import datetime

base_dir = os.path.dirname(lamini.__file__)

TEMPLATES = sorted(
    [
        p.name
        for p in (resources.files("lamini.project_templates")).iterdir()
        if p.is_dir()
    ]
)


@click.group()
def cli():
    """CLI tool for scaffolding projects."""
    pass


@cli.command("list-templates")
def list_templates():
    """List all available project templates."""
    click.echo("Available templates:")
    for tmpl in TEMPLATES:
        click.echo(f"  • {tmpl}")


@cli.command()
@click.argument("project_type")
@click.argument("workspace_name", required=False, default=None)
def create(project_type, workspace_name=None):
    """
    Create a new project based on the specified template.
    PROJECT_TYPE: Type of project (e.g., 'Q&A', 'text-to-sql')
    WORKSPACE_NAME: Name of the new workspace (optional; defaults to current timestamp if omitted)

    Options:

    - text-to-sql: Use agentic pipelines to generate synthetic data based on examples provided by the user to create a training dataset for text-to-sql. This option also enables the user to tune SLM models, perform inference, and evaluation.

    - Q&A: Use agentic pipelines to generate pairs of questions and answers from a source document, creating training data for tuning SLMs, inference, and evaluation.
    """
    if workspace_name is None:
        workspace_name = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    try:
        # Access template files from package data
        with resources.path("lamini.project_templates", project_type) as template_path:
            template_dir = pathlib.Path(template_path)
            if not template_dir.exists():
                click.echo(
                    f"Template for project type '{project_type}' does not exist."
                )
                return

            target_dir = os.path.join(os.getcwd(), workspace_name)
            if os.path.exists(target_dir):
                click.echo(f"Workspace '{workspace_name}' already exists.")
                return

            shutil.copytree(template_dir, target_dir)
            click.echo(
                f"Workspace '{workspace_name}' created successfully using the '{project_type}' template."
            )
    except ModuleNotFoundError:
        click.echo(f"Template for project type '{project_type}' does not exist.")
        return


@cli.command()
@click.argument("workspace_name", required=False, default=None)
@click.argument("args", nargs=-1)
def run(workspace_name, args):
    """
    Run the CLI app inside the specified workspace.
    WORKSPACE_NAME: Name of the workspace to run.
    Additional ARGS are forwarded to the CLI app.
    """
    if workspace_name is None:
        # Default to current directory as workspace
        workspace_name = os.path.basename(os.getcwd())
        target_dir = os.getcwd()
    else:
        target_dir = os.path.join(os.getcwd(), workspace_name)

    if not os.path.exists(target_dir):
        click.echo(f"Workspace '{workspace_name}' does not exist.")
        return
    script_path = os.path.join(target_dir, "cli-app.py")
    if not os.path.exists(script_path):
        click.echo(f"No 'cli-app.py' found in workspace '{workspace_name}'.")
        return
    result = subprocess.run(["python", script_path] + list(args))
    if result.returncode != 0:
        click.echo(f"'cli-app.py' exited with code {result.returncode}")
    return


@cli.command()
@click.argument("args", nargs=-1)
@click.option("-e", "--experiment-name", help="Name of the experiment to load")
@click.option(
    "-lr", type=float, help="Learning rate for tuning (overrides experiment.yml)"
)
@click.option(
    "-ms",
    "--max-steps",
    type=int,
    help="Max steps for fine tuning (overrides experiment.yml)",
)
def tune(args, experiment_name, lr, max_steps):
    """
    Run a tuning job on the results of a previous experiment.

    Usage:
      lamini tune <project_name> [options...]                # inside your workspace
      lamini tune <workspace> <project_name> [options...]    # point at a different workspace
    """
    # 1) validate and unpack args
    if len(args) == 1:
        workspace = None
        project_name = args[0]
    elif len(args) == 2:
        workspace, project_name = args
    else:
        click.echo(" Usage: lamini tune [WORKSPACE] PROJECT_NAME [options]")
        return

    # 2) figure out the root folder to cd into
    cwd = os.getcwd()
    root_dir = os.path.join(cwd, workspace) if workspace else cwd

    # 3) make sure the YAML files exist under projects/<project_name>/ymls
    yml_dir = os.path.join(root_dir, "projects", project_name, "ymls")
    if not os.path.isdir(yml_dir):
        click.echo(f"Could not find YAMLs at '{yml_dir}'")
        return

    # 4) find the workspace’s own main_scripts/train.py
    script_path = os.path.join(root_dir, "main_scripts", "train.py")
    if not os.path.isfile(script_path):
        click.echo(f"No 'main_scripts/train.py' found in '{root_dir}'")
        return

    # 5) assemble the subprocess invocation
    cmd = ["python", script_path, "--project_name", project_name]
    if experiment_name:
        cmd += ["--experiment_name", experiment_name]
    if lr is not None:
        cmd += ["--lr", str(lr)]
    if max_steps is not None:
        cmd += ["--max_steps", str(max_steps)]

    click.echo(f"Running tuning for project '{project_name}' in '{root_dir}'…")
    result = subprocess.run(cmd, cwd=root_dir)
    if result.returncode != 0:
        click.echo(f"'train.py' exited with code {result.returncode}")



@cli.command()
@click.argument("model_id", required=True)
@click.option("--input", help="Input file path (parquet or jsonl)")
@click.option("--output", help="Output file path for results")
@click.option("--system_message", help="Optional system message to use for inference")
def inference(model_id, input, output, system_message):
    """
    Run inference using a specified model ID.
    
    MODEL_ID: ID of the model to use for inference
    """
    project_type = "text-to-sql"
    
    with resources.path("lamini.project_templates", project_type) as template_path:
        template_dir = pathlib.Path(template_path)
        script_path = os.path.join(template_dir, "main_scripts", "inference.py")
        
        if not os.path.exists(script_path):
            click.echo(f"Inference script not found for project type '{project_type}'.")
            return
    
    # Build the command
    cmd = ["python", script_path, "--model_id", model_id]
    if input:
        cmd.extend(["--eval_file_path", input])
    if output:
        cmd.extend(["--output", output])
    if system_message:
        cmd.extend(["--system_message", system_message])
    
    # Run the inference script
    click.echo(f"Running inference with model: {model_id}")
    result = subprocess.run(cmd)
    return

@cli.command()
@click.argument("eval-data", required=False, default=None)
@click.argument("model-name", required=False, default=None)
@click.argument("metrics", required=False, default=None, nargs=-1)
@click.argument("output-dir", required=False, default=None)
def eval(eval_data, model_name, metrics, output_dir):
    if not os.path.exists(eval_data):
        click.echo(f"Eval data '{eval_data}' does not exist.")
        return
    if not os.path.exists(output_dir):
        click.echo(f"Output directory '{output_dir}' does not exist.")
        return
    with resources.path("lamini.project_templates", "text-to-sql") as template_path:
        template_dir = pathlib.Path(template_path)
    target_dir = os.path.join(template_dir, "main_scripts")
    script_path = os.path.join(target_dir, "eval.py")
    if not os.path.exists(script_path):
        click.echo(f"No 'eval.py' found in workspace '{target_dir}'.")
        return
    result = subprocess.run(["python", script_path, eval_data, model_name, metrics, output_dir])
    if result.returncode != 0:
        click.echo(f"'eval.py' exited with code {result.returncode}")
            

if __name__ == "__main__":
    cli()
