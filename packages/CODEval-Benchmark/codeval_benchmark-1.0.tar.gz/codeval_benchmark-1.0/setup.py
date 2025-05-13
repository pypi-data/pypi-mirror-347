from setuptools import setup, find_packages

setup(
    name = 'CODEval-Benchmark',
    version = '1.0',
    packages= find_packages(),
    install_requires = [
        'langchain',
        'langchain-core',
        'langchain-ollama',
        'langchain-text-splitters',
        'langsmith'
    ],
    py_modules=["About/about"],  
    entrt_points = {
        "console_scripts":[
            "CODEval = About:about"
        ]
    }
)