from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class SparkfitLLM:
    def __init__(self):
        model_name = "arveenazhand/sparkfit-llm"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)

    def generate_text(self, instruction, prompt):
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(device)

        full_prompt = f"{instruction}\n{prompt}"

        inputs = self.tokenizer(full_prompt, return_tensors="pt", max_length=1024, truncation=True, padding=True)

        with torch.no_grad():
            outputs = self.model.generate(inputs, max_length=1024, pad_token_id=self.tokenizer.eos_token_id)

        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response


