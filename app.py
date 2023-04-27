# import dependencies
import os
import streamlit as st
from apikey import apikey
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.memory import ConversationBufferMemory

os.environ["OPENAI_API_KEY"] = apikey

# App framwork
st.title("🦜🔗 LangChain 0.0.148 Recipe App")
st.write("This app generates a recipe based on a given input.")
st.write("The recipe is generated using the OpenAI Language Chain API.")
st.write("The API is based on the GPT-3 model.")
ingredients_prompt = st.text_input("Enter you ingredients here:")

# string templates
ingredients_template = PromptTemplate(
    template="""Question: I have the following ingredients: {ingredients}. Can you suggest a dish?

        Let's do it step buy step.
        First tell me the dish name and where it came from, List the steps to cook the dish in bullet points.
        Answer:""",
    input_variables=["ingredients"],
)

calories_templates = PromptTemplate(
    template="""Question: I have the following ingredients: {ingredients}. Can you calculate the calories for each one?

    Let's do it step buy step. Also mention the unit of measurement. and Total calories.
    Answer:""",
    input_variables=["ingredients"],
)

# Memory
memory = ConversationBufferMemory(input_key="ingredients", memory_key="ingridients_memory")

#llms
llm = OpenAI(temperature=0.9)
ingredients_llmChain = LLMChain(llm=llm, prompt=ingredients_template,output_key="meal",memory=memory)
calories_chain = LLMChain(llm=llm, prompt=calories_templates,output_key="calories",memory=memory)
sequential_chain = SequentialChain(chains=[ingredients_llmChain, calories_chain],input_variables=["ingredients"]
                                   ,output_variables=["meal", "calories"])

# Generate recipe
if ingredients_prompt:
    response = sequential_chain({'ingredients':ingredients_prompt})
    st.text(response['meal'])
    st.text(response['calories'])

    with st.expander("See the conversation"):
        st.info(memory.buffer)
