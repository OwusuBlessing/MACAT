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
from email.mime.application import MIMEApplication
from fastapi import UploadFile
load_dotenv()
from typing import Optional
from uvicorn import run
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from src.macat.transcriber import Transcriber
from src.macat.bot import refine_transcription
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="add any string...")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"], 
)


USER_ID = 0
oauth = OAuth()
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_id=os.getenv("CLIENT_ID_5"),
    client_secret=os.getenv("CLIENT_SECRET_5"),
    client_kwargs={
        'scope': 'email openid profile https://www.googleapis.com/auth/gmail.send',
        'redirect_uri': 'http://localhost:8000/auth'
    }
)
templates = Jinja2Templates(directory="templates")
@app.get("/")
def index(request: Request):
    """user = request.session.get('user')
    if user:
        return RedirectResponse('chat')"""

    return templates.TemplateResponse(
        name="login.html",
        context={"request": request})

@app.get('/auth')
async def auth(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as e:
        return templates.TemplateResponse(
            name='error.html',
            context={'request': request, 'error': e.error}
        )
    user = token.get('userinfo')
    if user:
        request.session['user'] = dict(user)
        request.session['access_token'] = token['access_token']
    

        # Save user information as JSON
        with open('users.json', 'a') as file:
            json.dump(dict(user), file)
            file.write('\n')
    return RedirectResponse('home_page')

@app.get("/login")
async def login(request: Request):
    url = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, url)

@app.get('/logout')
def logout(request: Request):
    request.session.pop('user')
    request.session.clear()
    return RedirectResponse('/')

@app.get("/home_page")
async def get_chat(request: Request):
    user = request.session.get('user')

    if not user:
         return RedirectResponse('/')
    # The `request` parameter is required for url_for to work
    #user if does not esit
    print(user)
    #print(f"{user["name"]}", f"{user["email"]}")
    #userid = get_user_id(f"{user["name"]}", f"{user["email"]}")

    #print(f"resID{userid}")
    #set user id when logged in
    #request.session['user_id'] = userid

    return templates.TemplateResponse(name="home_page.html", 
                                      context = {"request": request,"user":user})

@app.get("/user/record_audio")
async def get_chat(request: Request):
    user = request.session.get('user')

    if not user:
         return RedirectResponse('/')

    return templates.TemplateResponse(name="record_audio.html", 
                                      context = {"request": request,"user":user})
@app.get("/user/upload_audio")
async def get_chat(request: Request):
    user = request.session.get('user')

    if not user:
         return RedirectResponse('/')
    return templates.TemplateResponse(name="upload_audio.html", 
                                      context = {"request": request,"user":user})

@app.get("/user/upload_video")
async def get_chat(request: Request):
    user = request.session.get('user')

    if not user:
         return RedirectResponse('/')
    return templates.TemplateResponse(name="upload_video.html", 
                                      context = {"request": request,"user":user})
@app.post("/user/save_audio")
async def save_audio(request: Request, file: UploadFile = File(...), speaker_identification: str = Form(...)):
    try:
        uploads_dir = "static/uploads"
        if not os.path.exists(uploads_dir):
            os.makedirs(uploads_dir)
        file_location = f"{uploads_dir}/audio.wav"

        print(f"Saving file to: {file_location}")
        
        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())

        # Log the speaker identification option
        print(f"Speaker Identification: {speaker_identification}")
        transcriber = Transcriber(speak_identifier=speaker_identification)
        result = transcriber.transcribe_file(file_location, "audio")
        print(result)

        if result["status"] == "success":
            return templates.TemplateResponse(name="transcribe_out.html", 
                                              context={"request": request, "text": result["text"]})
        else:
            return templates.TemplateResponse(name="transcribe_out.html", 
                                              context={"request": request, "text": "Error in transcribing, try again"})
    except Exception as e:
        print(f"Error saving file: {e}")
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)

@app.post("/user/save_video")
async def save_video(request: Request, file: UploadFile = File(...)):
    try:
        uploads_dir = "static/uploads"
        if not os.path.exists(uploads_dir):
            os.makedirs(uploads_dir)
        file_location = f"{uploads_dir}/video.mp4"

        print(f"Saving file to: {file_location}")
        
        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())

        transcriber = Transcriber()
        result = transcriber.transcribe_file(file_location, "video")
        if result["status"] == "success":
            return templates.TemplateResponse(name="transcribe_out.html", 
                                              context={"request": request, "text": result["text"]})
        else:
            return templates.TemplateResponse(name="transcribe_out.html", 
                                              context={"request": request, "text": "Error in transcribing, try again"})
    except Exception as e:
        print(f"Error saving file: {e}")
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)


@app.post("/user/topic_model_text")
async def topic_model_text(request: Request, transcription: str = Form(...), role: str = Form(...)):
    try:
        refined_text = refine_transcription(transcription, role)
        if refined_text:
            return JSONResponse(content={"text": refined_text})
        else:
            return JSONResponse(content={"error": "Error in processing the transcription."}, status_code=400)
    except Exception as e:
        print(f"Error processing transcription: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)
       

    except Exception as e:
        print(f"Error saving file: {e}")
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)

if __name__ == "__main__":
    run("main:app", host="0.0.0.0", port=8000, reload=True)



