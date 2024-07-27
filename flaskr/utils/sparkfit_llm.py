from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import os

class SparkfitLLM:

    def __init__(self):
        self.tokenizer = None
        self.model = None
        self.quantized = False
        self.is_loaded = False

    def load_model(self):
        model_name = "arveenazhand/sparkfit-llm"
        token = os.getenv("HUGGINGFACE_HUB_TOKEN")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, token=token)

        if self.tokenizer.pad_token is None:
            self.tokenizer.add_special_tokens({'pad_token': self.tokenizer.eos_token})

        print("Tokenizer loaded")

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
                token=token,
            )
            self.quantized = True
        else:
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                trust_remote_code=True,
                token=token,
            )
            self.quantized = False
        
        self.is_loaded = True
        print("Model loaded")

    def generate_text(self, prompt):

        with open("prompt.txt", "r") as f:
            instruction = f.read()

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        if not self.quantized:
            self.model.to(device)

        full_prompt = f"{instruction}\n{prompt}"
        # print(f"Full prompt: {full_prompt}")

        inputs = self.tokenizer(full_prompt, return_tensors="pt", max_length=1024, truncation=True, padding=True)
        if not self.quantized:
            inputs = {key: value.to(device) for key, value in inputs.items()}
        print("Inputs prepared")

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=8192,
                pad_token_id=self.tokenizer.eos_token_id
            )
        print("Output generated")

        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(f"Response: {response}")
        return response
