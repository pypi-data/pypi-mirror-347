import os
import sys
import click
import json
import pandas as pd
from pathlib import Path

# Add parent directory to path to allow direct script execution
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Define user config directory and file
USER_CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".algosystem")
USER_CONFIG_FILE = os.path.join(USER_CONFIG_DIR, "config.json")


def ensure_user_config_exists():
    """
    Ensure the user configuration file exists. If not, create it with default settings.
    If it exists but is invalid, reset it to default settings.

    Returns:
    --------
    str
        Path to the user configuration file
    """
    # Create .algosystem directory if it doesn't exist
    os.makedirs(USER_CONFIG_DIR, exist_ok=True)

    # Load default configuration
    from algosystem.backtesting.dashboard.utils.default_config import get_default_config

    default_config = get_default_config()

    # Check if user config exists
    if not os.path.exists(USER_CONFIG_FILE):
        click.echo(f"Creating new user configuration at: {USER_CONFIG_FILE}")
        with open(USER_CONFIG_FILE, "w") as f:
            json.dump(default_config, f, indent=4)
        click.echo("User configuration initialized with default settings.")
        return USER_CONFIG_FILE

    # Validate existing config
    try:
        with open(USER_CONFIG_FILE, "r") as f:
            user_config = json.load(f)

        # Basic validation - check required sections
        required_sections = ["metrics", "charts", "layout"]
        config_valid = True

        for section in required_sections:
            if section not in user_config:
                config_valid = False
                break

        # Check that metrics and charts are lists
        if config_valid:
            if not isinstance(user_config.get("metrics"), list):
                config_valid = False
            if not isinstance(user_config.get("charts"), list):
                config_valid = False
            if not isinstance(user_config.get("layout"), dict):
                config_valid = False

        # Additional validation for required fields in metrics and charts
        if config_valid:
            for metric in user_config["metrics"]:
                if not all(
                    key in metric for key in ["id", "type", "title", "value_key", "position"]
                ):
                    config_valid = False
                    break

            for chart in user_config["charts"]:
                if not all(key in chart for key in ["id", "type", "title", "data_key", "position"]):
                    config_valid = False
                    break

        if config_valid:
            click.echo(f"Using existing user configuration: {USER_CONFIG_FILE}")
            return USER_CONFIG_FILE
        else:
            # Invalid config - reset to default
            click.echo(
                f"Warning: User configuration file is invalid. Resetting to default settings."
            )
            # Backup the old config
            backup_file = (
                f"{USER_CONFIG_FILE}.backup.{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}"
            )
            os.rename(USER_CONFIG_FILE, backup_file)
            click.echo(f"Old configuration backed up to: {backup_file}")

            # Create new config with defaults
            with open(USER_CONFIG_FILE, "w") as f:
                json.dump(default_config, f, indent=4)
            click.echo("User configuration reset to default settings.")
            return USER_CONFIG_FILE

    except (json.JSONDecodeError, IOError) as e:
        # File exists but can't be read - reset to default
        click.echo(
            f"Warning: Cannot read user configuration file ({str(e)}). Resetting to default settings."
        )
        # Backup the old config
        backup_file = f"{USER_CONFIG_FILE}.backup.{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}"
        if os.path.exists(USER_CONFIG_FILE):
            os.rename(USER_CONFIG_FILE, backup_file)
            click.echo(f"Old configuration backed up to: {backup_file}")

        # Create new config with defaults
        with open(USER_CONFIG_FILE, "w") as f:
            json.dump(default_config, f, indent=4)
        click.echo("User configuration reset to default settings.")
        return USER_CONFIG_FILE


@click.group()
def cli():
    """AlgoSystem Dashboard command-line interface."""
    pass


