# Fetch.ai Hackathon Project

## Solution Structure
1. Agent to parse information from document and create rules (via OpenAI assistants)
    - Input: document (word/pdf)
    - Output: text summary of rules
    - Things to consider:
        - Relationship between category, scheme, and price
        - RAG? External data (e.g. wikipedia for defenitions)?
1. Agent to take input table filter relevant information
    - Input: Table with all fields (`pd.DataFrame`)
    - Output: Table with relevant fields (`pd.DataFrame`)
    - Things to consider:
        - Only take relevant columns based on schema, rules, and prompt.
        - Filter out PII with AI firewall (not necessry if local LLM)
1. Agent to take user information and output category and price
    - Input: Row from dataframe
    - Output: LLM chat output stating the the category and price
    - Things to consider:
        - LLM must be local to protect sensative data
        - There should be a function that transforms the tabular input into a prompt

## Additional features
- [ ] Custom frontend
- [ ] AI firewall (only required if agent 3 uses a non-local LLM)
- [ ] Chat fetaure that allows users to change their data and see any resulting change in category