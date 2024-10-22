from setuptools import setup


setup(
    name="gitpt",
    version="0.1",
    py_modules=['gitpt', 'spinner'],
    install_requires=["Click"],
    entry_points={
        'console_scripts':[
            'gitpt = gitpt:commit'
        ]
    }

)