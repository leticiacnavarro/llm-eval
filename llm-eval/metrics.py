import re
import json
import string
import prompts 

from tqdm import tqdm
from sklearn.metrics import accuracy_score
from prompts import get_prompt

def find_min_index(lst):
    min_value = min(lst)
    min_index = lst.index(min_value)
    return min_index

def process(model, list_json, type_bench, perplexity, accuracy):
    golds, predict_ppl, predict_acc  = [], [], []

    accuracy_, accuracy_ppl = 0, 0

    for data in tqdm(list_json):
        choice_str = ''
        letras = string.ascii_uppercase[:10]
        golds.append(letras[data['gold']])

        letter_choices = []
        for choice in data["choices"]:
            idx = data["choices"].index(choice)
            choice_str = choice_str + f"{letras[idx]}) {choice} "
            letter_choices.append(f"[{letras[idx]}] {choice}.")

        if perplexity:
            
            lst_choices = []

            if type_bench == "hella" or "piqa":
                prompt = prompts.get_prompt_complete(data['query'])
                lst_choices = data['choices']
            elif type_bench == "bulas":
                prompt = prompts.get_prompt_bulas(data['query'], choice_str)
                lst_choices = letter_choices
            else:
                prompt = prompts.get_prompt_multiple_choice(data['query'], choice_str)
                lst_choices = letter_choices

            lst_ppl = []
            for choice in lst_choices:
                ppl = model.perplexity(prompt, choice)
                lst_ppl.append(ppl)
            #     print(f"PPL {choice}: {ppl}")
            # print(letras[find_min_index(lst_ppl)])
            # print("Gold:", letras[data['gold']])
            
            predict_ppl.append(letras[find_min_index(lst_ppl)])

        if accuracy:
            prompt = get_prompt(type_bench, data['query'], choice_str)
            answer = model.make_question(prompt)

            # Encontrar letras entre colchetes
            letras_entre_colchetes = re.findall(r'\[(.*?)\]', answer)

            if letras_entre_colchetes:
                answer_letter = letras_entre_colchetes[0]
            else:
                answer_letter = '0'
            predict_acc.append(answer_letter)

    if perplexity:
        accuracy_ppl = accuracy_score(golds, predict_ppl)
        print("Accuracy Perplexity: ", accuracy_ppl)
    if accuracy:
        accuracy_ = accuracy_score(golds, predict_acc)
        print("Accuracy: ", accuracy_)
        print("Invalide Answers: ", predict_acc.count('0'))
        print("Valide Answers: ", len(predict_acc) - predict_acc.count('0'))

    return accuracy_, accuracy_ppl
# def perplexity(model, list_json, type_bench):
#     golds = []
#     predict = []

#     for data in tqdm(list_json[:10]):
#         choices = ''
#         idx = 0
#         letras = string.ascii_uppercase[:10]
#         letter_choices = []
#         for choice in data["choices"]:
#             choices = choices + f"{letras[idx]}) {choice} "
#             letter_choices.append(f"[{letras[idx]}] {choice}.")
#             idx = idx + 1
        
#         prompt = get_prompt(type_bench, data['query'], choices)
#         lst_ppl = []
#         for choice in letter_choices:
#             ppl = model.perplexity(prompt, choice)
#             lst_ppl.append(ppl)
#             # print(f"PPL {choice}: {ppl}")

#         # print(letras[find_min_index(lst_ppl)])
#         # print("Gold:", letras[data['gold']])
#         golds.append(letras[data['gold']])
#         predict.append(letras[find_min_index(lst_ppl)])
#     accuracy = accuracy_score(golds, predict)
#     print("Accuracy Perplexity: ", accuracy)
#     return ""

# def accuracy(model, list_json, type_bench):
    
#     golds = []
#     predict = []

#     for data in tqdm(list_json[:50]):
#    # for data in list_json[:50]:

#         choices = ''
#         idx = 0
#         letras = string.ascii_uppercase[:10]
#         for choice in data["choices"]:
#             choices = choices + f"{letras[idx]}) {choice} "
#             idx = idx + 1
        
#         prompt = get_prompt(type_bench, data['query'], choices)

#         answer = model.make_question(prompt)

#         # Encontrar letras entre colchetes
#         letras_entre_colchetes = re.findall(r'\[(.*?)\]', answer)

#         if letras_entre_colchetes:
#             answer_letter = letras_entre_colchetes[0]
#         else:
#             answer_letter = '0'

#         # print("prompt", prompt)
#         # print("Answer", answer)
#         # print("Answer Letter:", answer_letter)
#         # print("Gold:", letras[data['gold']])
#         # print()
        
#         golds.append(letras[data['gold']])
#         predict.append(answer_letter)

    
#     accuracy = accuracy_score(golds, predict)
#     print("Accuracy: ", accuracy)
#     print("Invalide Answers: ", predict.count('0'))
#     print("Valide Answers: ", len(predict) - predict.count('0'))
#    # print(predict)
    
#     # Filtrando os itens diferentes de zero da lista A e seus correspondentes em B
#     valores_A = [a for a, b in zip(predict, golds) if a != '0']
#     valores_B = [b for a, b in zip(predict, golds) if a != '0']
#     print("Accuracy Not Zero: ", accuracy_score(valores_A, valores_B))