from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage

class GPTResponder:
    def __init__(self, model="gpt-4o-mini"):
        self.model = ChatOpenAI(model=model)
        self.chat_history = [SystemMessage(content="You are a helpful AI assistant.")]
    
    def get_response(self, query):
        self.chat_history.append(HumanMessage(content=query))
        result = self.model.invoke(self.chat_history)
        response = result.content
        self.chat_history.append(AIMessage(content=response))
        return response