import click
import sys
import os
from typing import Optional
from pathlib import Path
import json

from core.engine import FirewallEngine
from core.config_manager import ConfigManager

@click.group()
@click.version_option(version="1.0.0")
def cli():
    """PhantomFirewall - Adaptive Firewall System with ML capabilities"""
    pass

@cli.command()
@click.option('--
