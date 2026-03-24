# hippokampus
Local AI assistant that reads and answers questions about your Notion

## Why
Notion already has AI features that do more than this, but it is limited

## Requirements
### Ollama
[Ollama](https://ollama.com/) is a free, open-source framework designed to run large language models locally or access cloud models

### Notion
[Notion](https://www.notion.com/) is an all-in-one digital workspace that combines note-taking, document collaboration, project management, and databases into a single, customizable platform

## Setup

### Get Notion token
Go to [Notion integrations](https://www.notion.so/profile/integrations/internal) and click "Create a new integration".
Name it whatever you want, but remember it. Choose a work space where you want hippokampus to be able to access. Remember to grab the token.

### Enable hippokampus in Notion
Go to any Notion page in the workspace selected above. Click the triple dots, connections, and enable the integration that was just created.


### Clone the repository
```bash
git clone https://github.com/Aiden-Jun/hippokampus.git
cd hippokampus
```

### Create venv and set it up
#### MacOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
#### Windows
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Run
```bash
python main.py
```