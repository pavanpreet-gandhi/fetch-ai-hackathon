import json
import pandas as pd
import ollama


client = ollama.Client('http://localhost:11434')


def create_user_message(row: pd.Series, schema: dict) -> str:
    """
    Sub-agent to write an introduction for the user based on the data provided and the schema.
    """
    system_message = f"Your job is to introduce yourself as the user based on the data provided and the schema. Make sure to include all the information (and no more) and be consise and clear. This is the schema: \n\n{schema}"
    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': str(row)},
    ]
    response = client.chat('llama3', messages)
    return response['message']['content']


def create_scheme_analysis(user_message: str, rules: str) -> str:
    """
    Sub-agent to write out an analysis of the user's scheme based on the rules provided.
    """
    system_message = f"""
    You are a helpful AI assistant who is an expert at insurance schemes. 
    Your job is to accurately determine which scheme a user falls into based on their personal information.
    Do not make up any information, only answer with the information provided.
    You must use the following rules to determine the scheme: \n\n{rules}
    """
    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': user_message},
    ]
    response = client.chat('llama3', messages)
    return response['message']['content']


def extract_primary_scheme(scheme_analysis: str, rules: str) -> str:
    """
    Sub-agent to extract the primary scheme from the scheme analysis.
    """
    system_message = f"""
    You are a helpful AI assistant who is an expert at insurance schemes. 
    Your job is to output the scheme that the user is matched to based on the provided analysis. If there are multiple schemes, pick the one that could be the primary scheme.
    Only reply with one scheme name and nothing else. Strip away any markdown formatting. If the user is not compatible with any scheme, reply with 'No Scheme'.
    You must use the scheme names from the following rules: \n\n{rules}
    """
    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': scheme_analysis},
    ]
    response = client.chat('llama3', messages)
    return response['message']['content']


"""
THIS IS THE MAIN AGENT
"""
def scheme_agent(row: pd.Series, schema: dict, rules: str) -> str:
    """
    Agent to get the primary scheme based on the row data.
    """
    user_message = create_user_message(row, schema)
    scheme_analysis = create_scheme_analysis(user_message, rules)
    scheme = extract_primary_scheme(scheme_analysis, rules)
    return scheme, scheme_analysis


# Example usage
if __name__ == '__main__':

    # Setup

    df = pd.read_csv('data/sample_employee_data.csv')
    with open('data/sample_schema.json', 'r') as f:
        sample_schema = json.load(f) # this is the schema for sample data

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

    from schema_agent import schema_agent
    required_schema = schema_agent(sample_schema, rules) # this is what the previous agent passes to this agent


    # Filter data based on the required schema
    required_cols = [col['name'] for col in required_schema['columns']]
    required_cols

    # Get the primary scheme for the first row
    row = df.iloc[0]
    scheme, scheme_analysis = scheme_agent(row, required_schema, rules)
    print(scheme)
    print(scheme_analysis)