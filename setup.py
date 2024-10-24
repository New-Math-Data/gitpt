from setuptools import setup


setup(
    name="gitpt",
    version="0.1",
    py_modules=['gitpt', 'spinner', 'llm_helper'],
    install_requires=["Click", "langchain-ollama", "langchain-openai"],
    entry_points={
        'console_scripts':[
            'gitpt = gitpt:create_message'
        ]
    }

)