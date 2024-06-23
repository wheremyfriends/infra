import subprocess


def deploy_backend():
    cmds = [
        ["docker", "compose", "pull"],
        ["docker", "compose", "up", "-d"],
    ]

    for cmd in cmds:
        subprocess.run(cmd)
