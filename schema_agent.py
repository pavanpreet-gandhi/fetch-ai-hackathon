import json
from openai import OpenAI

client = OpenAI() # this requires .env to contain the OPENAI_API_KEY

def schema_agent(input_schema: dict, rules: str):
    """
    This is an AI agent that extracts the relevant columns from a schema based on a set of rules that define a task.

    Parameters:
        - input_schema: A dictionary containing the schema columns.
        - rules: A string containing the rules that define the task.
    
    Returns:
        - A dictionary containing the extracted columns from the schema.
    
    Limitations:
        - The AI agent may not extract the correct columns based on the rules.
        - The AI agent may not output in exact json which will cause a runtime error (solution: dspy.utils.jsonify)
    """
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a schema editing assistant, capable of extracting only the relevant columns based on a task. You only output in JSON format. Do not include other text or markdown tags in the output."},
            {"role": "user", "content": f"The relevant task is to determine the scheme of a person based on the following rules: {rules}"},
            {"role": "user", "content": f"The following is a schema in JSON format with potentially irrelavant information: {input_schema}"},
            {"role": "user", "content": "Please extract only the relevant columns from the schema based on the task. The final output should be a schema in JSON format."},
        ]
    )
    return json.loads(completion.choices[0].message.content)


# Example Usage
if __name__ == "__main__":

    with open("data/sample_schema.json", "r") as f:
        schema = json.load(f)
    
    rules = """
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

    extracted_schema = schema_agent(schema, rules)

    print(extracted_schema)