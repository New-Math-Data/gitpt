from langchain_core.prompts import PromptTemplate
from langchain_ollama.llms import OllamaLLM
import sys


prompt_1 = """
    Write concise, informative commit messages based on git diff: 
    Start with a summary in imperative mood, explain the 'why' behind changes, 
    keep the summary under 50 characters. 
    Use bullet points for multiple changes, and reference related issues or tickets. 
    What you write will be passed to git commit -m "[message]"
    git_diff: {git_diff}
    """

prompt_0 = """
    You are a programming expert. Please provide a concise summary of the following code snippet:
    Code:
    {git_diff}
    
    Summary:
    """

prompt_dict = {'prompt_0': prompt_0, 'prompt_1': prompt_1}


def generate_commit_message(diff_files, prompt_txt):

    print(prompt_text)

    git_diff = diff_files[0]

    model = OllamaLLM(model="gemma2", temperature=0, top_p=0.5, top_k=10)

    prompt = PromptTemplate(
        input_variables=["git_diff"],
        template=prompt_txt
    )

    code_summary_chain = prompt | model
    commit_message = code_summary_chain.invoke(git_diff)

    return commit_message


def read_file(ext_file):

    with open(ext_file) as f:

        file_input = f.read()

    return file_input


if __name__ == "__main__":

    prompt_style = sys.argv[1]

    change_input = [read_file(file) for file in sys.argv[2:]]

    commit_msg = generate_commit_message(change_input, prompt_dict[prompt_style])

    print(commit_msg)
