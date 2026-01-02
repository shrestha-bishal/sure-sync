# sure-sync
Sync OFX and CSV transactions files to the Sure (Maybe) Finance.

`Sure Sync` is a Docker-based, localised automation service that simplifies importing bank transactions into the ~~Maybe~~ `Sure` finance platform. It is ideal for users whose banks do not provide public APIs, offering a secure, file-driven workflow for financial data while keeping all sensitive credentials local.

## Key Workflow:
- Consume OFX files – Reads exported bank statements from a local consume folder for processing.
- Account mapping – Maps bank accounts to Sure accounts using a user-defined YAML configuration.
- Deduplication – Checks for and skips transactions that have already been processed to prevent duplicates.
- Transaction creation – Creates new transactions in ~~Maybe~~ Sure automatically.
- Archiving – Moves processed OFX files to a local archive folder for record-keeping.
- Localised control – Users maintain full control of credentials, configuration, and data without storing secrets in the repository.


## Features
- Localised, file-based workflow (no need for bank APIs)  
- Docker-first deployment  
- Automatic deduplication of transactions  
- Easy account mapping through YAML  
- Secure: credentials are never committed to GitHub  

## Prerequisites
- Docker  
- Docker Compose  
- A Sure account with API access  
- OFX files exported from your bank  


---

## Quick Start

- Clone the repository
```bash
git clone https://github.com/shrestha-bishal/sure-sync.git
cd sure-sync
```
- Configure environment variables
```bash
cp .env.example .env
```
Edit `.env` to set your Sure API credentials and folder paths.

- Configure account mapping
```bash
cp account-mapping.example.yml account-mapping.yml
```
Edit `account-mapping.yml` to map your OFX accounts to Sure accounts. Keep this file gitignored.

- Start the service
```bash
docker compose up -d
```
The service will automatically process any OFX files in the **consume/** folder.

### Contributing
- Fork the repo, make changes, and submit a pull request.
- Report bugs or feature requests via GitHub issues.

### License
MIT License. See [LICENSE](./LICENSE)  for details.

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