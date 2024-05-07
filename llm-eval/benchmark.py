import os
import sys

import json
import argparse
from model import LLM

from metrics import process
from sklearn.metrics import accuracy_score
import re
import json
import string
import prompts 

from tqdm import tqdm
from sklearn.metrics import accuracy_score
from prompts import get_prompt

import pandas as pd
import yaml

def find_min_index(lst):
    min_value = min(lst)
    min_index = lst.index(min_value)
    return min_index

def create_question(question, choices, gold_answer, show_options, complete):
    letras = string.ascii_uppercase[:10]
    letter_choices = []
    choice_str = ''
    for choice in choices:
            idx = choices.index(choice)
            choice_str = choice_str + f"{letras[idx]}) {choice} "
            letter_choices.append(f"[{letras[idx]}] {choice}.")
    if show_options:
        prompt_shot = f"{question} \nChoices: {choice_str}\n"
    else:
        prompt_shot = f"{question} \n"           
    if gold_answer:
        if complete:
            prompt_shot = prompt_shot + f"Complete: {choices[gold_answer]}\n"
        else:
            if show_options:
                prompt_shot = prompt_shot + f"Answer: {letter_choices[gold_answer]}\n"
            else:
                prompt_shot = prompt_shot + f"Answer: [{letras[gold_answer]}]\n"
           
    return prompt_shot, letter_choices

def main(config):
    # Set up the argument parser
    # parser = argparse.ArgumentParser(description="Receive deepen model's args")
    # parser.add_argument("--model_id", default='mistralai/Mistral-7B-Instruct-v0.2', type=str, help="quantizer")
    # parser.add_argument("--quantizer", default='', type=str, help="quantizer")
    # parser.add_argument("--type", default='copa', type=str, help="quantizer")
    # parser.add_argument("--test", default=False, type=bool, help="quantizer")

    # args = parser.parse_args()

    print(config)

    # if config['type'] == 'winogrande':
    #     path = 'data/winogrande.jsonl'
    #     get_prompt = prompts.get_prompt_complete
    #     type_bench = 'complete'

    # elif config['type'] == 'hella':
    #     path = 'data/hellaswag.jsonl'
    #     get_prompt = prompts.get_prompt_complete
    #     type_bench = 'complete'

    # elif config['type'] == 'mmlu':
    #     path = 'data/mmlu.jsonl'
    #     get_prompt = prompts.get_prompt_complete
    #     type_bench = 'complete'
    #     create_shot = False

    # elif config['type'] == 'arc_easy':
    #     path = 'data/arc_easy.jsonl'
    #     get_prompt = prompts.get_prompt_question
    #     type_bench = 'questions'

    # elif config['type'] == 'bulas':
    #     path = 'data/bulas.jsonl'
    #     get_prompt = prompts.get_prompt_question
    #     type_bench = 'questions'

    # elif config['type'] == 'bf':
    #     path = 'data/bf.jsonl'
    #     type_bench = 'questions'
    # elif config['type'] == 'piqa':
    #     path = 'data/piqa.jsonl'
    #     #get_prompt = prompts.get_prompt_question
    #     get_prompt = prompts.get_prompt_complete
    #     type_bench = 'complete'

    dict_results = {}
    models = config['models']
    access_token = config['access_token']
    type_bench = config['type_bench']
    path = config['path']
    if type_bench == 'complete':
        get_prompt = prompts.get_prompt_complete
    elif type_bench == 'questions':
        get_prompt = prompts.get_prompt_question

    for model_id in models:
        # model_id = config['model_id']
        quantizer = config['quantizer']

        complete = False
        show_options = True
        if type_bench == 'complete':
            complete = True
            show_options = False

        model = LLM(model_id, access_token, quantizer)
        list_json = []

        print("Loading the JSONL with the questions...")

        with open(path, 'r') as file:
            for line in file:
                list_json.append(json.loads(line))
        print("Inference...")

        # If was a simple test to see the benchmark performance, only pass the firsts 50 questions. 
        if config['test'] == True:
            list_json = list_json[:50]

        golds, predict_ppl, predict_acc  = [], [], []

        accuracy_, accuracy_ppl = 0, 0
        perplexity = True
        accuracy = False



        lst_shots = list_json[:0]
        list_json = list_json[0:]
        prompt_shot = ''
        for shot in lst_shots:
            p_shot, lst = create_question(shot['query'], shot['choices'], shot['gold'], show_options, complete)
            prompt_shot = prompt_shot + p_shot

        # print(prompt_shot)
        rows = []
        
        for data in tqdm(list_json):
            choice_str = ''
            letras = string.ascii_uppercase[:10]
            golds.append(letras[data['gold']])

            # letter_choices = []
            # for choice in data["choices"]:
            #     idx = data["choices"].index(choice)
            #     choice_str = choice_str + f"{letras[idx]}) {choice} "
            #     letter_choices.append(f"[{letras[idx]}] {choice}.")
            question, letter_choices = create_question(data['query'], data['choices'], None, show_options, complete)

            if perplexity:
                
                lst_choices = []
                #prompt_shot = f"Contexto: {data['points']}"
                prompt = get_prompt(question, prompt_shot)
                # print(prompt)
                # exit()
                if type_bench == "complete":
                    lst_choices = data['choices']

                elif type_bench == "questions":
                    lst_choices = letter_choices


                # prompt = prompt_shot + f"{data['query']} \nAnswer: "

                lst_ppl = []
                # print(prompt)
                for choice in lst_choices:
                    ppl = model.perplexity(prompt, choice)
                    lst_ppl.append(ppl)
                #     print(f"PPL {choice}: {ppl}")
                # print(letras[find_min_index(lst_ppl)])
                # print("Gold:", letras[data['gold']])
                data['ppl'] = lst_ppl[find_min_index(lst_ppl)]
                predict_ppl.append(letras[find_min_index(lst_ppl)])

            if accuracy:
                prompt = get_prompt(config['type'], data['query'], choice_str)
                answer = model.make_question(prompt)

                # Encontrar letras entre colchetes
                letras_entre_colchetes = re.findall(r'\[(.*?)\]', answer)

                if letras_entre_colchetes:
                    answer_letter = letras_entre_colchetes[0]
                else:
                    answer_letter = '0'
                predict_acc.append(answer_letter)
            rows.append(data)


        model_name = model_id.split("/")[-1]


        if perplexity:
            accuracy_ppl = accuracy_score(golds, predict_ppl)
            print("Accuracy Perplexity: ", accuracy_ppl)
        if accuracy:
            accuracy_ = accuracy_score(golds, predict_acc)
            print("Accuracy: ", accuracy_)
            print("Invalide Answers: ", predict_acc.count('0'))
            print("Valide Answers: ", len(predict_acc) - predict_acc.count('0'))
        
        dict_results[model_id] = accuracy_ppl

    if not os.path.exists('results'):
        os.makedirs('results')


    with open(f"results/{config['type']}_{config['experiment_name']}.json", "w") as outfile: 
        json.dump(dict_results, outfile, indent=4)


    # df = pd.DataFrame(rows)
    # df.to_csv(f'results/{model_name}_{config["type"]}.csv', index=False)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        with open('config.yaml', 'r') as file:
            config = yaml.safe_load(file)
            main(config)
    else:
        config_file = sys.argv[1]
        with open(config_file, 'r') as file:
            config = yaml.safe_load(file)
            main(config)