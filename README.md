# hackathon-4

Hackathon 4 - October 2024

1. `chmod +x commit.sh`
1. `chmod +x get_diffs.sh`
1. Download ollama from https://ollama.com/
1. In the terminal run `ollama pull gemma2`
   ( the model will be downloaded into `~/.ollama/models/blobs` on mac)
1. Create virtual environment for python: `python -m venv venv`
1. Activate virtual environemnt: `source venv/bin/activate`
1. Install requirements: `pip install -r requirements.txt`
1. CD into folder of project
1. Install project into venv `pip install --editable .` Setup file will create keyword to utilize cli
1. Type `gitpt` to interact with cli, `gitpt --help` to see available options to pass.