@cli.command()
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=True),
    help="Path to a dashboard configuration file to load",
)
@click.option(
    "--data-dir",
    "-d",
    type=click.Path(exists=True),
    help="Directory containing data files to preload",
)
@click.option(
    "--host",
    type=str,
    default="127.0.0.1",
    help="Host to run the dashboard editor server on (default: 127.0.0.1)",
)
@click.option(
    "--port",
    type=int,
    default=5000,
    help="Port to run the dashboard editor server on (default: 5000)",
)
@click.option("--debug", is_flag=True, default=False, help="Run the server in debug mode")
@click.option(
    "--save-config",
    type=click.Path(),
    help="Path to save the edited configuration file (creates a new file if it does not exist)",
)
@click.option(
    "--default",
    is_flag=True,
    default=False,
    help="Use the default configuration instead of user config",
)
def launch(config, data_dir, host, port, debug, save_config, default):
    """Launch the AlgoSystem Dashboard UI."""
    # Clear environment variables to start fresh
    if "ALGO_DASHBOARD_CONFIG" in os.environ:
        del os.environ["ALGO_DASHBOARD_CONFIG"]
    if "ALGO_DASHBOARD_SAVE_CONFIG" in os.environ:
        del os.environ["ALGO_DASHBOARD_SAVE_CONFIG"]

    # Determine which configuration to use
    if default:
        # Use library default config
        from algosystem.backtesting.dashboard.utils.default_config import DEFAULT_CONFIG_PATH

        os.environ["ALGO_DASHBOARD_CONFIG"] = DEFAULT_CONFIG_PATH
        click.echo("Using library default configuration")
    elif config:
        # Use specified config file
        os.environ["ALGO_DASHBOARD_CONFIG"] = os.path.abspath(config)
        click.echo(f"Loading configuration from: {os.path.abspath(config)}")
    else:
        # Use or create user config
        user_config_path = ensure_user_config_exists()
        os.environ["ALGO_DASHBOARD_CONFIG"] = user_config_path
        click.echo(f"Using user configuration: {user_config_path}")

    # Set save location
    if save_config:
        # Ensure it's an absolute path
        save_config_path = os.path.abspath(save_config)
        os.environ["ALGO_DASHBOARD_SAVE_CONFIG"] = save_config_path
        click.echo(f"Configuration will be saved to: {save_config_path}")

        # Create directory for save_config if it doesn't exist
        os.makedirs(os.path.dirname(save_config_path), exist_ok=True)
    else:
        # If no save-config specified and using user config, save back to user config
        if not default and not config:
            os.environ["ALGO_DASHBOARD_SAVE_CONFIG"] = USER_CONFIG_FILE
            click.echo(f"Changes will be saved to user configuration: {USER_CONFIG_FILE}")

    if data_dir:
        os.environ["ALGO_DASHBOARD_DATA_DIR"] = os.path.abspath(data_dir)

    # Launch the dashboard web editor
    try:
        from algosystem.backtesting.dashboard.web_app.app import start_dashboard_editor

        click.echo(f"Starting AlgoSystem Dashboard Editor on http://{host}:{port}/")
        click.echo("Press Ctrl+C to stop the server.")
        start_dashboard_editor(host=host, port=port, debug=debug)
    except ImportError as e:
        click.echo(f"Error: {e}")
        click.echo("Make sure Flask is installed: pip install flask")
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error starting dashboard editor: {e}")
        sys.exit(1)


