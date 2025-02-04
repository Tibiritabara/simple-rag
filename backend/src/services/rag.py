import datetime
from collections.abc import Callable
from typing import Literal, cast

from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.tools import Tool
from langchain_openai import AzureChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from llama_index.core import VectorStoreIndex
from llama_index.core.schema import NodeWithScore
from pydantic import BaseModel, PrivateAttr

from services.embeddings import VectorStoreHandler
from services.prompts import (
    ANSWER_PROMPT,
    DOCUMENT_GRADING_PROMPT,
    QUERY_REWRITE_PROMPT,
    RAG_SYSTEM_PROMPT,
    RAG_USER_PROMPT,
)
from utils.config import get_config
from utils.types import AgenticRagState, DocumentGrade, QueryResponse, Source


class RagService(BaseModel):
    """
    Service to handle the RAG process.

    Attributes:
        index_name(str): The name of the index to use.
    """

    index_name: str
    __vector_store_index: VectorStoreIndex = PrivateAttr()
    __llm_model: AzureChatOpenAI = PrivateAttr()

    def __init__(self, index_name: str = "Documents", **kwargs):
        """
        Initializes the RAG service.

        Args:
            index_name(str): The name of the index to use.
        """
        super().__init__(index_name=index_name, **kwargs)
        self.__vector_store_index = VectorStoreHandler(
            index_name=index_name,
        ).get_index()
        self.__llm_model = AzureChatOpenAI(
            api_version=get_config().azure_openai_api_version,
            azure_endpoint=str(get_config().azure_openai_endpoint),
            model=get_config().azure_openai_llm_model,
            api_key=get_config().azure_openai_api_key,
        )

    def query(
        self,
        query: str,
        query_mode: str = "hybrid",
        top_k: int = 15,
    ) -> QueryResponse:
        """
        Queries the RAG service.

        Args:
            query(str): The query to use.
            top_k(int): The number of results to return.

        Returns:
            The response containing the status and message.
        """
        sources = self.__vector_store_index.as_retriever(
            vector_store_query_mode=query_mode,
            similarity_top_k=top_k,
            alpha=0.3,
        ).retrieve(query)
        sources = cast(list[NodeWithScore], sources)
        sources_str = "\n\n".join([source.get_content() for source in sources])
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", RAG_SYSTEM_PROMPT),
                ("user", RAG_USER_PROMPT),
            ]
        )
        chain = prompt | self.__llm_model
        response = chain.invoke(
            {
                "query": query,
                "documents": sources_str,
                "date": datetime.datetime.now().strftime("%Y-%m-%d"),
            }
        )

        print("Response: ", response.content)

        return QueryResponse(
            message=str(response.content),
            sources=[
                Source(
                    text=source.get_content(),
                    metadata=source.metadata,
                )
                for source in sources
            ],
        )

    def retrieve(
        self,
        query: str,
        query_mode: str = "hybrid",
        top_k: int = 15,
    ) -> list[Source]:
        sources = self.__vector_store_index.as_retriever(
            vector_store_query_mode=query_mode,
            similarity_top_k=top_k,
            alpha=0.3,
        ).retrieve(query)
        return [
            Source(text=source.get_content(), metadata=source.metadata)
            for source in sources
        ]


