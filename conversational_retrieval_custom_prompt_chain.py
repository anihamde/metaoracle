from typing import Any, Optional, Dict

from langchain.chains import ConversationalRetrievalChain
from langchain.base_language import BaseLanguageModel
from langchain.prompts import BasePromptTemplate
from langchain.callbacks.base import BaseCallbackManager
from langchain.chains.combine_documents.base import BaseCombineDocumentsChain
from langchain.chains.conversational_retrieval.prompts import CONDENSE_QUESTION_PROMPT
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain.schema import BaseRetriever
from langchain.chains.conversational_retrieval.base import BaseConversationalRetrievalChain


def load_qa_chain_stuff_custom_prompt(
    llm: BaseLanguageModel,
    custom_prompt: BasePromptTemplate,
    verbose: Optional[bool] = None,
    callback_manager: Optional[BaseCallbackManager] = None,
    **kwargs: Any,
) -> BaseCombineDocumentsChain:
    """Load question answering chain.

    Args:
        llm: Language Model to use in the chain.
        chain_type: Type of document combining chain to use. Should be one of "stuff",
            "map_reduce", "map_rerank", and "refine".
        verbose: Whether chains should be run in verbose mode or not. Note that this
            applies to all chains that make up the final chain.
        callback_manager: Callback manager to use for the chain.

    Returns:
        A chain to use for question answering.
    """
    llm_chain = LLMChain(
        llm=llm, prompt=custom_prompt, verbose=verbose, callback_manager=callback_manager
    )
    # TODO: document prompt
    return StuffDocumentsChain(
        llm_chain=llm_chain,
        document_variable_name="context",
        verbose=verbose,
        callback_manager=callback_manager,
        **kwargs,
    )



class ConversationalRetrievalCustomPromptChain(ConversationalRetrievalChain):
    """Chain for chatting with an index."""

    retriever: BaseRetriever
    """Index to connect to."""
    max_tokens_limit: Optional[int] = None
    """If set, restricts the docs to return from store based on tokens, enforced only
    for StuffDocumentChain"""
    
    @classmethod
    def from_llm(
        cls,
        llm: BaseLanguageModel,
        retriever: BaseRetriever,
        qa_prompt: BasePromptTemplate,
        condense_question_prompt: BasePromptTemplate = CONDENSE_QUESTION_PROMPT,
        verbose: bool = False,
        combine_docs_chain_kwargs: Optional[Dict] = None,
        **kwargs: Any,
    ) -> BaseConversationalRetrievalChain:
        """Load chain from LLM."""
        combine_docs_chain_kwargs = combine_docs_chain_kwargs or {}
        doc_chain = load_qa_chain_stuff_custom_prompt(
            llm,
            custom_prompt=qa_prompt,
            verbose=verbose,
            **combine_docs_chain_kwargs,
        )
        condense_question_chain = LLMChain(
            llm=llm, prompt=condense_question_prompt, verbose=verbose
        )
        return cls(
            retriever=retriever,
            combine_docs_chain=doc_chain,
            question_generator=condense_question_chain,
            **kwargs,
        )