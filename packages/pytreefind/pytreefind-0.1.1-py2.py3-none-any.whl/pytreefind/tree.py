import subprocess
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description="List backend Python files in a tree structure.")
    parser.add_argument("--level", "-L", type=int, default=3, help="Max depth level (default: 3)")
    parser.add_argument("path", nargs="?", default=".", help="Directory to scan (default: current)")
    args = parser.parse_args()

    command = [
        "tree",
        f"-P", "*.py",
        f"-I", "__pycache__|env|venv|.git|node_modules|.pytest_cache|*.egg-info",
        f"-L", str(args.level),
        "-a", args.path
    ]

    try:
        subprocess.run(command, check=True)
    except FileNotFoundError:
        print("Error: 'tree' command not found. Please install it with your package manager.")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print("Error running tree:", e)
        sys.exit(e.returncode)

if __name__ == "__main__":
    main()
