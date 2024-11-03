# GitPT

## Using GitPT Commit CLI

The `gitpt commit` command helps you generate meaningful commit messages for your git changes. Here's how to use it:

1. **Basic Usage**
   ```bash
   gitpt commit
   ```
 ```bash
   # Generate commit message with custom style
   gitpt commit --style professional

   # Specify maximum length for commit message
   gitpt commit --length 50 
   ```

3. **Examples**
   ```bash
   # Basic commit
   gitpt commit

   # Conversational style with 50 char limit
   gitpt commit --style professional --length 50

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

4. **Configure Environment Variables**
   - Create a `.env` file in the root directory of the project.

### Available Environment Variables
| Environment Variable | Description | Default Value |
|---------------------|-------------|---------------|
| GITPT__LLM | LLM provider selection (ollama, openai, claude, google) | ollama |
| GITPT__MODEL | Model name to use | gemma2 |
| GITPT__OPENAI_API_KEY | OpenAI API key for using OpenAI models | None |
| GITPT__CLAUDE_API_KEY | Claude API key for using Anthropic models | None |
| GITPT__GOOGLE_API_KEY | Google API key for using Google models | None |
| GITPT__STYLE | Style of generated commit messages | professional |
| GITPT__LENGTH | Maximum length of commit messages | 72 |   - Adjust the values according to your needs and API access.

5. **Run GitPT**
   - To interact with the CLI, type `gitpt`
   - Use `gitpt --help` to see available options and commands. 

---