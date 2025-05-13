from setuptools import setup, find_packages

setup(
    name = 'CODEval-Benchmark',
    version = '1.1.0',
    packages= find_packages(),
    install_requires = [
        'langchain',
        'langchain-core',
        'langchain-ollama',
        'langchain-text-splitters',
        'langsmith'
    ],
    description="A Benchmark used to evaluate small large language models.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",  
    entrt_points = {
        "console_scripts":[
            "CODEval = CODEval.About:about"
        ]
    }
)