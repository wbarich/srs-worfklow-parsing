import os

from langchain_openai import AzureChatOpenAI

from dotenv import load_dotenv

def return_azure_llm():
    llm = AzureChatOpenAI(azure_deployment=os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME_GPT3'), 
                                model_name=os.getenv('AZURE_OPENAI_MODEL_NAME_GPT3'),
                                api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                                azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT'),
                                api_version=os.getenv('AZURE_OPENAI_VERSION'))
    return llm    

if __name__ == "__main__":
    load_dotenv(".env")
    llm = return_azure_llm()
    print(llm.invoke("hello"))