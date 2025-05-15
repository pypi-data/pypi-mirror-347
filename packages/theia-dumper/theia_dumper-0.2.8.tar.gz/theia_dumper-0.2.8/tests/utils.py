"""Utils file."""

from theia_dumper import cli


STAC_EP_DEV = "https://api-dev.stac.teledetection.fr"
S3_SIGNING_EP_DEV = "https://signing-dev.stac.teledetection.fr/"


def set_test_stac_ep() -> None:
    """Change stac endpoint for tests."""
    cli.DEFAULT_STAC_EP = STAC_EP_DEV
