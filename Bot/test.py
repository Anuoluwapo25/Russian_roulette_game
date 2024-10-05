import requests

BOT_TOKEN = '7618149231:AAEexKMU147voLpVvfbTc_av4ZRMsShiYQ4'
url = f"https://api.telegram.org/bot{BOT_TOKEN}/getMe"
response = requests.get(url)
print(response.json())
