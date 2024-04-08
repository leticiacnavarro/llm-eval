import os
import json
import argparse
from model import LLM

from metrics import process
from sklearn.metrics import accuracy_score

def main():
    # Set up the argument parser
    parser = argparse.ArgumentParser(description="Receive deepen model's args")
    parser.add_argument("--model_id", default='meta-llama/Llama-2-7b-chat-hf', type=str, help="quantizer")
    parser.add_argument("--quantizer", default='', type=str, help="quantizer")
    parser.add_argument("--type", default='copa', type=str, help="quantizer")

    args = parser.parse_args()

    if args.type == 'copa':
        path = 'data/copa-0.jsonl'
    elif args.type == 'hella':
        path = 'data/hellaswag-0.jsonl'
    elif args.type == 'mmlu':
        path = 'data/mmlu.jsonl'
    elif args.type == 'bulas':
        path = 'data/bulas.jsonl'
    elif args.type == 'bf':
        path = 'data/bf.jsonl'

    model_id = args.model_id
    quantizer = args.quantizer

    model = LLM(model_id, quantizer)
    list_json = []

    print("Loading the JSONL with the questions...")

    with open(path, 'r') as file:
        for line in file:
            list_json.append(json.loads(line))
    print("Inference...")

    acc, acc_ppl = process(model, list_json, args.type, True, False)

    dict_results = {
        "benchmark" : args.type,
        "accuracy_perplexity": acc_ppl,
        "accuracy": acc
    }

    if not os.path.exists('results'):
        os.makedirs('results')

    with open("results/sample.json", "w") as outfile: 
        json.dump(dict_results, outfile)
    
if __name__ == "__main__":
    main()
