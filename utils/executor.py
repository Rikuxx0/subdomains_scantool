import subprocess
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def run_command(command, output_file=None, shell=True):
    """Executes a shell command and optionally saves its output to a file."""
    logger.info(f"Executing: {command}")
    try:
        process = subprocess.Popen(
            command,
            shell=shell,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        stdout, stderr = process.communicate()
        
        if process.returncode != 0:
            logger.error(f"Command failed with return code {process.returncode}")
            if stderr:
                logger.error(f"Error: {stderr.strip()}")
            return False
        
        if output_file:
            with open(output_file, 'w') as f:
                f.write(stdout)
            logger.info(f"Output saved to {output_file}")
            
        return stdout
    except Exception as e:
        logger.error(f"An exception occurred: {e}")
        return False

def pipe_commands(commands):
    """Executes a series of commands piped together."""
    full_command = " | ".join(commands)
    return run_command(full_command)