class AgenticRagService(BaseModel):
    """
    Service to handle the RAG process.
    This service uses Azure OpenAI to generate the response, as it has broader capabilities than Ollama.

    Attributes:
        index_name(str): The name of the index to use.
    """

    index_name: str
    __vector_store_index: VectorStoreIndex = PrivateAttr()
    __llm_model: AzureChatOpenAI = PrivateAttr()

    def __init__(self, index_name: str = "Documents", **kwargs):
        """
        Initialize the Agentic RAG service.

        Args:
            index_name(str): The name of the index to use.
        """
        super().__init__(index_name=index_name, **kwargs)
        self.__vector_store_index = VectorStoreHandler(
            index_name=index_name,
        ).get_index()
        self.__llm_model = AzureChatOpenAI(
            api_version=get_config().azure_openai_api_version,
            azure_endpoint=str(get_config().azure_openai_endpoint),
            model=get_config().azure_openai_llm_model,
            api_key=get_config().azure_openai_api_key,
        )

    def generate_grade_documents_edge(
        self,
    ) -> Callable[[AgenticRagState], Literal["answer", "rewrite"]]:
        """
        Generate a document grader edge for the documents.
        It will grade the documents and based on the output it will move through the graph.
        """

        def grade_documents(state: AgenticRagState) -> Literal["answer", "rewrite"]:
            """
            Grade the documents and based on the output it will move through the graph.

            Args:
                state(AgenticRagState): The state of the agent.

            Returns:
                (Literal["answer", "rewrite"]): The next edge to move to.
            """
            print("--- DOCUMENT GRADING ---")
            llm_with_structured_output = self.__llm_model.with_structured_output(
                DocumentGrade
            )
            document_grading_prompt = PromptTemplate.from_template(
                DOCUMENT_GRADING_PROMPT
            )
            chain = document_grading_prompt | llm_with_structured_output
            messages = state["messages"]
            response = chain.invoke(
                {
                    "question": messages[0].content,
                    "context": messages[-1].content,
                }
            )
            response = cast(DocumentGrade, response)
            print("Response: ", response)

            if response.is_relevant:
                return "answer"
            return "rewrite"

        return grade_documents

    def __generate_retriever_tool(self) -> list[Tool]:
        """
        Generate a retriever tool for the vector store.
        """
        retriever = self.__vector_store_index.as_retriever(
            vector_store_query_mode="hybrid",
            similarity_top_k=15,
            alpha=0.3,
        )

        def retrieve(query: str) -> list[Source]:
            """
            Retrieve documents from the vector store.

            Args:
                query(str): The query to retrieve documents for.

            Returns:
                (list[Source]): A list of documents.
            """
            print("--- RETRIEVING DOCUMENTS TOOL ---")
            sources = retriever.retrieve(query)
            return [
                Source(text=source.get_content(), metadata=source.metadata)
                for source in sources
            ]

        return [
            Tool.from_function(
                retrieve,
                name="retrieve",
                description="Retrieve documents from the vector store",
            )
        ]

    def generate_agent_node(self) -> Callable[[AgenticRagState], AgenticRagState]:
        """
        Generate an agent node for the graph.
        """

        def agent_node(state: AgenticRagState) -> AgenticRagState:
            """
            Call the agent.

            Args:
                state(AgenticRagState): The state of the agent.

            Returns:
                (AgenticRagState): The state of the agent.
            """
            print("--- AGENT NODE ---")
            messages = state["messages"]
            llm_with_tools = self.__llm_model.bind_tools(
                self.__generate_retriever_tool()
            )
            response = llm_with_tools.invoke(messages)
            return {"messages": [response]}

        return agent_node

    def generate_rewrite_node(self) -> Callable[[AgenticRagState], AgenticRagState]:
        """
        Generate a rewrite node for the graph.
        This node will rewrite the user query based on the efficacy of the retrieved documents.
        """

        def rewrite_node(state: AgenticRagState) -> AgenticRagState:
            """
            Rewrite the documents.

            Args:
                state(AgenticRagState): The state of the agent.

            Returns:
                (AgenticRagState): The state of the agent.
            """
            print("--- REWRITE QUERY ---")
            messages = state["messages"]
            question = messages[0].content
            prompt = PromptTemplate.from_template(QUERY_REWRITE_PROMPT)
            chain = prompt | self.__llm_model
            response = chain.invoke({"question": question})
            return {"messages": [response]}

        return rewrite_node

    def generate_answer_node(self) -> Callable[[AgenticRagState], AgenticRagState]:
        """
        Generate an answer node for the graph.
        """

        def answer_node(state: AgenticRagState) -> AgenticRagState:
            """
            Answer the question.

            Args:
                state(AgenticRagState): The state of the agent.

            Returns:
                (AgenticRagState): The state of the agent.
            """
            print("--- ANSWER QUERY ---")
            messages = state["messages"]
            question = messages[0].content
            last_message = messages[-1]
            docs = last_message.content
            prompt = PromptTemplate.from_template(ANSWER_PROMPT)
            chain = prompt | self.__llm_model
            response = chain.invoke({"question": question, "context": docs})
            return {"messages": [response]}

        return answer_node

    def generate_rag_graph(self) -> CompiledStateGraph:
        """
        Generate the Agentic RAG LangGraph graph.
        """
        graph = StateGraph(AgenticRagState)
        graph.add_node("agent", self.generate_agent_node())
        retriever_node = ToolNode(self.__generate_retriever_tool())
        graph.add_node("retrieve", retriever_node)
        graph.add_node("rewrite", self.generate_rewrite_node())
        graph.add_node("answer", self.generate_answer_node())
        graph.add_edge(START, "agent")
        graph.add_conditional_edges(
            "agent",
            tools_condition,
            {
                "tools": "retrieve",
                "END": END,
            },
        )
        graph.add_conditional_edges(
            "retrieve",
            self.generate_grade_documents_edge(),
        )
        graph.add_edge("answer", END)
        graph.add_edge("rewrite", "agent")
        compiled_graph = graph.compile()
        return compiled_graph
