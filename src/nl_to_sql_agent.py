import os
from langchain.prompts import PromptTemplate
# from langchain.chains import LLMChain  # Deprecated
from langchain_openai import ChatOpenAI, OpenAI

class NLToSQLAgent:
    def __init__(self, schema_metadata, openai_api_key=None, model_name="gpt-3.5-turbo", llm=None):
        self.schema_metadata = schema_metadata
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.model_name = model_name
        if llm is not None:
            self.llm = llm
        else:
            if "gpt-3.5" in model_name or "gpt-4" in model_name:
                self.llm = ChatOpenAI(api_key=self.openai_api_key, model=model_name, temperature=0)
            else:
                self.llm = OpenAI(api_key=self.openai_api_key, model=model_name, temperature=0)
        self.prompt_template = PromptTemplate(
            input_variables=["question", "schema"],
            template=(
                "You are an expert data analyst. Given the following database schema and a natural language question, generate a syntactically correct SQL query.\n"
                "Schema: {schema}\n"
                "Question: {question}\n"
                "SQL:"
            )
        )
        # Use RunnableSequence: prompt | llm
        self.chain = self.prompt_template | self.llm

    def schema_to_string(self):
        # Convert schema metadata to a readable string for the prompt
        models = self.schema_metadata.get("models", {})
        lines = []
        for model, info in models.items():
            cols = ", ".join(info.get("columns", []))
            lines.append(f"Table: {model} (columns: {cols})")
        return "\n".join(lines)

    def translate(self, question):
        schema_str = self.schema_to_string()
        # Use invoke instead of run
        result = self.chain.invoke({"question": question, "schema": schema_str})
        # result may be a dict or string depending on the model
        if isinstance(result, dict) and "text" in result:
            return result["text"].strip()
        elif isinstance(result, str):
            return result.strip()
        else:
            return str(result).strip() 