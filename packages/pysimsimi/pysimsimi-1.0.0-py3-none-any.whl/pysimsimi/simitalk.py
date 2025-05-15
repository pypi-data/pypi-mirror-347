import requests

HEADERS = {
    'sec-ch-ua-platform': '"Android"',
    'Referer': 'https://simi.anbuinfosec.live/',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Mobile Safari/537.36',
    'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
    'Content-Type': 'application/json',
    'sec-ch-ua-mobile': '?1'
}

def simitalk(ask, language):
    try:
        response = requests.post(
            'https://simi.anbuinfosec.live/api/chat',
            json={'ask': ask, 'lc': language},
            headers=HEADERS
        )
        data = response.json()
        return data.get('message', 'No message received.')
    except Exception:
        return 'An error occurred. Author: https://facebook.com/anbuinfosec'
