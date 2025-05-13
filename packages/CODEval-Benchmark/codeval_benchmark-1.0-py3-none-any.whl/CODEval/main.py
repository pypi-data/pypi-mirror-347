from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
import subprocess
import json
import threading
import time
import sys
from CODEval.Data.data import data1, data2, data3, data4, data5

data = [data1, data2, data3, data4, data5]

def loading_animation(stop_event, estimated_duration=10):
    spinner = ['|', '/', '-', '\\']
    spinner_length = len(spinner)
    start_time = time.time()
    i = 0

    while not stop_event.is_set():
        elapsed = time.time() - start_time
        remaining = max(0, int(estimated_duration - elapsed))
        sys.stdout.write(
            f"\r{spinner[i % spinner_length]}  Estimated time left: {remaining} seconds "
        )
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1

    sys.stdout.write("\r✔️  Done loading!                          \n")

def long_task():
    time.sleep(7) 

# Main logic


class Ollama:
    def __init__(self, model):
        self.model = model
    
    def isavailable(model):
        template = """{question}, only give the answer in showing ,and answer "I AM RUNNING !", 
        """
        prompt = ChatPromptTemplate.from_template(template)
        model = OllamaLLM(model=model)
        chain = prompt | model
        try:
            print(chain.invoke({"question": "Hi!"}))
        except Exception as e:
            if "WinError 10061" in str(e):
                print("Ollama is not running")
            else:
                command = input(f"Model is not installed, Shall i install the model (y/n):")
                if command == 'Y' or 'y':
                    try:
                        subprocess.run("ollama run ",model) 
                    except Exception as e:
                        print(f"You got an error : {str(e)}")
            
    def result_from_model(model,query):
        template = """{question}, only give the option as answer, ex: 'A' or 'B or 'C' or 'D' ,and remove `'` from the result, don't give any explanation
        """
        prompt = ChatPromptTemplate.from_template(template)
        model = OllamaLLM(model=model)
        chain = prompt | model
        a = (chain.invoke({"question": query}))
        return a

    def MainEvaluate(model):
        final_score = []
        for i in range(6):
            performance_counter = []
            for i in data:
                count = 0
                for j in i:
                    res = Ollama.result_from_model(model,j['question'])
                    if res == j["answer"]:
                        count+=1   
                performance_counter.append(count)
            final_score.append(performance_counter)
        b = Ollama.calculate_percentile(final_score)
        return b
    
    def calculate_percentile(a):
        sum = 0
        for i in a:
            for j in range(len(i)):
                sum = sum + (i[j]*(j+1))
        return f"{(sum/1800)*100:.2f}%"

    def Evaluate(model):
        stop_event = threading.Event()
        loading_thread = threading.Thread(target=loading_animation, args=(stop_event, 1200))
        loading_thread.start()
        # Run the task
        score = Ollama.MainEvaluate(model)
        stop_event.set()
        loading_thread.join()
        print(f"The Evaluated Score for {model} : {score}")
        return score
#print(Ollama.calculate_percentile([[16, 7, 15, 5, 5], [18, 6, 14, 5, 7], [17, 7, 12, 6, 5]]))

