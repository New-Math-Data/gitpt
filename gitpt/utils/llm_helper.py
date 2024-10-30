from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

class CommentGenerator():
    def __init__(self, llm, model, api_key):
        self.llm = llm
        self.model = model
        self.TEMP = 0.8
        self.TOP_P = 0.9
        self.TOP_K = 40
        self.api_key = api_key
        self.generator = self.create_generator()
        

    
    def create_generator(self):
        if self.llm == "openai":
        # Check for API Key
            if self.api_key != '':
                from langchain_openai import ChatOpenAI

                try:
                    generator = ChatOpenAI(model=self.model, 
                                temperature=self.TEMP,
                                api_key = self.api_key,
                                top_p = self.TOP_P
                                )
                    return generator
                except Exception as e:
                    print(f"Error: {e}")
                
            else:
                print(f"Failed to get API Key, using Ollama with Gemma2")
                self.model = 'gemma2'

        elif self.llm == "claude":
            # Check for API Key
            if self.api_key != '':
                from langchain_openai import ChatAnthropic

                try:
                    generator = ChatAnthropic(
                        model=self.model,
                        temperature = self.TEMP,
                        api_key = self.api_key,
                        top_p = self.TOP_P,
                        top_k = self.TOP_K
                    )
                    return generator
                except Exception as e:
                    print(f"Error: {e}")
            else:
                print(f"Failed to get API Key, using Ollama with Gemma2")
                self.model = 'gemma2'

        # Use Ollama if no other model passed in
        from langchain_ollama import ChatOllama

        generator = ChatOllama(model=self.model, 
                        temperature=self.TEMP, 
                        top_p=self.TOP_P, 
                        top_k=self.TOP_K
                        )
            
        return generator


    def generate_message(self, git_diff:str, style:str, summary_prompt:str, message_prompt:str, length:int) -> str:
        """_summary_

        Args:
            diff_file (str): Contents of git diff
            style (str): Style of response to be generated
            prompt_txt (str): Prompt to be use to generate response

        Returns:
            str: LLM summary of git diff file.
        """


        summary = ChatPromptTemplate.from_messages([
            (
                "system",
                summary_prompt
            ),
            ("human", "{git_diff}")
        ])

        message = ChatPromptTemplate.from_messages([
            (
                "system",
                message_prompt
            ),
            ("human", "{summary}")
        ])

        summary_out = StrOutputParser()

        code_summary_chain = summary | self.generator | summary_out
        summary_op = code_summary_chain.invoke({
            "git_diff": git_diff
        })

        code_commit_chain = message | self.generator | summary_out
        commit = code_commit_chain.invoke({
            "style":style,
            "summary":summary_op,
            "char_length":length
        })

        return commit