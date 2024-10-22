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


def generate_commit_message(git_diff, prompt_txt):

    model = OllamaLLM(model="gemma2", temperature=0, top_p=0.5, top_k=10)

    prompt = PromptTemplate(
        input_variables=["git_diff"],
        template=prompt_txt
    )

    code_summary_chain = prompt | model
    commit_message = code_summary_chain.invoke(git_diff)

    return commit_message


if __name__ == "__main__":

    prompt_style = sys.argv[1]

    file = open("test_data/diff.txt", "r")
    diff_input = file.read()
    file.close()

    commit_msg = generate_commit_message(diff_input, prompt_style)

    print(commit_msg)
