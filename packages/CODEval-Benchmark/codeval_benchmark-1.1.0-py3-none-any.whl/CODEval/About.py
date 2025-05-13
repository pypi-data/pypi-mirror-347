
def info():
    __title__ = "CODEval-Benchmark"
    __description__ = "A LLM Benchmark that used to evaluate small Large Language Model."
    __version__ = "1.0.0"
    __author__ = "R Kiran Kumar Reddy"
    __author_email__ = "rkirankumarreddy599@gmail.com"
    __license__ = "MIT"
    __url__ = "https://github.com/yourusername/myawesomeproject"
    info = {
        "Title": __title__,
        "Description": __description__,
        "Version": __version__,
        "Author": __author__,
        "Email": __author_email__,
        "License": __license__,
        "URL": __url__
    }
    return info
    
def about():
    for key, value in info().items():
        print(f"{key}: {value}")
