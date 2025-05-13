"Build and download SMARTDS dataset from AWS S3 bucket"

from pathlib import Path

from loguru import logger

from dsloader.case.aws import (
    cached_download_aws_dir,
    fix_aws_prefix,
    get_aws_unsigned_client,
    is_aws_prefix_exist,
)
from dsloader.constants import SMARTDS_AWS_BUCKET
from dsloader.exceptions import WrongSMARTDSPrefix
from dsloader.utils import time_spent


def build_smartds_model_prefix(
    year: int, area: str, version: str, region: str, folder: str, feeder: str = ""
) -> str:
    """
    Builds the prefix path for the SMARTDS model data.

    Parameters
    ----------
    year : int
        The year of the SMARTDS data.
    area : str
        The area name of the SMARTDS data.
    version : str
        The version of the SMARTDS data.
    region : str
        The region of the SMARTDS data.
    folder : str
        The folder name of the SMARTDS data.
    feeder : str, optional
        The feeder name of the SMARTDS data. Defaults to ""

    Returns
    -------
    str
        The prefix path of the SMARTDS model data.
    """
    prefix = (
        f"SMART-DS/{version}/{year}/{area}/{region}/scenarios/base_timeseries/{folder}/{feeder}"
    )
    logger.info(f"Folder path: {prefix}")
    return prefix


def build_smartds_profile_prefix(
    year: int,
    area: str,
    version: str,
    region: str | None,
) -> str:
    """
    Builds the prefix path for the SMARTDS profile data.

    Parameters
    ----------
    year : int
        The year of the SMARTDS data.
    area : str
        The area name of the SMARTDS data.
    version : str
        The version of the SMARTDS data.
    region : str or None
        The region of the SMARTDS data. Can be None if no specific region is provided.

    Returns
    -------
    str
        The prefix path of the SMARTDS profile data.
    """

    prefix = f"SMART-DS/{version}/{year}/{area}/{region}/profiles"
    logger.info(f"Folder path: {prefix}")
    return prefix


@time_spent
def download_aws_smartds_dataset(prefix: str, target_folder: Path) -> None:
    """
    Downloads the SMARTDS dataset from AWS S3 bucket given the prefix.

    Parameters
    ----------
    prefix : str
        The prefix of the SMARTDS dataset to download.
    target_folder : Path
        The target folder to save the downloaded dataset.

    Returns
    -------
    None
    """

    prefix = fix_aws_prefix(prefix)
    client = get_aws_unsigned_client()
    if not is_aws_prefix_exist(prefix, SMARTDS_AWS_BUCKET, client):
        msg = f"{prefix} does not exist. Please fix the path first."
        logger.error(msg)
        raise WrongSMARTDSPrefix(msg)

    cached_download_aws_dir(client, SMARTDS_AWS_BUCKET, prefix, target_folder)
