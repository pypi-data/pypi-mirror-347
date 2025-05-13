import logging
import logging.handlers
import os
from importlib.metadata import version
from typing import Annotated
from typer import Typer, Option
import typer

from .utils.utils import setup_cert

setup_cert()

from .model import handler
from .utils import dns

logger = logging.getLogger(__name__)

app = Typer()

def setup_logging(logging_level = logging.WARN ,enable_file_logging=False):
    """Configure logging with console and optional file handlers"""
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    logging.getLogger('urllib3').setLevel(logging.WARNING)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging_level)
    
    # Create formatters
    console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging_level)
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)
    
    # File handler (disabled by default)
    if enable_file_logging:
        file_handler = logging.handlers.RotatingFileHandler(
            f"{log_dir}/app.log",
            maxBytes=10*1024*1024,
            backupCount=5
        )
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)


@app.command("version", help="Show version and exit.")
def show_version():
    typer.echo(f"cloud-aitools version: {version('cloud-aitools')}")


@app.callback()
def main(
    verbose: Annotated[bool, Option("--verbose", "-v", help="Enable verbose logging.")] = False,
):

    log_level = logging.DEBUG if verbose else logging.WARNING
    setup_logging(logging_level=log_level, enable_file_logging=True)


app.add_typer(handler.app, name="model", help="Model related commands.")
app.add_typer(dns.app)

if __name__ == "__main__":
    app()
