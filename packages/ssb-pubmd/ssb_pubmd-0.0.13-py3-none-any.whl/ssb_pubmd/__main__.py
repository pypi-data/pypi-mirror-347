"""Command-line interface."""

import json

import click

from ssb_pubmd.browser_context import BrowserRequestContext as RequestContext
from ssb_pubmd.markdown_syncer import MarkdownSyncer

CONFIG_FILE = "pubmd_config.json"


class ConfigKeys:
    """The keys used in the configuration file."""

    LOGIN = "login_url"
    POST = "post_url"


def get_config_value(key: str) -> str:
    """Get a configuration value."""
    try:
        with open(CONFIG_FILE) as json_file:
            config = json.load(json_file)
            value = config[key]
    except FileNotFoundError:
        click.echo(
            f"Configuration file '{CONFIG_FILE}' not found. Please run the 'config' command first."
        )
    except Exception:
        click.echo(
            f"Error reading configuration file '{CONFIG_FILE}'. Please run the 'pubmd config' command again."
        )
    return str(value)


@click.group()
def cli() -> None:
    """'pubmd' is a tool to sync markdown and notebook files to a CMS application.

    Setup with subcommands 'config' and 'login', then use subcommand 'sync'.
    """
    pass


@click.command()
def config() -> None:
    """Configure the CMS to connect to."""
    login_url = click.prompt("Enter the login URL", type=str)
    post_url = click.prompt("Enter the post URL", type=str)

    config = {ConfigKeys.LOGIN: login_url, ConfigKeys.POST: post_url}

    with open(CONFIG_FILE, "w") as json_file:
        json.dump(config, json_file, indent=4)

    click.echo(f"\nThe configuration has been stored in:\n{CONFIG_FILE}")


@click.command()
def login() -> None:
    """Login to the CMS application."""
    login_url = get_config_value(ConfigKeys.LOGIN)
    request_context = RequestContext()
    storage_state_file, storage_state = request_context.create_new(login_url)
    click.echo(f"\nThe browser context has been stored in:\n{storage_state_file}")


@click.command()
@click.argument("content_file_path", type=click.Path())
def sync(content_file_path: str) -> None:
    """Sync a markdown or notebook file to the CMS."""
    post_url = get_config_value(ConfigKeys.POST)
    request_context = RequestContext()
    request_context.recreate_from_file()

    syncer = MarkdownSyncer(post_url=post_url, request_context=request_context)
    syncer.content_file_path = content_file_path

    content_id = syncer.sync_content()

    click.echo(
        f"File '{click.format_filename(content_file_path)}' synced to CMS with content ID: {content_id}"
    )


cli.add_command(config)
cli.add_command(login)
cli.add_command(sync)

if __name__ == "__main__":
    cli()  # pragma: no cover
