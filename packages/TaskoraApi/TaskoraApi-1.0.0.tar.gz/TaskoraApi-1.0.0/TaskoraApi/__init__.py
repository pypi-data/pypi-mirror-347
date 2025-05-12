__VERSION__ = "1.0.0"
__AUTHOR__ = "SAM"
__EMAIL__ = "taskorabot@gmail.com"
__LICENCE__ = "MIT"
__DISCORD__ = ""
__GITHUB__ = ""


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