@cli.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option(
    "--output-dir",
    "-o",
    type=click.Path(),
    default="./dashboard_output",
    help="Directory to save the dashboard files (default: ./dashboard_output)",
)
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=True),
    help="Path to a custom dashboard configuration file",
)
@click.option(
    "--benchmark", "-b", type=click.Path(exists=True), help="Path to a CSV file with benchmark data"
)
@click.option(
    "--open-browser",
    is_flag=True,
    default=False,
    help="Open the dashboard in a browser after rendering",
)
@click.option(
    "--default",
    is_flag=True,
    default=False,
    help="Use library default configuration (overrides --config)",
)
def render(input_file, output_dir, config, benchmark, open_browser, default):
    """
    Render a dashboard from a CSV file with strategy data.

    INPUT_FILE: Path to a CSV file with strategy data
    """
    import json
    import webbrowser
    from algosystem.backtesting.engine import Engine
    from algosystem.backtesting.dashboard.dashboard_generator import generate_dashboard

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Load the dashboard configuration
    config_path = None
    if default:
        click.echo("Using library default dashboard configuration")
        from algosystem.backtesting.dashboard.utils.default_config import DEFAULT_CONFIG_PATH

        config_path = DEFAULT_CONFIG_PATH
    elif config:
        click.echo(f"Using custom configuration from: {config}")
        config_path = config
    else:
        # Use user config
        config_path = ensure_user_config_exists()
        click.echo(f"Using user configuration: {config_path}")

    try:
        # Load the CSV data
        click.echo(f"Loading data from {input_file}...")
        data = pd.read_csv(input_file, index_col=0, parse_dates=True)
        click.echo(f"Loaded data with shape: {data.shape}")

        # Load benchmark data if provided
        benchmark_data = None
        if benchmark:
            click.echo(f"Loading benchmark data from {benchmark}...")
            benchmark_data = pd.read_csv(benchmark, index_col=0, parse_dates=True)
            if isinstance(benchmark_data, pd.DataFrame) and benchmark_data.shape[1] > 1:
                benchmark_data = benchmark_data.iloc[:, 0]  # Use first column
            click.echo(f"Loaded benchmark data with {len(benchmark_data)} rows")

        # Create a backtest engine to process the data
        click.echo("Running backtest...")
        if isinstance(data, pd.DataFrame) and data.shape[1] > 1:
            # Use the first column as price data
            price_data = data.iloc[:, 0]
        else:
            price_data = data

        # Initialize and run the engine
        engine = Engine(data=price_data, benchmark=benchmark_data)
        results = engine.run()
        click.echo("Backtest completed successfully")

        # Generate dashboard
        click.echo(f"Generating dashboard using configuration from: {config_path}")
        dashboard_path = generate_dashboard(
            engine=engine, output_dir=output_dir, open_browser=open_browser, config_path=config_path
        )

        click.echo(f"Dashboard generated successfully at: {dashboard_path}")

        # Provide instructions for viewing
        if not open_browser:
            click.echo("To view the dashboard, open this file in a web browser:")
            click.echo(f"  {os.path.abspath(dashboard_path)}")

    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("output_path", type=click.Path())
