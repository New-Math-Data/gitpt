from llm_helper import CommentGenerator
import subprocess


with open("./prompts/prompt_txt.md", "r") as prompt:
    prompt_txt = prompt.read()
    prompt.close()

generator = CommentGenerator("Ollama")
diff_text = subprocess.run(
    ["./get_diffs.sh"], capture_output=True, text=True, shell=True
)

# print(prompt_txt)
style = "funny"
# style = "imperative"
# style = "professional"

verbose_message = generator.generate_verbose_message(diff_text, style, prompt_txt)

print(verbose_message)
with open("./prompts/small_prompt.md", "r") as sp:
    short_prompt = sp.read()
    sp.close()

# print(short_prompt)
length = 50
concise_message = generator.generate_short_message(
    verbose_message, length, short_prompt, style
)
print(concise_message)
