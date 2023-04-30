# import dependencies
# import os
# import json
import re
import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.memory import ConversationBufferMemory
from langchain.agents import load_tools,initialize_agent,AgentType
from fastapi import FastAPI

# os.environ["OPENAI_API_KEY"] = apikey
# os.environ["WOLFRAM_ALPHA_APPID"] = wolfram_alpha_appid
# os.environ["SERPAPI_API_KEY"] = serpApiKey

# Load tools
app = FastAPI()
# llm = OpenAI(temperature=0.9)

# App framwork
st.title("🦜🔗 LangChain 0.0.148 Recipe App")
st.write("This app generates a recipe based on a given input.")
st.write("The recipe is generated using the OpenAI Language Chain API.")
st.write("The API is based on the GPT-3 model.")
ingredients_prompt = st.text_input("Enter you ingredients here:")

# string templates
dish_template = PromptTemplate(
    template="""Question: I have the following ingredients: {ingredients}. Can you suggest a dish?

        only suggest a dish name, with list of ingredients.
        First tell me the dish name and where it came from, List the steps to cook the dish in bullet points.
        Answer:""",
    input_variables=["ingredients"],
)

dish_steps_template = PromptTemplate(template="""
Question: Can you describe how to make the following dish?
Dish name: {dish}
""", input_variables=["dish"])

# Memory
memory = ConversationBufferMemory(input_key="ingredients", memory_key="ingredients_memory")

# llms
# dish_chain = LLMChain(llm=llm, prompt=dish_template, output_key="dish", memory=memory,verbose=True)
# dish_steps_chain = LLMChain(llm=llm, prompt=dish_steps_template, output_key="steps", memory=memory,verbose=True)
# sequential_chain = SequentialChain(chains=[dish_chain,dish_steps_chain], input_variables=["ingredients"]
#                                    , output_variables=["dish", "steps"],verbose=True)
# tools = load_tools(['wolfram-alpha'],llm=llm)
# agent = initialize_agent(tools,llm,agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,verbose=True)


# @app.post("/recipe-ingredients/")
# async def get_recipe(ingredients: str):
#     response = sequential_chain({'ingredients': ingredients})
#     print(response)
#     calories_template = """
#     Question: I have the following dish: {dish}. Calculate the calories for each individual ingredient, Then calculate the total calories for the dish."""
#     agent_response = agent(calories_template.format(dish=response['dish']))
#     final_response = {
#         "output":response,
#         "calorie":agent_response
#     }
#     return final_response

@app.get("/")
async def root():
    return {"message": "Welcome to Lightring Recipe App api. Refer to the documentation for more details."}
@app.get("/recipe/")
async def get_recipe(health_condition: str,cuisine_type:str,food_type:str,food_preference:str,openAiKey:str):
    prompt = PromptTemplate(template="""
    Question: You are a nutritionist agent and you job is to provide a list of not less than 10 recipes for your client. Your client has the following rules:
    1- health condition: {health_condition}. 
    2- Your client is looking for a {cuisine_type} 
    3- dish that is {food_type}. 
    4- Your client is not like the follwoing ingrideants: {food_preference}.
    Please provide the list of recipes that meet the criteria.
    Note: if on of the rules is not available, Ignore it.
    
    In you answer just mention the dishes names separated by ','.
    Answer:
    """,input_variables=["health_condition","cuisine_type","food_type","food_preference"])
    llm = OpenAI(temperature=0.9,openai_api_key=openAiKey)
    response = llm(prompt.format(health_condition=health_condition,cuisine_type=cuisine_type,food_type=food_type,food_preference=food_preference))
    response_array = re.split(',', response)
    return response_array

@app.get('/recipe-description/')
async def get_recipe_description(dish:str,openAiKey:str):
    description_template = PromptTemplate(template="""
    Question: I have the following dish: {dish}.
     First list the ingredients for the dish,
     Then list the steps to cook the dish in bullet points.""",
                                          input_variables=["dish"])
    llm = OpenAI(temperature=0.9,openai_api_key=openAiKey)
    response = llm(description_template.format(dish=dish))
    return response
# Generate recipe
# if ingredients_prompt:
#     response = sequential_chain({'ingredients': ingredients_prompt})
#     st.text(response['meal'])
#     # st.text(response['calories'])
#
#     with st.expander("See the conversation"):
#         st.info(memory.buffer)
