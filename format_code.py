import json
import logging
import os
import subprocess
import sys
import time
from pathlib import Path

# 📂 Setup logging
LOG_FILE = Path("logs/format.log")
LOG_FILE.parent.mkdir(exist_ok=True)
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# 🔁 Retry decorator


def retry(max_attempts=3, delay=2):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except subprocess.CalledProcessError as e:
                    logging.error(f"Attempt {attempt} failed: {e.stderr.strip()}")
                    if attempt < max_attempts:
                        time.sleep(delay)
                    else:
                        logging.critical(
                            f"{args[1]} failed after {max_attempts} attempts."
                        )
                        sys.exit(e.returncode)

        return wrapper

    return decorator


# 🧱 Command runner


@retry()
def run_command(cmd: list, name: str):
    logging.info(f"Running {name}...")
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    logging.info(f"{name} succeeded.")
    print(f"✅ {name} completed.")


# 📜 Load config


def load_config(path="formatter_config.json"):
    with open(path, "r") as f:
        return json.load(f)


# 🔄 Resolve environment overrides


def resolve_command(tool_name, default_cmd, env_overrides):
    env_var = env_overrides.get(tool_name.lower())
    if env_var and env_var.startswith("${") and env_var.endswith("}"):
        var_name = env_var[2:-1]
        return os.environ.get(var_name, default_cmd)
    return default_cmd


# 🚀 Main execution
if __name__ == "__main__":
    config = load_config()
    tools = config.get("tools", [])
    env_overrides = config.get("env_overrides", {})

    for tool in tools:
        cmd_name = resolve_command(tool["name"], tool["command"], env_overrides)
        full_cmd = [cmd_name] + tool["args"]
        run_command(full_cmd, tool["name"])
