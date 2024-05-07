import torch
from torch import float32, nn
from transformers import AutoTokenizer, BitsAndBytesConfig, AutoModelForCausalLM

class LLM():
    def __init__(self, model_id, access_token, quantizer = None):

        self.model_id = model_id
        
        if(quantizer == '4b'):
            quantizer_cfg = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_use_double_quant=True,
                bnb_4bit_compute_dtype=torch.bfloat16
            )
        elif(quantizer == '8b'):
            quantizer_cfg = BitsAndBytesConfig(
                    load_in_8bit=True
                    )    
        else:    
            quantizer_cfg = None

        self.quantizer_cfg = quantizer_cfg
        self.tokenizer = AutoTokenizer.from_pretrained(model_id, token=access_token)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        self.tokenizer.padding_side = "right"
        self.model = AutoModelForCausalLM.from_pretrained(
            model_id,
            quantization_config=quantizer_cfg,
            torch_dtype=torch.float16,
            token = access_token,
            #device_map = 'cuda'
        )
    def prepare_model(self):
        for param in self.model.parameters():
            param.requires_grad = False  # freeze the model - train adapters later
            if param.ndim == 1:
                # cast the small parameters (e.g. layernorm) to fp32 for stability
                param.data = param.data.to(float32)
   #         self.model.gradient_checkpointing_enable()  # reduce number of stored activations
   #         self.model.enable_input_require_grads()
        return self.model

    
    def perplexity(self, prompt, answer):
        self.model.to('cuda')
        inputs_length = len(self.tokenizer(prompt, return_tensors="pt").to("cuda")["input_ids"][0])
        complete_phrase = prompt + answer       
        input = self.tokenizer(complete_phrase, return_tensors="pt").input_ids.to("cuda")
        target_id = input.clone()
        target_id[:,:inputs_length] = -100

        with torch.no_grad():
            outputs = self.model(input, labels=target_id)
            neg_log_likelihood = outputs.loss
        
        ppl = torch.exp(neg_log_likelihood)
        return ppl.item()   
        

    def make_question(self, question: str, inst: str = ""):
        self.model.to('cuda')
        if inst:
            question = f"""[INST] <<SYS>> {inst.strip()}.<</SYS>>
            {question.strip()}[/INST]""".strip()
        inputs = self.tokenizer(question, return_tensors="pt").to("cuda")
        inputs_length = len(inputs["input_ids"][0])
        with torch.inference_mode():
            outputs = self.model.generate(**inputs, max_new_tokens=64, temperature=0.0001)
        return self.tokenizer.decode(outputs[0][inputs_length:], skip_special_tokens=True)
        return summary
