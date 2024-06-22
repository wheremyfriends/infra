# Infrastructure

## Getting started

- Install ansible
- Install dependencies
    ```bash
    ansible-galaxy collection install community.general
    ```

- Set up the private key paths in the `hosts` file

- Run `ansible-playbook`,
  the password is ********.
  ```bash
  ansible-playbook -i hosts -e @secrets.enc --ask-vault-pass dev.yaml
  ```

## Architecture

- `frontend`
    - Located in `/var/www/wamf`
- `backend` 
    - `compose.yaml` located in `~/infra`
    - Port 4000
- `wamf-webhook`
    - Managed by `systemd`
    - Port 8000

Caddy is used as reverse proxy

## Directory Structure on Production

```
~/
├─ infra/
│  ├─ webhook/
│  │  ├─ webhook.py
│  │  ├─ client.py
│  ├─ compose.yaml
```

- `webhook/` to listen for changes in the repo,
  and redeploy on notify.