@click.option(
    "--based-on",
    "-b",
    type=click.Path(exists=True),
    help="Path to an existing configuration file to use as a base",
)
@click.option(
    "--default",
    is_flag=True,
    default=False,
    help="Create config based on library default configuration",
)
@click.option(
    "--user", is_flag=True, default=False, help="Create config based on user configuration"
)
def create_config(output_path, based_on, default, user):
    """
    Create a dashboard configuration file.

    OUTPUT_PATH: Path where the configuration file will be saved
    """
    # Load the base configuration
    if default:
        # Load the library default configuration
        from algosystem.backtesting.dashboard.utils.default_config import DEFAULT_CONFIG_PATH

        click.echo("Creating configuration based on library default template")
        with open(DEFAULT_CONFIG_PATH, "r") as f:
            config = json.load(f)
    elif user:
        # Load user configuration
        user_config_path = ensure_user_config_exists()
        click.echo(f"Creating configuration based on user template: {user_config_path}")
        with open(user_config_path, "r") as f:
            config = json.load(f)
    elif based_on:
        try:
            click.echo(f"Creating configuration based on: {based_on}")
            with open(based_on, "r") as f:
                config = json.load(f)
        except Exception as e:
            click.echo(f"Error loading base configuration: {str(e)}", err=True)
            sys.exit(1)
    else:
        # Default to user config if it exists, otherwise library default
        if os.path.exists(USER_CONFIG_FILE):
            click.echo("Creating configuration based on user template")
            with open(USER_CONFIG_FILE, "r") as f:
                config = json.load(f)
        else:
            from algosystem.backtesting.dashboard.utils.default_config import DEFAULT_CONFIG_PATH

            click.echo("Creating configuration based on library default template")
            with open(DEFAULT_CONFIG_PATH, "r") as f:
                config = json.load(f)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    # Save configuration file
    try:
        with open(output_path, "w") as f:
            json.dump(config, f, indent=4)
        click.echo(f"Configuration saved to: {output_path}")
    except Exception as e:
        click.echo(f"Error saving configuration: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option(
    "--output-file",
    "-o",
    type=click.Path(),
    default="./dashboard.html",
    help="Path to save the dashboard HTML file (default: ./dashboard.html)",
)
@click.option(
    "--benchmark", "-b", type=click.Path(exists=True), help="Path to a CSV file with benchmark data"
)
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=True),
    help="Path to a custom dashboard configuration file",
)
@click.option(
    "--default",
    is_flag=True,
    default=False,
    help="Use library default configuration (overrides --config)",
)
@click.option(
    "--open-browser",
    is_flag=True,
    default=True,
    help="Open the dashboard in a browser after rendering",
)
def dashboard(input_file, output_file, benchmark, config, default, open_browser):
    """
    Create a standalone HTML dashboard from a CSV file that can be viewed without a web server.

    INPUT_FILE: Path to a CSV file with strategy data
    """
    import webbrowser
    from algosystem.backtesting.engine import Engine
    from algosystem.backtesting.dashboard.dashboard_generator import generate_standalone_dashboard

    # Determine which configuration to use
    config_path = None
    if default:
        click.echo("Using library default dashboard configuration")
        from algosystem.backtesting.dashboard.utils.default_config import DEFAULT_CONFIG_PATH

        config_path = DEFAULT_CONFIG_PATH
    elif config:
        click.echo(f"Using custom configuration from: {config}")
        config_path = config
    else:
        # Use user config
        config_path = ensure_user_config_exists()
        click.echo(f"Using user configuration: {config_path}")

    try:
        # Load the CSV data
        click.echo(f"Loading data from {input_file}...")
        data = pd.read_csv(input_file, index_col=0, parse_dates=True)
        click.echo(f"Loaded data with shape: {data.shape}")

        # Load benchmark data if provided
        benchmark_data = None
        if benchmark:
            click.echo(f"Loading benchmark data from {benchmark}...")
            benchmark_data = pd.read_csv(benchmark, index_col=0, parse_dates=True)
            if isinstance(benchmark_data, pd.DataFrame) and benchmark_data.shape[1] > 1:
                benchmark_data = benchmark_data.iloc[:, 0]  # Use first column
            click.echo(f"Loaded benchmark data with {len(benchmark_data)} rows")

        # Create a backtest engine to process the data
        click.echo("Running backtest...")
        if isinstance(data, pd.DataFrame) and data.shape[1] > 1:
            # Use the first column as price data
            price_data = data.iloc[:, 0]
        else:
            price_data = data

        # Initialize and run the engine
        engine = Engine(data=price_data, benchmark=benchmark_data)
        results = engine.run()
        click.echo("Backtest completed successfully")

        # Generate standalone dashboard
        click.echo(f"Generating standalone dashboard using configuration from: {config_path}")
        dashboard_path = generate_standalone_dashboard(
            engine=engine, output_path=output_file, config_path=config_path
        )

        click.echo(f"Standalone dashboard generated successfully at: {dashboard_path}")

        # Open in browser if requested
        if open_browser:
            webbrowser.open("file://" + os.path.abspath(dashboard_path))
        else:
            click.echo("To view the dashboard, open this file in a web browser:")
            click.echo(f"  {os.path.abspath(dashboard_path)}")

    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("config_file", type=click.Path(exists=True))
