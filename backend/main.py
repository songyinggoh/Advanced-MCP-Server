from fastmcp import FastMCP
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from starlette.requests import Request as StarletteRequest
from starlette.responses import JSONResponse
from fastmcp.server.auth import BearerAuthProvider
from fastmcp.server.dependencies import get_access_token,AccessToken
from database import NoteRepository
import os

load_dotenv()

auth=BearerAuthProvider(
    jwks_uri=f"{os.getenv('STYTCH_DOMAIN')}/.well-known/jwks.json",
    issuer=os.getenv("STYTCH_DOMAIN"),
    algorithm="RS256",
    audience=os.getenv("STYTCH_PROJECT_ID"),
)

mcp=FastMCP(name="Notes App")

@mcp.tool()
def get_my_notes()->str:
    """Get all notes for user"""
    access_token:AccessToken=get_access_token()
    user_id=access_token.user_id
    notes=NoteRepository.get_notes_by_user(user_id)
    if not notes:
        return "no notes found"
    
    result="Your notes;\n"

    for note in notes:
        result+=f"{notes.id}:{note.content}\n"

    return result



@mcp.tool()
def add_note(content:str)->str:
    """Add a note for user"""
    access_token:AccessToken=get_access_token()
    user_id=access_token.user_id
    note=NoteRepository.create_note(user_id,content)
    return f"added note: {note.content}"

@mcp.custom_route(path="/.well-known/oauth-protected-resource", methods=["GET","OPTIONS"])
def oauth_metadata(request:StarletteRequest)->JSONResponse:
    base_url=str(request.base_url).rstrip("/")

    return JSONResponse(
        {
            "resource":base_url,
            #tells MCP client location of auth server
            "authorization_servers":[os.getenv("STYTCH_DOMAIN")],
            "scopes_supported":["read","write"],
            #auth token is either in the head or body of request
            "bearer_methods_supported":["header","body"]
        }
    )

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