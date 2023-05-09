from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import DeepLake
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain

from constants import *

embeddings = OpenAIEmbeddings(disallowed_special=())

db = DeepLake(dataset_path=f"hub://{username_activeloop}/{name_lake}", read_only=True, embedding_function=embeddings)

retriever = db.as_retriever()
retriever.search_kwargs['distance_metric'] = 'cos'
retriever.search_kwargs['fetch_k'] = 100
retriever.search_kwargs['maximal_marginal_relevance'] = True
retriever.search_kwargs['k'] = 10

# import chatbot
model = ChatOpenAI(model='gpt-3.5-turbo') # switch to 'gpt-4'
qa = ConversationalRetrievalChain.from_llm(model,retriever=retriever)

chat_history = []

while True:
    question = input("Ask a question: ")

    result = qa({"question": question, "chat_history": chat_history})
    chat_history.append((question, result['answer']))
    print(f"-> **Question**: {question} \n")
    print(f"**Answer**: {result['answer']} \n")