def show_config(config_file):
    """
    Display the contents of a configuration file in a readable format.

    CONFIG_FILE: Path to the configuration file to display
    """
    try:
        with open(config_file, "r") as f:
            config = json.load(f)

        click.echo(f"Configuration file: {config_file}\n")

        # Display layout
        if "layout" in config:
            click.echo("=== Layout ===")
            click.echo(f"Title: {config['layout'].get('title', 'N/A')}")
            click.echo(f"Max columns: {config['layout'].get('max_cols', 'N/A')}")
            click.echo("")

        # Display metrics
        if "metrics" in config:
            click.echo("=== Metrics ===")
            for i, metric in enumerate(config["metrics"]):
                click.echo(
                    f"{i+1}. {metric.get('title', 'Untitled')} ({metric.get('id', 'no-id')})"
                )
                click.echo(f"   Type: {metric.get('type', 'N/A')}")
                click.echo(
                    f"   Position: Row {metric['position'].get('row', 'N/A')}, Column {metric['position'].get('col', 'N/A')}"
                )
                click.echo("")

        # Display charts
        if "charts" in config:
            click.echo("=== Charts ===")
            for i, chart in enumerate(config["charts"]):
                click.echo(f"{i+1}. {chart.get('title', 'Untitled')} ({chart.get('id', 'no-id')})")
                click.echo(f"   Type: {chart.get('type', 'N/A')}")
                click.echo(f"   Data Key: {chart.get('data_key', 'N/A')}")
                click.echo(
                    f"   Position: Row {chart['position'].get('row', 'N/A')}, Column {chart['position'].get('col', 'N/A')}"
                )
                click.echo("")

    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.option(
    "--show-user", is_flag=True, default=False, help="Show full path of user configuration file"
)
@click.option(
    "--show-default",
    is_flag=True,
    default=False,
    help="Show full path of library default configuration file",
)
def list_configs(show_user, show_default):
    """
    List all available configuration files in the user's home directory.
    """
    # Show special config file paths if requested
    if show_user:
        user_config_path = ensure_user_config_exists()
        click.echo(f"User configuration file: {user_config_path}")
        return

    if show_default:
        from algosystem.backtesting.dashboard.utils.default_config import DEFAULT_CONFIG_PATH

        click.echo(f"Library default configuration: {DEFAULT_CONFIG_PATH}")
        return

    # List all config files in user directory
    if not os.path.exists(USER_CONFIG_DIR):
        click.echo(
            "No configuration directory found. Use 'create-config' to create your first configuration."
        )
        return

    config_files = [f for f in os.listdir(USER_CONFIG_DIR) if f.endswith(".json")]

    if not config_files:
        click.echo("No configuration files found in the user directory.")
        click.echo(f"Directory: {USER_CONFIG_DIR}")
        return

    click.echo(f"Configuration files in {USER_CONFIG_DIR}:")
    for i, config_file in enumerate(config_files):
        full_path = os.path.join(USER_CONFIG_DIR, config_file)
        file_size = os.path.getsize(full_path) / 1024  # size in KB
        mod_time = os.path.getmtime(full_path)
        mod_time_str = pd.to_datetime(mod_time, unit="s").strftime("%Y-%m-%d %H:%M:%S")

        # Mark the main user config file
        marker = " (user config)" if config_file == "config.json" else ""
        click.echo(f"{i+1}. {config_file}{marker} ({file_size:.1f} KB, modified: {mod_time_str})")

    # Show paths to special files
    click.echo(f"\nUser configuration: {USER_CONFIG_FILE}")
    click.echo("Use --show-default to see the library default configuration path")


# Add a new command to reset user config
@cli.command()
@click.option(
    "--backup",
    is_flag=True,
    default=True,
    help="Create a backup of existing user configuration (default: True)",
)
@click.option(
    "--no-backup", is_flag=True, default=False, help="Do not create a backup (overrides --backup)"
)
def reset_user_config(backup, no_backup):
    """
    Reset the user configuration to library defaults.
    """
    if not os.path.exists(USER_CONFIG_FILE):
        click.echo("No user configuration file exists. Creating one now...")
        ensure_user_config_exists()
        return

    # Confirm reset
    click.confirm(
        f"This will reset your user configuration at {USER_CONFIG_FILE} to library defaults. "
        f"Continue?",
        abort=True,
    )

    # Create backup if requested
    create_backup = backup and not no_backup
    if create_backup:
        backup_file = f"{USER_CONFIG_FILE}.backup.{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}"
        os.rename(USER_CONFIG_FILE, backup_file)
        click.echo(f"Backup created: {backup_file}")

    # Load default config and save to user config
    from algosystem.backtesting.dashboard.utils.default_config import get_default_config

    default_config = get_default_config()

    with open(USER_CONFIG_FILE, "w") as f:
        json.dump(default_config, f, indent=4)

    click.echo(f"User configuration reset to library defaults: {USER_CONFIG_FILE}")


if __name__ == "__main__":
    cli()
