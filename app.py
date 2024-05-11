import time

from flask import Flask, url_for, redirect, session
from authlib.integrations.flask_client import OAuth
import sys
import os
from openai import OpenAI

sys.path.append(os.path.join(os.path.dirname(__file__), 'Suno-API'))


import schemas
from deps import get_token, get_token_flask
from fastapi import Depends, FastAPI, HTTPException, Request, status
from utils import generate_music, download_song

app = Flask(__name__)
app.secret_key = 'MAGIC KABOOOMJIEDJFGDF'

oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id='', #Mettre votre client id
    client_secret='', #Mettre votre client secret, faut faire une application sur google console dev
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={
        'scope': 'email profile https://www.googleapis.com/auth/youtube.readonly https://www.googleapis.com/auth/user.birthday.read https://www.googleapis.com/auth/contacts https://www.googleapis.com/auth/user.gender.read https://www.googleapis.com/auth/user.phonenumbers.read',
    },
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration'
)

client = OpenAI(
    api_key='',  #Mettre votre clé api 
)

@app.route("/")
def hello_world():
    email = dict(session).get('email',None)
    birthday = dict(session).get('birthday',None)
    return f"<p>Hello {email} and {birthday}</p>"

@app.route('/login')
def login():
    google = oauth.create_client('google')
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize')
async def authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()

    #Basic user info
    resp = google.get('userinfo')
    #Number of everyone LOL
    resp2 = google.get('https://people.googleapis.com/v1/people/me/connections', params={'personFields': 'names,emailAddresses,birthdays,genders,biographies,skills,phoneNumbers,occupations,addresses,genders,calendarUrls,ageRanges', 'pageSize': 100},)


    resp.raise_for_status()
    resp2.raise_for_status()

    contacts = resp2.json()
    print(contacts)
    user_info = resp.json()
    # do something with the token and profile
    session['email'] = user_info['email']

    data = schemas.CustomModeGenerateParam
    token_suno = get_token_flask()


    #OpenAI Call
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "Genere les paroles d'un slam où le chanteur parle à l'utilisateur et lui montre que Google sait tout le de lui en disant les nom de la donnée et sa valeur. Ensure the lyrics do not include apostrophes or commas aligning with the given stylistic requirements. Do not exceed 210 words"
             },
            {"role": "user","content": "Léo Martin, 18 ans, Étudiant en informatique, Montpellier, France. Intérêts : Jeux vidéo, musique électronique, streaming sur Twitch, technologies émergentes. Numéro de téléphone : +33 6 78 90 12 34, E-mail : leo.martin@jeuxexemple.com, Adresse : 450 Rue de lUniversité, 34000 Montpellier, France. Parents : Claire Martin (+33 6 12 34 56 78), Jacques Martin (+33 6 87 65 43 21). Meilleurs amis : Émilie Dupont (+33 6 75 43 21 90), Tom Renault (+33 6 89 76 54 32). Dernières recherches Google : Meilleurs PC gaming 2024, Prochains tournois eSports en France, Comment améliorer le streaming sur Twitch. Vidéos YouTube likées : Guide complet pour optimiser votre setup de streaming, Highlights du tournoi Fortnite 2024, Nouveautés musique électronique cette semaine. Documents Google Drive : Exposé sur lintelligence artificielle.pdf, Liste des jeux à tester.txt, Planning des streams Twitch Mars 2024.xlsx. Lieux visités : Paris Games Week, FNAC, Salle de concert à Montpellier. Dernière vacance : Tokyo, Japon. Prochains rendez-vous : Tournoi local de League of Legends, Rendez-vous avec lorienteur universitaire, Concert de Petit Biscuit à Montpellier. Marques préférées : Razer, NVIDIA, Red Bull. Derniers e-mails : Confirmation de votre inscription au tournoi LoL, Rappel de paiement pour le concert de Petit Biscuit, Offre spéciale de NVIDIA pour les étudiants."}
        ],
        temperature=0.8
    )
    lyrics = completion.choices[0].message.content
    print(lyrics)

    song_details = {
        "prompt": lyrics,
        "mv": "chirp-v3-0",
        "title": "Test avec gpt",
        "tags": "indie"
    }

    generated_music = await generate_music(song_details, token_suno)
    print(generated_music)
    song_id = generated_music['id']
    clip_id = generated_music['clips'][0]['id']
    print('id du clip '+clip_id)
    time.sleep(30)
    downloaded_song = await download_song(song_id, token_suno)

    return redirect('https://audiopipe.suno.ai/?item_id='+str(clip_id))
