import click
import requests 
import json
#from my_cli_project import utils
#from my_cli_project.utils import reverse_string
import configparser
import os

# Define the config file path
CONFIG_FILE = os.path.expanduser("~/.sf-helper.ini") #C:\Users\<YourUsername>\.sf-helper.ini

def get_config():
    """Load the config file."""
    config = configparser.ConfigParser()
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)
    if 'DEFAULT' not in config:
        config['DEFAULT'] = {}
    return config

def save_config(config):
    """Save the config file."""
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)

@click.group()
def cli():
    """Salesforce Helper CLI"""
    pass

@cli.command()
@click.option('--api-key', prompt='Enter API key', hide_input=True, help='Set the API key.')
def set_key(api_key):
    """Set and persist the API key."""
    config = get_config()
    config['DEFAULT']['api_key'] = api_key
    save_config(config)
    click.echo("API key saved successfully!")

@cli.command()
def get_key():
    """Retrieve the stored API key."""
    config = get_config()
    api_key = config['DEFAULT'].get('api_key', None)
    if api_key:
        click.echo(f"Stored API key: {api_key}")
    else:
        click.echo("No API key set. Use 'set-key' to set one.")