# hackathon-4
Hackathon 4 - October 2024

1. Download ollama from https://ollama.com/
2. In the terminal run `ollama pull gemma2`
   ( the model will be downloaded into `~/.ollama/models/blobs` on mac)
3. Create virtual environment for python: `python -m venv venv`
4. Activate virtual environemnt: `source venv/bin/activate`
5. Install requirements: `pip install -r requirements.txt`
6. CD into folder of project
7. Install project into venv `pip install .` Setup file will create keyword to utilize cli
8. Type `gitpt` to interact with cli, `gitpt --help` to see available options to pass.