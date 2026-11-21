import logging
import shlex
import subprocess
import sys

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger(__name__)


def run_command(args, *, input_text=None, output_file=None, secret_args=()):
    """Run a tool, stopping the pipeline when it fails."""
    display = ["[REDACTED]" if arg in secret_args else arg for arg in args]
    logger.info("Executing: %s", shlex.join(display))
    try:
        result = subprocess.run(args, input=input_text, text=True, capture_output=True, check=True)
    except (OSError, subprocess.CalledProcessError) as exc:
        detail = exc.stderr.strip() if isinstance(exc, subprocess.CalledProcessError) else str(exc)
        raise RuntimeError(f"{args[0]} failed: {detail}") from exc
    if output_file is not None:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result.stdout)
    return result.stdout
