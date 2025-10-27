from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client
from mcp import StdioServerParameters, ClientSession
from groq import Groq
from dotenv import load_dotenv
import asyncio
from utils import response_with_llm
load_dotenv()

server_params=StdioServerParameters(
    command="uv",
    args=["run","mcp_server.py"],
    env=None,
)
async def main():
    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            tool_exit = await session.list_tools()
            # print("Available tools:", [t.name for t in tool_exit.tools])

            query = "How to install chromadb using langchain?"
            library = "langchain"
            res =  await session.call_tool(
                "fetch_official_docs",
                 arguments={"query":query, "library":library},
            )

            context = res.content
            user_prompt_with_context = f"""Using the following documentation context, answer the question: {query}\n\nDocumentation Context:\n{context}"""
            SYSTEM_PROMPT = """Answer ONLY using the provided context. If info is missing say you don't know.
            Keep every 'SOURCE:' line exactly; list sources at the end."""

            result = response_with_llm(user_prompt=user_prompt_with_context, system_prompt = SYSTEM_PROMPT , model = "openai/gpt-oss-20b")
            print("Final Answer:\n", result)






if __name__ == "__main__":
    asyncio.run(main())