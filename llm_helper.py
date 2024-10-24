from langchain_core.prompts import PromptTemplate
import os

class CommentGenerator():
    def __init__(self, model):
        self.model = model
        self.TEMP = 0
        self.TOP_P = 0.5
        self.TOP_K = 10
        self.llm = self.set_model(self.model)

    
    def set_model(self, model):
        if model == "chat-gpt":
        # Check for API Key
            if os.environ.get("OPENAI_API_KEY"):

                from langchain_openai.llms import OpenAI

                llm = OpenAI(model='gpt-3.5-turbo-instruct', 
                            temperature=self.TEMP,
                            api_key = os.environ.get("OPENAI_API_KEY"),
                            top_p = self.TOP_P
                            )
                return llm
            else:
                print(f"Failed to get API Key, using Ollama")

        # Use Ollama if no other model passed in
        from langchain_ollama.llms import OllamaLLM

        llm = OllamaLLM(model='gemma2', 
                        temperature=self.TEMP, 
                        top_p=self.TOP_P, 
                        top_k=self.TOP_K
                        )
            
        return llm
    
    def generate_short_message(self, verbose_msg:str, num_of_chars:int, short_prompt:str, style:str) -> str:
        """Run git diff verbose summary against llm for a small concise message

        Args:
            verbose_msg (str): Summary from first llm response
            num_of_chars (int): Length of message to return
            short_prompt (str): Short message prompt to send to llm

        Returns:
            _type_: _description_
        """

        prompt = PromptTemplate(
        input_variables=['char_length', 'verbose_summary', 'style'],
        template=short_prompt
        )

        code_summary_chain = prompt | self.llm
        summary = code_summary_chain.invoke({
            'char_length': num_of_chars,
            'verbose_summary': verbose_msg,
            'style':style
        })

        return summary


    def generate_verbose_message(self, diff_file:str, style:str, prompt_txt:str) -> str:
        """_summary_

        Args:
            diff_file (str): Contents of git diff
            style (str): Style of response to be generated
            prompt_txt (str): Prompt to be use to generate response

        Returns:
            str: LLM summary of git diff file.
        """
        prompt = PromptTemplate(
            input_variables=["git_diff", "style"],
            template=prompt_txt
        )

        llm = self.llm

        code_summary_chain = prompt | llm
        summary = code_summary_chain.invoke({
            "git_diff": diff_file,
            "style": style
        })

        return summary