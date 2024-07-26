from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class SparkfitLLM:
    def __init__(self):
        model_name = "arveenazhand/sparkfit-llm"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

        # Check if a GPU is available
        if torch.cuda.is_available():
            from transformers import BitsAndBytesConfig
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.bfloat16
            )
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                quantization_config=bnb_config,
                device_map="auto",
                trust_remote_code=True,
            )
        else:
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                trust_remote_code=True,
            )

    def generate_text(self, instruction, prompt):
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(device)

        full_prompt = f"{instruction}\n{prompt}"

        inputs = self.tokenizer(full_prompt, return_tensors="pt", max_length=1024, truncation=True, padding=True)
        inputs = {key: value.to(device) for key, value in inputs.items()}

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=1024,
                pad_token_id=self.tokenizer.eos_token_id
            )

        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response
