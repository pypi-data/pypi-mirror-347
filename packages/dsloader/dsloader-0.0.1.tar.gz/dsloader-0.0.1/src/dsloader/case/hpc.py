"Extract cached copy of the data from HPC machine to local machine."

from pathlib import Path
import shutil

import paramiko
from scp import SCPClient

from dsloader.case.aws import generate_hash_key


# TODO: If possible we want to show progress bar for download
def cached_copy_hpc_dir(
    hostname: str,
    username: str,
    password: str,
    source: Path,
    target: Path,
    base_folder: Path,
    cache_dir: Path = Path.home() / "cadet",
):
    """
    Copy a folder from an HPC machine to a local target directory.

    Parameters
    ----------
    hostname : str
        The hostname of the HPC machine.
    username : str
        The username to use for the SSH connection.
    password : str
        The password to use for the SSH connection.
    source : Path
        The path to the folder to copy from the HPC machine.
    target : Path
        The path to the target directory to copy the folder to.
    base_folder : Path
        The base folder on the HPC machine where the source folder is located.
    cache_dir : Path, optional
        The path to the cache directory to use. If the cache folder exists, it will be
        copied from the cache instead of from the HPC machine. By default, it is
        located at `~/.cadet`.

    Returns
    -------
    None
    """
    key_name = generate_hash_key(str(source))
    target_folder = target / source
    target_folder.mkdir(parents=True, exist_ok=True)
    if not cache_dir.exists():
        cache_dir.mkdir(parents=True)
    cache_folder = cache_dir / key_name
    if cache_folder.exists():
        shutil.copytree(cache_folder, target_folder, dirs_exist_ok=True)
        return

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, username=username, password=password)
    source_dir = base_folder / source
    with SCPClient(ssh.get_transport()) as scp:
        scp.get(source_dir.as_posix(), str(cache_folder), recursive=True)
    shutil.copytree(cache_folder, target_folder, dirs_exist_ok=True)
