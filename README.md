# Infrastructure

## Getting started

- Install ansible
- Install dependencies
    ```bash
    ansible-galaxy collection install community.general
    ```

- Set up keys to connect to host (fill up the `hosts` file)
    - Username
    - Private key/Password

- Fill up `secrets.yaml`
    - `cp secrets-example.yaml secrets.yaml`

- Run `ansible-playbook`
```
ansible-playbook -i hosts main.yaml
```

## Services

- `wamf-backend` (port 4000)
- `wamf-webhook` (port 8000)

There are all managed by systemd

## Directory Structure on Production

```
~/
├─ infra/
│  ├─ client/
│  │  ├─ deploy_client.py
│  ├─ webhook/
│  │  ├─ webhook.py
│  ├─ server/
│  │  ├─ compose.yaml
```

- `webhook/` to listen for changes in the repo
- `server/` and `client/` stores the required files to re-deploy the service
