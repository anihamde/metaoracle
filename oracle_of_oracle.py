import argparse
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import DeepLake
from langchain.chat_models import ChatOpenAI

from conversational_retrieval_custom_prompt_chain import ConversationalRetrievalCustomPromptChain
import custom_prompt
from constants import *
from pyth_prompt import *

def pythia_chatbot(lake_name, model_type, retriever_distance_metric, retriever_fetch_k, retriever_mmr, retriever_k):
    embeddings = OpenAIEmbeddings(disallowed_special=())

    db = DeepLake(dataset_path=f"hub://{username_activeloop}/{lake_name}", read_only=True, embedding_function=embeddings)

    retriever = db.as_retriever()
    retriever.search_kwargs['distance_metric'] = retriever_distance_metric
    retriever.search_kwargs['fetch_k'] = retriever_fetch_k
    retriever.search_kwargs['maximal_marginal_relevance'] = retriever_mmr
    retriever.search_kwargs['k'] = retriever_k

    # import custom prompt
    qa_prompt = custom_prompt.CHAT_PROMPT

    # import chatbot
    model = ChatOpenAI(model=model_type) # switch to 'gpt-4'
    qa = ConversationalRetrievalCustomPromptChain.from_llm(model,retriever=retriever,qa_prompt=qa_prompt)

    chat_history = []

    while True:
        question = input("Ask a question: ")

        result = qa({"question": question, "chat_history": chat_history})
        chat_history.append((question, result['answer']))
        print(f"-> **Question**: {question} \n")
        print(f"**Answer**: {result['answer']} \n")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run conversational retrieval chatbot based on indexed files in DeepLake VectorStore.')
    parser.add_argument("--lake_name", "-ln", type=str, help="Name of the lake you wish to draw from")
    parser.add_argument("--model_type", "-mt", type=str, help="Name of the LLM class to be used for the chatbot")
    parser.add_argument("--retriever_distance_metric", "-dm", type=str, help="Distance metric for retriever similarity function")
    parser.add_argument("--retriever_fetch_k", "-fk", type=int, help="Number of results to fetch in retrieval")
    parser.add_argument("--retriever_k", "-k", type=int, help="TODO")

    parser.set_defaults(model_type="gpt-3.5-turbo")
    parser.set_defaults(retriever_distance_metric="cos")
    parser.set_defaults(retriever_fetch_k=100)
    parser.set_defaults(retriever_k=10)

    args = parser.parse_args()

    pythia_chatbot(
        args.lake_name, 
        args.model_type, 
        args.retriever_distance_metric, 
        args.retriever_fetch_k, 
        True, 
        args.retriever_k
    )