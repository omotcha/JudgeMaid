import os
import openai

ft_model_id = "ft-VQ2YTiFmuh4RBCykzry7OCPe"

if __name__ == '__main__':
    openai.api_key = os.getenv("OPENAI_API_KEY")
    result = openai.FineTune.retrieve(id=ft_model_id)
    print(result)
