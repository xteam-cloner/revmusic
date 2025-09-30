from pyrogram import Client
from pytgcalls import PyTgCalls

from xteam.configs import Var
from ..logging import LOGGER

api_id: int = Var.API_ID
api_hash: str = Var.API_HASH
session_string: str = Var.SESSION_STRING

YMusicBot = Client(
    name="YMusic", api_id=api_id, api_hash=api_hash, session_string=session_string
)

YMusicUser = PyTgCalls(YMusicBot)
