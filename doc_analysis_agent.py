import openai
import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("OPENAI_API_KEY")

openai.api_key = key

def doc_analysis_agent(file):

    with open(file, "r") as file:
        mode = file.read()

    messages = [
        {"role": "system", 'content': f"You are an expert in finance and insurance. Your job is to output a set of rules that map users to schemes. This is the document containing the finformation for the schemes {mode}"}
    ]

    example = """
    | Scheme | Scheme Rules |
    |--------|--------------|
    | **Unemployment Assistance** | 1. Resident of the State. 2. Unemployed but capable of and available for work. 3. Have insufficient means. |
    | **Old Age Assistance** | 1. Resident of the State. 2. Aged 66 years or over. 3. Have insufficient means. |
    | **Blind Pension** | 1. Resident of the State. 2. Aged 18 years or over. 3. Have a vision impairment. 4. Have insufficient means. |
    | **Widow’s and Widower’s (Non-Contributory) Pension** | 1. Resident of the State. 2. Widow or widower not cohabiting. 3. Have insufficient means. |
    | **Deserted Wife’s Allowance** | 1. Resident of the State. 2. Deserted by husband. 3. Have insufficient means. 4. Not cohabiting. |
    | **Carer's Allowance** | 1. Resident of the State. 2. Providing full-time care and attention to a person in need. 3. Have insufficient means. |
    | **Prisoner's Wife Allowance** | 1. Resident of the State. 2. Husband in prison. 3. Have insufficient means. 4. Not cohabiting. |
    | **Single Woman’s Allowance** | 1. Resident of the State. 2. Aged 58 years or over. 3. Single woman living alone. 4. Have insufficient means. |
    | **Orphan’s (Non-Contributory) Pension** | 1. Resident of the State. 2. Under 18 years of age. 3. Orphaned. 4. Have insufficient means. |
    """

    messages.append({'role': 'system', 'content': f'This is an example output format \n\n: {example}'})

    messages.append({"role" : "user", "content" : "Please output a set of rules that map users to schemes."})

    completion = openai.ChatCompletion.create(
        model="gpt-4o",
        max_tokens=4096,
        messages=messages,
        temperature=0.8
    )

    response = completion.choices[0].message.content
    return response

if __name__ == "__main__":
    output = doc_analysis_agent("IBP_Problemstatement.csv")
    print(output)