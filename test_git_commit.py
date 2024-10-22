from langchain_core.prompts import PromptTemplate
from langchain_ollama.llms import OllamaLLM
import sys

def generate_commit_message(git_diff):
    model= OllamaLLM(model="gemma2",temperature=0, top_p=0.5, top_k=10)

    prompt_template = """
    Write concise, informative commit messages based on git diff: 
    Start with a summary in imperative mood, explain the 'why' behind changes, 
    keep the summary under 50 characters. 
    Use bullet points for multiple changes, and reference related issues or tickets. 
    What you write will be passed to git commit -m "[message]"
    git_diff: {git_diff}
    """

    prompt = PromptTemplate(
        input_variables=["git_diff"],
        template=prompt_template
    )

    code_summary_chain  = prompt | model
    commit_message = code_summary_chain.invoke(git_diff)
    return commit_message


if __name__ == "__main__":
  #git_diff = sys.argv[1]
  file = open("diff.txt", "r")
  git_diff = file.read()
  file.close()
  print(generate_commit_message(git_diff))