"Download SmartDS case data from AWS or HPC."

from pathlib import Path
import shutil
import getpass

import click

from dsloader.case.hpc import cached_copy_hpc_dir
from dsloader.case.smartds import (
    build_smartd_profile_prefix,
    build_smartds_model_prefix,
    download_aws_smartds_dataset,
)
from dsloader.exceptions import FolderAlreadyExistsError


@click.command()
@click.option(
    "-t",
    "--target-dir",
    type=str,
    help="Target directory for downloading case.",
)
@click.option(
    "-f",
    "--force",
    is_flag=True,
    default=False,
    help="Delete target directory forcefully if exists.",
)
@click.option(
    "-a",
    "--area",
    type=str,
    default="SFO",
    show_default=True,
    help="""SMARTDS area name e.g. SFO, AUS, GSO""",
)
@click.option(
    "-y",
    "--year",
    type=int,
    default=2018,
    show_default=True,
    help="""Model year to download.""",
)
@click.option(
    "-v",
    "--version",
    type=str,
    default="v1.0",
    show_default=True,
    help="""Model version to download.""",
)
@click.option(
    "-r",
    "--region",
    type=str,
    default="P10U",
    show_default=True,
    help="""SMARTDS region name. See available regions here
    https://data.openei.org/s3_viewer?bucket=oedi-data-lake&prefix=SMART-DS%2Fv1.0%2F2018%2FSFO%2F""",
)
@click.option(
    "-fe",
    "--feeder",
    type=str,
    help="""You can keep this empty if you want to download full region.""",
)
@click.option(
    "-ts",
    "--timeseries",
    is_flag=True,
    default=False,
    show_default=True,
    help="""Download timeseries model along with profiles.""",
)
@click.option(
    "-hpc",
    "--use_hpc",
    is_flag=True,
    default=False,
    show_default=True,
    help="""Use HPC to copy the data.""",
)
@click.option(
    "-h",
    "--hostname",
    type=str,
    default="kestrel.hpc.nrel.gov",
    show_default=True,
    help="""Hostname for HPC system.""",
)
@click.option(
    "-u",
    "--username",
    type=str,
    help="""HPC user name.""",
)
@click.option(
    "-bf",
    "--base-folder",
    type=str,
    default="/datasets",
    help="""Base folder name.""",
)
def download_smartds(
    target_dir: str,
    force: bool,
    area: str,
    year: int,
    version: str,
    region: str,
    feeder: str,
    timeseries: bool,
    use_hpc: bool,
    hostname: str,
    username: str,
    base_folder: str | Path,
):
    """Download SMART-DS dataset.

    Parameters
    ----------
    target_dir : str
        Target directory for downloading case.
    force : bool
        Delete target directory forcefully if exists.
    area : str
        SMARTDS area name e.g. SFO, AUS, GSO
    year : int
        Model year to download.
    version : str
        Model version to download.
    region : str
        SMARTDS region name. See available regions here
        https://data.openei.org/s3_viewer?bucket=oedi-data-lake&prefix=SMART-DS%2Fv1.0%2F2018%2F
    feeder : str
        You can keep this empty if you want to download full region.
    timeseries : bool
        Download timeseries model along with profiles.
    use_hpc : bool
        Use HPC to copy the data.
    hostname : str
        Hostname for HPC system.
    username : str
        HPC user name.
    base_folder : str | Path
        Base folder name.
    """
    working_dir = Path(target_dir)
    base_folder = Path(base_folder) if isinstance(base_folder, str) else base_folder
    if force and working_dir.exists():
        shutil.rmtree(working_dir)
    if not force and working_dir.exists():
        raise FolderAlreadyExistsError(
            f"""{working_dir} already exists. Consider deleting it first."""
        )
    folder = "opendss" if timeseries else "opendss_no_loadshapes"
    smartds_prefix = build_smartds_model_prefix(
        year, area, version, region, folder, feeder=feeder or ""
    )
    profile_prefix = build_smartd_profile_prefix(
        year, area, version, region if timeseries else None
    )

    if use_hpc:
        password = getpass.getpass(f"Enter SSH password for {hostname}:")
        cached_copy_hpc_dir(
            hostname,
            username,
            password,
            smartds_prefix,
            working_dir,
            base_folder,
        )

        if timeseries:
            cached_copy_hpc_dir(
                hostname,
                username,
                password,
                profile_prefix,
                working_dir,
                base_folder,
            )
    else:
        download_aws_smartds_dataset(smartds_prefix, working_dir)
        if timeseries:
            download_aws_smartds_dataset(profile_prefix, working_dir)
