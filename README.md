# Fetch.ai Hackathon Project
This repo contains the underlying logic for the agents that can be easily ported as fetch.ai agents. Each agent can work independantly from each other but are interoperable, making them ideal for the fetch.ai ecosystem.

Each agent can be run by pip installing everything from `requirements.txt` except the doc-aalysis-agent which reuires an older version of the `openai` library as specified in `requirements.txt`.

We hope to pathch these issues in future versions to create an end-to-end working solution tha runs on the AI engine aith DeltaV.

The following are the agent files:
1. `doc_analysis_agent.py` is responsible for extractig the relevant information from the document usingthe `openai` library (older version) with GPT-4o.
2. The `schema_agent.py` takes as input the schema of the data in JSON format and returns a new schema which only contains the relevant columns required for the task (in this case figuring out the pension scheme that the user qualifies for).
3. The `scheme_agent.py` takes each row from the table of employees and oututs the primary scheme that the user qualifies for along with it's reasoning based on the rules from the doc analysis agent. It uses a local language model running on `ollama` to prevent PII (personally identifiable information) and sensative data from being exposed to openai.
4. The final `price_agent.py` takes the reasoning output of the scheme agent and draws upon it's internal knowldege of insurance (potentially provided by RAG or system prompting) assess the price of the empployee.

## Solution Structure
1. Agent to parse information from document and create rules (via OpenAI assistants)
    - Input: document (word/pdf)
    - Output: text summary of rules to include Scheme name, Scheme rules, Price
    - Things to consider:
        - Relationship between category, scheme, and price
        - RAG? External data (e.g. wikipedia for defenitions)?
        - Second vice-Agent to check the results of the applied Logic from Agent 2
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
- Custom frontend
- AI firewall (only required if agent 3 uses a non-local LLM)
- Chat fetaure that allows users to change their data and see any resulting change in category

### Features and Limitations of the current repository:
- [x] All agents work end to end
- [x] All agents are interoperable
- [ ] All agents work with the same requirements
- [ ] All agents are functioning within the micro-agent architechture
- [ ] Product is working end-to-end on micro-agents
