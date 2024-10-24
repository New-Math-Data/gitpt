from langchain_core.prompts import PromptTemplate
import os

def set_model(model):
    TEMP = 0
    TOP_P = 0.5
    TOP_K = 10
    if model == "chat-gpt":
        # Check for API Key
        if os.environ.get("OPENAI_API_KEY"):

            from langchain_openai.llms import OpenAI

            llm = OpenAI(model='gpt-3.5-turbo-instruct', 
                        temperature=TEMP,
                        api_key = os.environ.get("OPENAI_API_KEY"),
                        top_p = TOP_P
                        )
            return llm
        else:
            print(f"Failed to get API Key, using Ollama")

    # Use Ollama if no other model passed in
    from langchain_ollama.llms import OllamaLLM

    llm = OllamaLLM(model='gemma2', 
                    temperature=TEMP, 
                    top_p=TOP_P, 
                    top_k=TOP_K
                    )
        
    return llm

prompt_2 = """
# IDENTITY and PURPOSE

You are an expert project manager and developer, and you specialize in creating {style} changed in a Git diff.

# STEPS

- Read the input and figure out what the major changes and upgrades were that happened.

- Create a message that can be included within a git command to reflet the changes.

- If there are a lot of changes include more bullets. If there are only a few changes, be more terse.

# OUTPUT INSTRUCTIONS

- Use conventional commits - i.e. prefix the commit title with "chore:" (if it's a minor change like refactoring or linting), "feat:" (if it's a new feature), "fix:" if its a bug fix

- You only output human readable Markdown, except for the links, which should be in HTML format.

- The output should be a message that will be included as part of a git command.

- You can use write the message in a {style} manner.

# INPUT:

INPUT: {git_diff}
"""


prompt_1 = """
    Write concise, informative commit messages based on git diff: 
    Start with a summary in imperative mood, explain the 'why' behind changes, 
    keep the summary under 50 characters. 
    Use bullet points for multiple changes, and reference related issues or tickets. 
    What you write will be passed to git commit -m "[message]"
    git_diff: {git_diff}
    """

prompt_0 ="""
    You are a programming expert. Please provide a concise summary of the following code changes. I will provide the
    git diff. 
    git diff: {git_diff}
    """

char_prompt = """
    Please summarize this message into {char_length} characters or less:
    {verbose_summary}
    """

prompt_dict = {'prompt_0': prompt_0, 'prompt_1': prompt_1}


def create_parser():

    parser = argparse.ArgumentParser()

    parser.add_argument('--char_length', '-c', default='50')
    parser.add_argument('--diff', '-d')
    parser.add_argument('--length', '-l', default='concise')
    parser.add_argument('--style', '-s', default='prompt_0')

    return parser.parse_args()


def generate_concise_message(verbose_msg, num_of_chars, model):

    prompt = PromptTemplate(
        input_variables=['char_length', 'verbose_summary'],
        template=char_prompt
    )

    llm = set_model(model)

    code_summary_chain = prompt | llm
    concise_summary = code_summary_chain.invoke({
        'char_length': num_of_chars,
        'verbose_summary': verbose_msg
    })

    return concise_summary


def generate_verbose_message(diff_files, style, model, prompt_txt=prompt_2):

    

    prompt = PromptTemplate(
        input_variables=["git_diff", "style"],
        template=prompt_txt
    )

    llm = set_model(model)

    code_summary_chain = prompt | llm
    verbose_summary = code_summary_chain.invoke({
        "git_diff": diff_files,
        "style": style
    })

    return verbose_summary


def read_file(ext_file):

    file_input = ''

    if ext_file is not None:

        with open(ext_file) as f:

            file_input = f.read()

    return file_input

if __name__ == "__main__":
    import subprocess
    import argparse

    params = create_parser()
    if read_file(params.diff):
        change_input = read_file(params.diff)
    else:
        bash_script = "./get_diffs.sh"
        change_input = subprocess.run([bash_script], capture_output=True, text=True, shell=True)

    print(f'Using the following style: {params.style}')

    verbose_message = generate_verbose_message(change_input, prompt_dict[params.style])

    if params.length != 'verbose':

        print(f'Character length of commit message - {params.char_length}')
        commit_message = generate_concise_message(verbose_message, params.char_length)

    else:

        commit_message = verbose_message

    print(commit_message)
