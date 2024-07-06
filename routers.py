from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth, OAuthError
import os
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import json
from authlib.integrations.starlette_client import OAuth, OAuthError
import google.auth
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64
import google.auth
from email.mime.application import MIMEApplication
from fastapi import UploadFile
load_dotenv()
from typing import Optional

router = APIRouter()
templates = Jinja2Templates(directory="templates")
@router.get("/")
def index(request: Request):
    """user = request.session.get('user')
    if user:
        return RedirectResponse('chat')"""

    return templates.TemplateResponse(
        name="login.html",
        context={"request": request})

@router.get("/login")
async def login(request: Request):
    url = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, url)