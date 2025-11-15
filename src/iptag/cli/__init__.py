"""Interview Phrase Tagger CLI (iptag) package initialization."""

import typer

from iptag.settings import IptagSettings

from .data import app as data
from .models import app as models

iptag_settings = IptagSettings()
typer.echo(f"Debug mode is {'ON' if iptag_settings.debug else 'OFF'}")

# Create Typer root app
app = typer.Typer(help="Interview Phrase Tagger CLI (iptag)")

# Add sub typer apps
app.add_typer(data, name="data")
app.add_typer(models, name="models")
