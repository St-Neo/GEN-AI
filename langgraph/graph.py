
#arrow is edge and block is node
#each node input is state and output is the modifed state
#maybe the state starts with data,user name and endds with result (the result is by default none)

from langgraph.graph import StateGraph, START,END
from langgraph.graph.message import add_messages
from langchain.chat_model import init_chat_model
from typing_extensions import TypedDict
from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()

client = OpenAI()
class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    query:str
    llm_result:str|None

def chatbot(state:State):
    query=state['query']

    llm_response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role":"user","content":query}
        ]
    )
    client.chat.
    result=llm_response.choices[0].message.content
    state["llm_result"]=result

    return state

graph_builder =StateGraph(State)

graph_builder.add_node("chatbot",chatbot)

graph_builder.add_edge(START,"chatbot")
graph_builder.add_edge("chatbot",END)

graph=graph_builder.compile()


def main():
    user= input(">")

    #to invoke the graph we need state
    _state={
        "query":user,
        "llm_result":None
    }
    #invoking the graph
    gpraph_result= graph.invoke(_state)

    print(gpraph_result)


main()