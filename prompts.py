
def get_prompt_multiple_choice(query: str, choices: str):
    prompt = f"""[INST]Select the right option that answer the question between []. 
    Example:
    Question: How much is 1+1?
    Options: A) 2 B) 15 C) Imposible
    Answer: [A]
    
    [/INST]    
    Question: {query}
    Options: {choices}
    Answer:
    """
    return prompt

def get_prompt_complete(query: str):
        prompt = f"""[INST] Complete the sequence: [/INST]{query}"""
        return prompt   


def get_prompt(type: str, query: str, choices: str):
    if type == 'bf':
            prompt = f"""Select the right option that answer the question between []. 
            Example:
            Question: How much is 1+1?
            Options: A) 2 B) 15 C) Imposible
            Answer: 
            [A] 2
            
            Now is your turn.
            
            Question: {query}
            Options: {choices}
            Answer:
            """
            return prompt
    
    elif type == 'copa' or type == 'hella':
            prompt = f"""[INST]Complete the sequence with the option make more sense. State the letter corresponding between []
            Example:
            Sequence: Roof shingle removal: A man is sitting on a roof. He
            Options: A) is using wrap to wrap a pair of skis. B) is ripping level tiles off. C) is holding a rubik's cube. D) starts pulling up roofing on a roof.
            Answer:
            [D] starts pulling up roofing on a roof. </s>
            
            Now is your turn.
            [/INST]
            Sequence: {query}
            Options: {choices}
            Answer: 
            """
            return prompt
    elif type == 'mmlu':
            prompt = f"""State the letter corresponding to the correct answer. 
            Example:
            Question: Obesity increases the risk of endometrial cancer. Which hormone is thought to mediate this effect?
            Choices
            A. Testosterone
            B. Oestrogen 
            C. Insulin-like growth factor-1
            D. Thyroxine
            Answer: 
            [B]
            
            Now is your turn.

            {query}
            Answer:
            """
            return prompt
    elif type == 'bulas':
            prompt = f"""Responda a pergunta sobre medicamentos com a letra que melhor responde a pergunta entre colchetes []. Abaixo um exemplo de como você deve proceder.
            Exemplo:
            Pergunta: Obesity increases the risk of endometrial cancer. Which hormone is thought to mediate this effect?
            Opções: A) Testosterone B) Oestrogen C) Insulin-like growth factor-1 D) Thyroxine
            Resposta: 
            [B]
            
            Sua vez:

            Pergunta: {query}
            Opções: {choices}
            Resposta:
            """
            return prompt

    else:
        return query