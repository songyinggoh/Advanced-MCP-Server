from fastmcp import FastMCP
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from starlette.requests import Request as StarletteRequest
from starlette.responses import JSONResponse
from fastmcp.server.auth import BearerAuthProvider
from fastmcp.server.dependencies import get_access_token,AccessToken
import os

load_dotenv()

auth=BearerAuthProvider(
    jwks_uri=f"{os.getenv('STYTCH_DOMAIN')}/.well-known/jwks.json"
    issuer=os.getenv("STYTCH_DOMAIN"),
    algoritm="RS256",
    audience=os.getenv("STYTCH_PROJECT_ID"),
)

mcp=FastMCP(name="Notes App")

@mcp.tool()
def get_my_notes()->str:
    """Get all notes for user"""
    return "No notes"

@mcp.tool()
def add_note(content:str)->str:
    """Add a note for user"""
    return f"added note: {content}"

if __name__=="__main__":
    mcp.run(
        transport="http",
        host="127.0.0.1",
        port=8000,
        middleware=[
            Middleware(
                CORSMiddleware,
                allow_origins=["*"],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )
        ]
    )