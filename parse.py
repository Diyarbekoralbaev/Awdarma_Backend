import aiohttp

class GoogleTranslator:
    def __init__(self, source='auto', target='en'):
        self.source = source
        self.target = target
        self.base_url = "https://translate.googleapis.com/translate_a/single"

    async def translate(self, text):
        params = {
            'client': 'gtx',
            'sl': self.source,
            'tl': self.target,
            'dt': 't',
            'q': text
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url, params=params) as response:
                if response.status != 200:
                    raise Exception("Error in translation request")
                data = await response.json()
                translated_text = ''.join([item[0] for item in data[0]])
                return translated_text


