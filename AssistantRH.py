import asyncio
import os
import streamlit as st
from dotenv import load_dotenv

from azure.identity.aio import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from semantic_kernel.agents import AzureAIAgent, AzureAIAgentSettings

# Load configuration from .env file
load_dotenv()

# ----- Agent IDs Configuration -----
# Document Search Agent (Agent 1)
AGENT1_ID = "xxxxxx"
# Web Search Agent (Agent 2)
AGENT2_ID = "xxxxxx"
# Summary Agent (Agent 3)
AGENT3_ID = "xxxxxx"
# ----- Azure Project Configuration -----
PROJECT_CONN_STR = os.environ.get("AZURE_AI_PROJECT_CONNECTION_STRING")

# Agent icons
agent_icons = {
    "document": "📄",
    "web": "🌐",
    "summary": "🧠"
}
st.set_page_config(page_title="Assistant RH - Télétravail", layout="wide")
st.title("🤖 Assistant RH – Politique de télétravail")

# Sidebar
with st.sidebar:
    st.header("⚙️ Paramètres")
    st.markdown(f"{agent_icons['document']} **Agent Document ID**: `{AGENT1_ID}`")
    st.markdown(f"{agent_icons['web']} **Agent Web ID**: `{AGENT2_ID}`")
    st.markdown(f"{agent_icons['summary']} **Agent Résumé ID**: `{AGENT3_ID}`")

    # Inputs utilisateur 
    web_input = st.text_area("🌐 Question Agent Web", value="", placeholder="Demandez quelque chose")
    doc_input = st.text_area("📄 Question Agent Document", value="", placeholder="Demandez quelque chose")


async def main() -> None:

    # Initialize credentials and the Azure AI Projects client
    credential = DefaultAzureCredential()
    try:
        project_client = AIProjectClient.from_connection_string(
            conn_str=PROJECT_CONN_STR,
            credential=credential
        )
    except Exception as e:
        st.error(f"❌ Error initializing project client: {e}")
        return

    # Use the async context for proper cleanup of the credential and client
    async with credential, AzureAIAgent.create_client(credential=credential) as client:
        # Retrieve pre-created agent definitions for each role
        document_agent_def = await client.agents.get_agent(agent_id=AGENT1_ID)
        web_agent_def = await client.agents.get_agent(agent_id=AGENT2_ID)
        summary_agent_def = await client.agents.get_agent(agent_id=AGENT3_ID)

        # Instantiate Semantic Kernel agent objects
        document_agent = AzureAIAgent(client=client, definition=document_agent_def)
        web_agent = AzureAIAgent(client=client, definition=web_agent_def)
        summary_agent = AzureAIAgent(client=client, definition=summary_agent_def)
        

        # ----- Agent 1: Document Search Agent -----
        # Create a thread for Agent 1 and send the user's query as a chat message.
        with st.spinner(f"{agent_icons['document']} Agent Document en cours..."):
            thread1 = await client.agents.create_thread()
            response_doc = await document_agent.get_response(messages=doc_input, thread_id=thread1.id)
        with st.expander(f"{agent_icons['document']} Réponse de l’agent Document"):
            st.chat_message("assistant").markdown(response_doc.message.content)


        # ----- Agent 2: Web Search Agent -----
        # Perform a SERP API search with the user's query.
        with st.spinner(f"{agent_icons['web']} Agent Web en cours..."):
            thread2 = await client.agents.create_thread()
            response_web = await web_agent.get_response(messages=web_input, thread_id=thread2.id)
        with st.expander(f"{agent_icons['web']} Résultat de la recherche Web"):
            #st.chat_message("assistant").markdown(response_web.message.content)
            st.chat_message("assistant").markdown(response_web)


        # ----- Agent 3: Summary Agent -----
        # Préparer l'entrée pour le summarizer_agent
        #combined_input = f"Extrait 1 : {response_doc.message.content}\n\nExtrait 2 : {response_web.message.content}"
        combined_input = f"Extrait 1 : {response_doc.message.content}\n\nExtrait 2 : {response_web}"
        with st.spinner(f"{agent_icons['summary']} Agent Résumé en cours..."):
            thread3 = await client.agents.create_thread()
            response_summary = await summary_agent.get_response(messages=combined_input, thread_id=thread3.id)
        with st.expander(f"{agent_icons['summary']} Synthèse et recommandations RH"):
            st.chat_message("assistant").markdown(response_summary.message.content)

        # ----- Optional Cleanup: Delete the conversation threads -----
        for thread in [thread1, thread2, thread3]:
            try:
                await client.agents.delete_thread(thread.id)
            except Exception as e:
               st.warning(f"⚠️ Impossible de supprimer le thread {thread.id}: {e}")


if __name__ == "__main__":
    asyncio.run(main())