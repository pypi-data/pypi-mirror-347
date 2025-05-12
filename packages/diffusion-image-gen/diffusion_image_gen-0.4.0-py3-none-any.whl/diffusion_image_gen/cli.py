import argparse
import subprocess
import sys
import os
from importlib import resources


def run_dashboard_command():
    """Locates and runs the Streamlit dashboard main script."""
    try:
        with resources.path('diffusion_image_gen.dashboard_app', 'main_dashboard.py') as dashboard_script_path:
            dashboard_dir = os.path.dirname(dashboard_script_path)
            command = [sys.executable, "-m", "streamlit",
                       "run", str(dashboard_script_path)]

            print(f"Attempting to run dashboard from: {dashboard_script_path}")
            process = subprocess.Popen(command, cwd=dashboard_dir)
            process.wait()
    except ModuleNotFoundError:
        print("Error: The 'diffusion_image_gen.dashboard_app' module was not found. "
              "Please ensure the dashboard files are correctly placed and the package is installed.", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("Error: 'main_dashboard.py' not found within 'diffusion_image_gen.dashboard_app'. "
              "Please check your package structure.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(
            f"An unexpected error occurred while trying to run the dashboard: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="diffusion-image-gen: A CLI tool for image generation models and dashboard.",
        prog="diffusion_image_gen"
    )
    subparsers = parser.add_subparsers(title='commands', dest='command_name',
                                       help='Available commands. Type a command followed by -h for more help.')
    if sys.version_info >= (3, 7):
        subparsers.required = True

    dashboard_parser = subparsers.add_parser(
        'dashboard',
        help='Run the Streamlit dashboard for diffusion_image_gen.',
        description='Starts the Streamlit web application for interacting with image generation models.'
    )
    dashboard_parser.set_defaults(func=run_dashboard_command)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func()
    elif not hasattr(args, 'func'):
        parser.print_help()


if __name__ == '__main__':
    main()
