import os
from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.mongodb import MongoDBSaver

load_dotenv()
DB_URI = os.getenv("MONGO_URI")

# Define your state
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Initialize your LLM
llm = ChatOpenAI(model='gpt-4.1-mini')

# Define the node
def chat_node(state: State):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

# Graph builder (shared)
graph_builder = StateGraph(State)
graph_builder.add_node('chat_node', chat_node)
graph_builder.add_edge(START, 'chat_node')
graph_builder.add_edge('chat_node', END)

# Function to compile graph with MongoDB checkpoint
def compile_mongo_checkpointer(checkpointer):
    return graph_builder.compile(checkpointer=checkpointer)

def main():
    prompt = input("> ")
    config = {"configurable": {"thread_id": "1"}}

    with MongoDBSaver.from_conn_string(DB_URI, db_name="checkpointer", collection_name="checkpointer") as checkpointer:
        graph_with_mongo = compile_mongo_checkpointer(checkpointer)

        graph_result = graph_with_mongo.invoke(
            {"messages": [{"role": "user", "content": prompt}]},
            config
        )
        print("Connecting to:", DB_URI)
        print(graph_result)

        #to stream a graph we can do something like
        # for event in graph_with_mongo.stream(_state):
        #     print("event",event)
        #we would actually need more nodes and edges and also need to implement the state but you get the gist

main()


#needs the configuration of the the mongo in env and api keys but should persist the checkpointer