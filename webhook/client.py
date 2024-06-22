import logging
import subprocess
from datetime import datetime
from pathlib import Path

import requests
from dotenv import dotenv_values

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


config = dotenv_values(".env.client")
API_KEY = config["GITHUB_API_KEY"]

ARTIFACT_NAME = "github-pages"
DST = Path("/var/www/wamf")
BACKUP_FOLDER = Path("~/bak").expanduser()
INTERMEDIATE_FILENAME = "github-pages.tar.gz"


def getcurtime():
    # Get the current datetime
    now = datetime.now()

    # Format the datetime as YYYYMMDD_HHMM
    return now.strftime("%Y%m%d_%H%M")


def get_archive_url(artifacts: list[dict]) -> str:
    for artifact in artifacts:
        if artifact["name"] == ARTIFACT_NAME:
            return artifact["archive_download_url"]
    return None


def deploy_frontend(msg: dict):
    logger.info("Deploying frontend")

    # Download the archive
    artifact_url = msg["workflow_run"]["artifacts_url"]
    logger.info("Artifact URL: %s", artifact_url)

    session = requests.Session()

    # Set headers for the session
    session.headers.update(
        {
            "Authorization": f"Bearer {API_KEY}",
            "X-GitHub-Api-Version": "2022-11-28",
        }
    )

    # Get artifact information
    resp = session.get(artifact_url).json()

    archive_download_url = get_archive_url(resp["artifacts"])

    logger.info("Downloading %s from %s", ARTIFACT_NAME, archive_download_url)
    artifact = session.get(archive_download_url)

    with open(INTERMEDIATE_FILENAME, "wb") as f:
        f.write(artifact.content)
    logger.info("Downloaded %s to %s", ARTIFACT_NAME, INTERMEDIATE_FILENAME)

    logger.info("Backup existing frontend")
    # Backup old files
    now = getcurtime()
    if not BACKUP_FOLDER.exists():
        BACKUP_FOLDER.mkdir(parents=True, exist_ok=True)
    backup_loc = BACKUP_FOLDER / f"wamf_{now}"
    subprocess.run(["sudo", "mv", DST, backup_loc])

    logger.info("Deploying new code")
    subprocess.run(["sudo", "mkdir", "-p", DST])
    subprocess.run(["sudo", "tar", "-xf", INTERMEDIATE_FILENAME, "-C", DST])
