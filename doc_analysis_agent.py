import openai

key = OPENAI_API_KEY,

openai.api_key = key
  
personality = "IBP_Problemstatement.csv"

with open(personality, "r") as file:
    mode = file.read()

messages = [
    {"role": "system", "content": f"{mode}"}
]
  
while True:
    user_input = input("Hello to Insurance Advisor Pro! Press Enter to Analyse The schemes and prices of the insurance provider.")

    messages.append({"role" : "user", "content" : user_input})

    completion = openai.ChatCompletion.create(
model="gpt-4o",
max_tokens=4096,
messages=messages,
temperature=0.8
)

    response = completion.choices[0].message.content
    messages.append({"role": "assistant", "content": response})
    print(f"\n{response}\n")
    
    #"Welcome to Insurance Advisor Pro. Custom insurance broker providing tailored quotes and pricing information based on user data and an insurance document. Let me find you a policy right for you!"
