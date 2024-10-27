import subprocess
import os
import logging

def setup_logger(log_file_path):
    # Set up the logger
    logger = logging.getLogger("DockerRunner")
    logger.setLevel(logging.INFO)

    # Create file handler for logging to a file
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.INFO)

    # Create console handler for logging to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Create a logging format
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

def run_docker():
    try:
        # Get the current working directory
        current_dir = os.path.abspath(os.getcwd())
        
        # Define the output directory path (using the same directory for input and output)
        output_dir = os.path.join(current_dir, "output")

        # Make sure output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Define the log file path
        log_file_path = os.path.join(current_dir, "docker_output.log")

        # Set up the logger
        logger = setup_logger(log_file_path)

        # Define the Docker command
        docker_command = [
            "sudo", "docker", "run", "--rm", "--user", "root",
            "-v", f"{output_dir}:/output",  # Same path for both input and output
            "-v", f"{output_dir}:/input",   # Mapping input to the same output directory
            "--entrypoint", "/bin/sh",
            "cosmos9526/varient_calling:latest",
            "-c", "/usr/bin/python3 /run2.py --input_dir /input --output_dir /output"
        ]

        logger.info("Starting Docker command execution...")

        # Run the Docker command
        process = subprocess.Popen(docker_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        # Read output line by line
        for line in process.stdout:
            logger.info(line.strip())  # Log each line

        # Wait for the process to finish
        process.wait()

        # Check the return code and print a success or error message
        if process.returncode == 0:
            logger.info("Docker container executed successfully.")
        else:
            logger.error(f"Docker container failed with return code {process.returncode}.")

    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    run_docker()
