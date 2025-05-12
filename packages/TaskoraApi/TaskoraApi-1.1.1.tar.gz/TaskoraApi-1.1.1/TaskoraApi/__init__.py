__TITLE__ = "TaskoraApi"
__VERSION__ = "1.1.1"
__AUTHOR__ = "SAM"
__EMAIL__ = "taskorabot@gmail.com"
__LICENCE__ = "MIT"
__DISCORD__ = "https://discord.com/invite/wMkKzGtAuQ"
__GITHUB__ = "https://github.com/taskorabot/TaskoraApi.git"


from .InstagramApi.aiohttp_client import AiohttpInstagramAPI
from .InstagramApi.httpx_client import HttpxInstagramAPI
from .InstagramApi.requests_client import RequestsInstagramAPI
from .QuizApi.aiohttp_client import AiohttpQuizAPI
from .QuizApi.httpx_client import HttpxQuizAPI
from .QuizApi.requests_client import RequestQuizAPI
from .reCaptchaV3Solver.client import AiohttpreChaptchaAPI
from .reCaptchaV3Solver.client import HttpxreChaptchaAPI
from .reCaptchaV3Solver.client import RequestsreChaptchaAPI
from .chatBot.client import AiohttpChatbotAPI
from .chatBot.client import HttpxChatbotAPI
from .chatBot.client import RequestsChatbotAPI

from json import loads
from requests import get

__all__ = [
    "AiohttpInstagramAPI",
    "HttpxInstagramAPI",
    "RequestsInstagramAPI",
    "AiohttpQuizAPI",
    "HttpxQuizAPI",
    "RequestQuizAPI",
    "AiohttpreChaptchaAPI",
    "HttpxreChaptchaAPI",
    "RequestsreChaptchaAPI",
    "AiohttpChatbotAPI",
    "HttpxChatbotAPI",
    "RequestsChatbotAPI",
    "__VERSION__",
    "__AUTHOR__",
    "__EMAIL__",
    "__LICENCE__",
    "__DISCORD__",
    "__GITHUB__"
]


__newest__ = loads(get("https://pypi.org/pypi/TaskoraApi/json").text)["info"]["version"]

if __VERSION__ != __newest__:
    print(f"New version of {__TITLE__} available: {__newest__} (Using {__VERSION__})")
    print("Visit our discord - https://discord.com/invite/wMkKzGtAuQ")