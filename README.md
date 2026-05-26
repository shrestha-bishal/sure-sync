<img width="1920" height="959" alt="image" src="https://github.com/user-attachments/assets/f657ba20-fdb8-418a-b54e-904bffd05cdc" /># sure-sync
Sync OFX transactions files to the Sure (Maybe) Finance.

`Sure Sync` is a Docker-based, localised automation service that simplifies importing bank transactions into the ~~Maybe~~ `Sure` finance platform. It is ideal for users whose banks do not provide public APIs, offering a secure, file-driven workflow for financial data while keeping all sensitive credentials, configuration, and data local.

The current release includes a web dashboard for live status, processing statistics, and account mapping management.

## Key Workflow:
- Consume OFX files – Reads exported bank statements from a local consume folder for processing.
- Account mapping – Maps bank accounts to Sure accounts using a user-defined YAML configuration.
- Deduplication – Checks for and skips transactions that have already been processed to prevent duplicates.
- Transaction creation – Creates new transactions in ~~Maybe~~ Sure automatically.
- Archiving – Moves processed OFX files to a local archive folder for record-keeping.
- Localised control – Users maintain full control of credentials, configuration, and data without storing secrets in the repository.

<img width="813" height="293" alt="image" src="https://github.com/user-attachments/assets/980dbeae-1f8d-40ba-8b17-8f18693f4197" />
<img width="651" height="111" alt="image" src="https://github.com/user-attachments/assets/8f4071d4-7ed1-4dd0-9beb-4f958370333b" />
<img width="614" height="48" alt="image" src="https://github.com/user-attachments/assets/80d7c0bb-4dc3-4bf3-91b6-d8578ac891ae" />

## Features
- Localised, file-based workflow (no need for bank APIs)  
- Docker-first deployment  
- Automatic deduplication of transactions  
- Easy account mapping through YAML  
- Web dashboard for monitoring stats and managing account mappings
- Persistent state storage in a host-mounted data directory
- Secure local credentials via `.env`

## Prerequisites
- Docker
- Docker Compose
- Sure account with API access
- Exported OFX files from your bank

---
## Quick Start
- Create the directory 
```bash
mkdir ~/.docker-apps/sure-sync
cd ~/.docker-apps/sure-sync
```

- Download configuration files from the latest release:
> Download the `docker-compose.yml`
```bash
wget -O docker-compose.yml https://github.com/shrestha-bishal/sure-sync/releases/latest/download/docker-compose.yml
```
> Download the `example.env`
```bash
wget -O .env.example https://github.com/shrestha-bishal/sure-sync/releases/latest/download/example.env
```

### Important `.env` variables
| Variable | Description | Example |
|---|---|---|
| `CONSUME_PATH` | Local folder to scan for OFX files | `./consume/` |
| `DATA_PATH` | Host folder for persistent state and stats | `./data/` |
| `API_URL` | Sure API base URL | `http://host.docker.internal:3000/api/v1/` |
| `API_KEY` | Sure API key with read/write access | `your-api-key` |
| `LOOKUP_INTERVAL` | Poll interval for scanning files (seconds) | `5` |

### Service behavior
- The worker service watches `CONSUME_PATH` for OFX files.
- Processed files are moved to `processed/` and failures to `failed/`.
- Account mappings are managed through the web dashboard.

### Web Dashboardc
- Access the dashboard at `http://localhost:9000`
- Use **Settings → Accounts** to add mapped bank accounts
- Dashboard also shows processing statistics and current app state
<img width="1920" height="959" alt="image" src="https://github.com/user-attachments/assets/d407a25f-da07-4f86-a788-fef55887d9bc" />
<img width="1920" height="959" alt="image" src="https://github.com/user-attachments/assets/69460e9b-ce66-4ea6-ac21-2cf0221ead9a" />
<img width="1920" height="959" alt="image" src="https://github.com/user-attachments/assets/277b877f-c54f-434b-8e33-3a92b81305ca" />

> More updates on the way

### Contributing
- Fork the repo, make changes, and submit a pull request.
- Report bugs or feature requests via GitHub issues.

## License
MIT License. See [LICENSE](./LICENSE) for details.

### Funding & Sponsorship
Sure Sync is an open-source tool developed and maintained to automate the import of bank transactions into the Sure finance platform. It simplifies financial data workflows and ensures reliable, localised syncing for users without public bank APIs.

If you or your organisation find this project valuable, please consider supporting its ongoing development. Your sponsorship helps sustain long-term maintenance, improve features, enhance documentation, and maintain compatibility with future Sure API updates while keeping the project free and open for the community.

As a token of appreciation, sponsors may have their logo and link featured in the project README and documentation. Priority support, early access to new features, or custom enhancements may also be offered where appropriate.

### Support Options
[![GitHub Sponsors](https://img.shields.io/badge/GitHub%20Sponsors-Become%20a%20Sponsor-blueviolet?logo=githubsponsors&style=flat-square)](https://github.com/sponsors/shrestha-bishal)  
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-Support%20Developer-yellow?logo=buymeacoffee&style=flat-square)](https://www.buymeacoffee.com/shresthabishal)  
[![Thanks.dev](https://img.shields.io/badge/Thanks.dev-Appreciate%20Open%20Source-29abe0?logo=github&style=flat-square)](https://thanks.dev/gh/shrestha-bishal)  

---

### Author
**Bishal Shrestha**  

[![GitHub](https://img.shields.io/badge/GitHub-Profile-black?logo=github)](https://github.com/shrestha-bishal)  
[![Repo](https://img.shields.io/badge/Repository-GitHub-black?logo=github)](https://github.com/shrestha-bishal/sure-sync)

© 2026 Bishal Shrestha, All rights reserved  
