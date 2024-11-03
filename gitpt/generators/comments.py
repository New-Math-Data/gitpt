import logging

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


log = logging.getLogger(__name__)


class BaseCommentGenerator:
    def __init__(self, model):
        self.model = model
        self.TEMP = 0.8
        self.TOP_P = 0.9
        self.TOP_K = 40
        self.generator = self.create_generator()

    def create_generator(self):
        from langchain_ollama import ChatOllama

        generator = ChatOllama(
            model=self.model, temperature=self.TEMP, top_p=self.TOP_P, top_k=self.TOP_K
        )
        return generator

    def generate_message(
        self,
        git_diff: str,
        style: str,
        summary_prompt: str,
        message_prompt: str,
        length: int,
    ) -> str:
        """_summary_

        Args:
            diff_file (str): Contents of git diff
            style (str): Style of response to be generated
            prompt_txt (str): Prompt to be use to generate response

        Returns:
            str: LLM summary of git diff file.
        """
        summary = ChatPromptTemplate.from_messages(
            [("system", summary_prompt), ("human", "{git_diff}")]
        )

        message = ChatPromptTemplate.from_messages(
            [("system", message_prompt), ("human", "{summary}")]
        )

        summary_out = StrOutputParser()

        code_summary_chain = summary | self.generator | summary_out
        summary_op = code_summary_chain.invoke({"git_diff": git_diff})

        code_commit_chain = message | self.generator | summary_out
        commit = code_commit_chain.invoke(
            {"style": style, "summary": summary_op, "char_length": length}
        )

        return commit


class OpenAICommentGenerator(BaseCommentGenerator):
    def __init__(self, model, api_key):
        self.api_key = api_key
        super().__init__(model)

    def create_generator(self):
        if self.api_key != "":
            from langchain_openai import ChatOpenAI

            try:
                generator = ChatOpenAI(
                    model=self.model,
                    temperature=self.TEMP,
                    api_key=self.api_key,
                    top_p=self.TOP_P,
                )
                return generator
            except Exception as e:
                log.error(f"Error: {e}")
                self.model = "gemma2"
                return super().create_generator()
        else:
            log.error("Failed to get API Key, using Ollama with Gemma2")
            self.model = "gemma2"
            return super().create_generator()


class ClaudeCommentGenerator(BaseCommentGenerator):
    def __init__(self, model, api_key):
        self.api_key = api_key
        super().__init__(model)

    def create_generator(self):
        if self.api_key != "":
            from langchain_anthropic import ChatAnthropic

            try:
                generator = ChatAnthropic(
                    model=self.model,
                    temperature=self.TEMP,
                    api_key=self.api_key,
                    top_p=self.TOP_P,
                    top_k=self.TOP_K,
                )
                return generator
            except Exception as e:
                log.error(f"Error: {e}")
                self.model = "gemma2"
                return super().create_generator()
        else:
            log.error("Failed to get API Key, using Ollama with Gemma2")
            self.model = "gemma2"
            return super().create_generator()


class GeminiCommentGenerator(BaseCommentGenerator):
    def __init__(self, model, api_key):
        self.api_key = api_key
        super().__init__(model)

    def create_generator(self):
        if self.api_key != "":
            from langchain_google_genai import ChatGoogleGenerativeAI

            try:
                generator = ChatGoogleGenerativeAI(
                    model=self.model,
                    temperature=self.TEMP,
                    api_key=self.api_key,
                    top_p=self.TOP_P,
                    top_k=self.TOP_K,
                )
                return generator
            except Exception as e:
                log.error(f"Error: {e}")
                self.model = "gemma2"
                return super().create_generator()
        else:
            log.error("Failed to get API Key, using Ollama with Gemma2")
            self.model = "gemma2"
            return super().create_generator()
