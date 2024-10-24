from setuptools import setup


setup(
    name="gitpt",
    version="0.1",
    py_modules=['gitpt', 'spinner', 'test_git_commit'],
    install_requires=["Click", "langchain-ollama"],
    entry_points={
        'console_scripts':[
            'gitpt = gitpt:create_message'
        ]
    }

)