import re
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from fastapi import FastAPI

# Load tools
app = FastAPI()

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
