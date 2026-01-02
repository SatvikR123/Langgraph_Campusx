from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List, Annotated
from langchain_core.messages import BaseMessage 
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
load_dotenv()

class chatState(TypedDict):
    messages : Annotated[List[BaseMessage], add_messages]

from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

def chat_node(state:chatState):
    # take user query from state
    messages = state["messages"]
    # send it to llm
    response = llm.invoke(messages)
    # store the response in state
    return {"messages": [response]}

checkpointer = MemorySaver()
graph = StateGraph(chatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)
chatbot = graph.compile(checkpointer=checkpointer)