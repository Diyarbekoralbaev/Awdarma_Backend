from fastapi import FastAPI, HTTPException, Header, Body
from fastapi.middleware.cors import CORSMiddleware
from parse import GoogleTranslator
import aiohttp
import json
import requests
from pydantic import BaseModel
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

users = {"Diyarbek": "diyarbek"}

bot_token = "6474796928:AAGJOqIVHeSw5l5PiPOM34EnsTfsKRO_I0c"
bot_chat_id = '6185590222'


class diyar(BaseModel):
    text: str
    lang_from: str
    lang_to: str


def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {'chat_id': chat_id, 'text': text}
    response = requests.post(url, params=params)
    return response.json()


async def trkaa(lang_from, lang_to, text):
    url = "https://api.from-to.uz/api/v1/translate"
    headers = {"Content-Type": "application/json"}
    payload = {
        "resultCase": "latin",
        "lang_from": lang_from,
        "lang_to": lang_to,
        "text": text,
    }
    payload_json = json.dumps({"body": payload})

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload_json, headers=headers) as response:
            response.raise_for_status()
            result = await response.json()

    return result


@app.get('/')
def hello_world():
    return 'API created by python developer Diyarbek Oralbaev. https://t.me/Diyarbek_Blog/'


@app.post('/awdarma')
async def translate(diyar: diyar):
        if diyar.text != "":
            text1 = diyar.text
            lang_from = diyar.lang_from
            lang_to = diyar.lang_to

            if lang_from != 'kaa' and lang_to != 'kaa':
                text = await GoogleTranslator(
                    source=lang_from, target=lang_to).translate(str(text1))
                return {
                    'awdarma': text,
                    'jaratiwshi': 'Diyarbek Oralbaev',
                    'blog': 'https://diyarbek.uz/'
                }

            elif lang_to == 'kaa':
                if lang_from == 'uz':
                    response = await trkaa("uz", "kaa", str(text1))
                    response = response['result']
                else:
                    text = await GoogleTranslator(
                        source=lang_from, target='uz').translate(str(text1))
                    response = await trkaa("uz", "kaa", text)
                    response = response['result']
            elif lang_from == 'kaa':
                kaaa = await trkaa("kaa", "uz", text1)
                response = await GoogleTranslator(
                    source='uz', target=lang_to).translate(kaaa['result'])
            elif lang_from == lang_to:
                response = text1
            return {
                'awdarma': response,
                'jaratiwshi': 'Diyarbek Oralbaev',
                'blog': 'https://diyarbek.uz/'
            }
        else:
            return {
                "awdarma": "",
                "jaratiwshi": "Diyarbek Oralbaev",
                "blog": "https://diyarbek.uz/"
            }


@app.post('/send_message')
async def send_message_route(data: dict = Body(..., embed=True)):
    if 'number' in data and 'email' in data and 'message' in data:
        number = data['number']
        email = data['email']
        message = data['message']

        text = f"Phone: {number}\nGmail: {email}\nMessage: {message}"

        rs = send_message('-1001979868420', text)

        return {'success': True, 'message': 'Success'}
    else:
        raise HTTPException(
            status_code=400, detail={'success': False, 'message': 'Failed'}
        )

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8005)