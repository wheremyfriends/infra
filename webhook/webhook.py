import logging
import subprocess

from fastapi import FastAPI, Request

from .client import deploy_frontend

logging.basicConfig()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

app = FastAPI()


BACKEND_REPONAME = "wheremyfriends/webapp"
FRONTEND_REPONAME = "wheremyfriends/nusmods"


@app.post("/postreceive")
async def receive_json(request: Request):
    json_data = await request.json()

    if "action" not in json_data or json_data["action"] != "completed":
        return {"message": "JSON data received successfully"}

    repo_name = json_data["repository"]["full_name"]

    if repo_name == FRONTEND_REPONAME:
        deploy_frontend(json_data)
    elif repo_name == BACKEND_REPONAME:
        subprocess.run(["sudo", "systemctl", "restart", "wamf-backend"])

    return {"message": "JSON data received successfully"}


def main():
    import uvicorn

    uvicorn.run(app, port=8000)


if __name__ == "__main__":
    main()
