
def get_prompt_multiple_choice(query: str, choices: str):
    prompt = f"""[INST]Select the right option that answer the question between []. 
    Example:
    Question: A student throws a ball into the air. While the ball travels up, the speed of the ball decreases. What force causes the ball to slow while traveling up?
    Options: A) electricity B) gravity C) magnetism d) tension
    Answer: 
    [B] gravity  
    
    [/INST]  

    {query}
    Options: {choices}
    Answer:
    """
    return prompt

def get_prompt_bulas(query, options):
        return f"""[INST]Responda a pergunta sobre medicamentos com a letra que melhor responde a pergunta.
        Exemplo:

        Questão: Qual a dosagem inicial recomendada de Abilify comprimidos para adultos com esquizofrenia?
        Opções: A) 2 mg uma vez ao dia B) 10 a 15 mg uma vez ao dia C) 15 mg uma vez ao dia D) 30 mg uma vez ao dia
        Resposta: 
        [B] 10 a 15 mg uma vez ao dia
        [/INST]
        
        Questão: {query}
        Opções: {options}
        Resposta:
        """

def get_prompt_complete(query, shots):
        prompt = f"""{shots}[INST] Complete the sequence: [/INST]{query}Complete: """
        return prompt   

def get_prompt_question(query, shots):
        return f"""{shots}[INST]Select the right option that answer the question between [] [/INST]{query}Answer: """ 

def get_prompt_question_science(query, choices):
        return f"""<<SYS>> You are a very intelligent studious student. <</SYS>> [INST]Answer the science question: [/INST]{query}""" 

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