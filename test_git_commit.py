import argparse

from langchain_core.prompts import PromptTemplate
from langchain_ollama.llms import OllamaLLM
import subprocess

MODEL = 'gemma2'
TEMP = 0
TOP_P = 0.5
TOP_K = 10
ollama_model = OllamaLLM(model=MODEL, temperature=TEMP, top_p=TOP_P, top_k=TOP_K)


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
    git diff, a list of new files added, and a list of files renamed. 
    git diff: {git_diff}
    
    If the new files list or the renamed files list just says the word none, please ignore those respective changes in 
    the summary. If a deleted file shows up in the renamed files list, treat the deleted file as a renamed file in the
    summary.
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
    parser.add_argument('--new_files')
    parser.add_argument('--renamed_files')
    parser.add_argument('--style', '-s', default='prompt_0')

    return parser.parse_args()


def generate_concise_message(verbose_msg, num_of_chars):

    prompt = PromptTemplate(
        input_variables=['char_length', 'verbose_summary'],
        template=char_prompt
    )

    code_summary_chain = prompt | ollama_model
    concise_summary = code_summary_chain.invoke({
        'char_length': num_of_chars,
        'verbose_summary': verbose_msg
    })

    return concise_summary


def generate_verbose_message(diff_files, prompt_txt=prompt_0):

    

    prompt = PromptTemplate(
        input_variables=["git_diff"],
        template=prompt_txt
    )

    code_summary_chain = prompt | ollama_model
    verbose_summary = code_summary_chain.invoke({
        "git_diff": diff_files
    })

    return verbose_summary


def read_file(ext_file):

    file_input = ''

    if ext_file is not None:

        with open(ext_file) as f:

            file_input = f.read()

    return file_input

if __name__ == "__main__":

    params = create_parser()
    if read_file(params.diff):
        change_input = [read_file(params.diff), read_file(params.new_files), read_file(params.renamed_files)]
    else:
        # diff = new_files = renamed_files = None
        bash_script = "./get_diffs.sh"
        result = subprocess.run([bash_script], capture_output=True, text=True, shell=True)

        if result.returncode == 0:
            output = result.stdout.strip()
            sections = output.split("\n\n")
            if len(sections)>=1:
                diff = sections[0]
            if len(sections) >= 2:
                new_files = sections[1]
            if len(sections) >= 3:
                renamed_files = sections[2]
        else:
            print("Error getting git diffs:")
            print(result.stderr)

        # change_input = [diff,new_files,renamed_files]
    #print(change_input)
    print(f'Using the following style: {params.style}')
    verbose_message = generate_verbose_message(result, prompt_dict[params.style])

    if params.length != 'verbose':

        print(f'Character length of commit message - {params.char_length}')
        commit_message = generate_concise_message(verbose_message, params.char_length)

    else:

        commit_message = verbose_message

    print(commit_message)
