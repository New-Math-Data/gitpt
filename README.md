# GitPT

## Overview
Welcome to the repo for GitPT, the command line utility that uses an LLM to generate git commit messages for you. Save your brain cycles for something other than writing meaningful commit messages. Choose from LLMs installed on your machine or use API access. Select the message style that matches your codebase and personality: professional, funny, or intrinsic.

Remember: LLMs are used to generate the messages. LLMs make mistakes. Verify all responses created by GitPT

## Common Scenarios
If you’d like to get the repo working on your machine, follow [these steps](#setup-your-machine-for-development).

## Setup Your Machine for Development

### Assumptions
1. You already have Git installed and working.
1. You are familiar with Python and creating virtual environments.
1. You are able to access a LLM (either locally or with an API key). 

### Decide about LLM Access
**If you prefer a local LLM**
Be sure your machine can handle the system requirements. Specifics in the [Ollama documentation](https://github.com/ollama/ollama/blob/main/README.md#quickstart). 
   - Download [Ollama](https://ollama.com/) and install it. 
   - Follow the Ollama instructions for pulling gemma2.
      - For Mac, run `ollama pull gemma2` in the Terminal and wait for the model to be downloaded into `~/.ollama/models/blobs`

**If you prefer API Access**

Use the developer documentation to review the API pricing and obtain your API key. For example, at the time of writing, Gemini allows 1,500 requests per day free. 

### Steps

1. **Use Git to Clone this Repo**
   
1. **Set Up Python Virtual Environment and Install Poetry**
   - Follow the [venv directions](https://docs.python.org/3/library/venv.html) for creating a virtual environment. For example: `python -m venv venv`
   - Activate the virtual environment: `source venv/bin/activate`
   - If Poetry is not installed, install it.  For example: `pip install poetry`

1. **Install Project Dependencies**
   - CD into the project folder.
   - Use Poetry to install the project in editable mode: `poetry install`
   - This will install the dependencies specified in `pyproject.toml` and set up the project for CLI use.

1. **Configure Environment Variables**
   - Create a `.env` file in the root directory of the project. See [Available Environment Variables](#available-environment-variables).

1. **Run GitPT**
   - To interact with the CLI, type `gitpt`
   - Use `gitpt --help` to see available options and commands.
   - See additional [Usage Instructions](#usage-instructions)  

## Usage Instructions

The `gitpt commit` command helps you generate meaningful commit messages for your Git changes. Here's how to use it:

1. **Basic Usage**
   ```bash
   gitpt commit
   ```
 ```bash
   # Generate commit message with custom style
   gitpt  --style professional commit

   # Specify maximum length for commit message
   gitpt --length 50 commit 
   ```

3. **Examples**
   ```bash
   # Basic commit
   gitpt commit

   # Conversational style with 50 char limit
   gitpt --style professional --length 50 commit


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

---
