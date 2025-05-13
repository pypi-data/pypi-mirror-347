"AWS helper functions to access the case from S3 bucket."

from pathlib import Path
import hashlib
import shutil

import boto3
from botocore.config import Config
from botocore import UNSIGNED


def get_aws_unsigned_client() -> boto3.client:
    return boto3.client("s3", config=Config(signature_version=UNSIGNED))


def fix_aws_prefix(prefix: str) -> str:
    if not prefix.endswith("/"):
        prefix += "/"
    return prefix


def is_aws_prefix_exist(prefix: str, bucket_name: str, client: boto3.client) -> bool:
    response = client.list_objects_v2(Bucket=bucket_name, Prefix=prefix, MaxKeys=1)
    return isinstance(response, dict) and "Contents" in response


def generate_hash_key(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def download_aws_dir(
    client: boto3.client,
    bucket_name: str,
    prefix: str,
    target: Path,
) -> None:
    paginator = client.get_paginator("list_objects_v2")
    for result in paginator.paginate(Bucket=bucket_name, Prefix=prefix):
        for key in result["Contents"]:
            # Calculate relative path
            rel_path = key["Key"][len(prefix) :]

            # Skip paths ending in /
            if not key["Key"].endswith("/"):
                local_file_path = target / rel_path
                local_file_path.parent.mkdir(parents=True, exist_ok=True)
                client.download_file(bucket_name, key["Key"], str(local_file_path))


def cached_download_aws_dir(
    client: boto3.client,
    bucket_name: str,
    prefix: str,
    target: Path,
    cache_dir: Path = Path.home() / "cadet",
):
    key_name = generate_hash_key(prefix)
    cache_folder = cache_dir / key_name
    target_folder = target / prefix
    target_folder.mkdir(parents=True, exist_ok=True)
    if cache_folder.exists():
        shutil.copytree(cache_folder, target_folder, dirs_exist_ok=True)
        return
    download_aws_dir(client, bucket_name, prefix, cache_folder)
    shutil.copytree(cache_folder, target_folder, dirs_exist_ok=True)
