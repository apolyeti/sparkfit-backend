from sparkfit_llm import SparkfitLLM

def test_generate_text():
    with open("prompt.txt", "r") as f:
        instruction = f.read()

    
    llm = SparkfitLLM()
    prompt = "001 black, cotton, baggy hoodie; 002 blue, denim, baggy jeans; 003 white, polyester, oversized t-shirt; 004 green, wool, slim-fit sweater; 005 grey, cotton, regular-fit trousers; 006 brown, leather, boots. Weather: 15°C, cloudy."
    response = llm.generate_text(instruction, prompt)

    print(response)


if __name__ == "__main__":
    test_generate_text()

