from openai import OpenAI

client = OpenAI() # this requires .env to contain the OPENAI_API_KEY

def price_agent(scheme_analysis: str, pricing_rules: str) -> str:
    """
    This is an AI agent that comes up with a pricefor the user based on the scheme analysis.
    This price is based on the scheme(s) that the user is eligible for, the price rules, and the internal knowledge of the LLM.

    Parameters:
        - scheme_analysis: A string containing the scheme analysis.
        - price_rules: A string containing the rules that define the price.
    
    Returns:
        - A string containing the price for the user.
    
    Limitations:
        - The AI agent may not have a large enough knowldge base to accurately make a price prediction.
    """
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert in pensions and insurance. Your job is to determine the price to charge a user based on the provided scheme analysis and the pricing rules."},
            {"role": "user", "content": f"This is the scheme analysis: {scheme_analysis}\n\n"},
            {"role": "user", "content": f"These are the pricing rules: {pricing_rules}\n\n"},
            {"role": "user", "content": "Please give provide a price estimate. Only output a number and nothing else."},
        ]
    )
    return completion.choices[0].message.content


# Example Usage
if __name__ == '__main__':

    # Sample output from agent 1
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

    # Agent 2
    import json
    with open('data/sample_schema.json', 'r') as f:
        sample_schema = json.load(f) # this is the schema for sample data
    from schema_agent import schema_agent
    required_schema = schema_agent(sample_schema, rules) # this is what the previous agent passes to this agent
    print(required_schema)

    # Agent 3
    import pandas as pd
    df = pd.read_csv('data/sample_employee_data.csv')
    required_cols = [col['name'] for col in required_schema['columns']]
    row = df.iloc[0]
    from scheme_agent import scheme_agent
    scheme, scheme_analysis = scheme_agent(row, required_schema, rules)
    print(scheme)
    print(scheme_analysis)

    # Agent 4
    pricing_rules = """
    | Scheme                                  | Scheme Price   |
    |-----------------------------------------|----------------|
    | Unemployment Assistance                 | $200 per month |
    | Old Age Assistance                      | $300 per month |
    | Blind Pension                           | $250 per month |
    | Widow's and Widower's (Non-Contributory) Pension | $220 per month |
    | Deserted Wife's Allowance               | $230 per month |
    | Carer's Allowance                       | $210 per month |
    | Prisoner’s Wife Allowance               | $240 per month |
    | Single Woman’s Allowance                | $215 per month |
    | Orphan’s (Non-Contributory) Pension     | $200 per month |
    """
    price = price_agent(scheme_analysis, pricing_rules)
    print(price)