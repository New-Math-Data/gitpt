# GitPT

## History
Hackathon 4 - October 2024

## Development Instructions

1. **Download the Model**
   - Download Ollama from [https://ollama.com/](https://ollama.com/)
   - In the terminal, run `ollama pull gemma2`  
     (The model will be downloaded into `~/.ollama/models/blobs` on Mac)

2. **Set Up Python Virtual Environment and Install Poetry**
   - Create a virtual environment: `python -m venv venv`
   - Activate the virtual environment: `source venv/bin/activate`
   - Install Poetry if it’s not already installed: `pip install poetry`

3. **Install Project Dependencies**
   - CD into the project folder.
   - Use Poetry to install the project in editable mode: `poetry install`
   - This will install the dependencies specified in `pyproject.toml` and set up the project for CLI use.

4. **Run GitPT**
   - To interact with the CLI, type `gitpt`
   - Use `gitpt --help` to see available options and commands. 

---