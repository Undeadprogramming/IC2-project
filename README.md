# Discord Bot

## Instalace pro windows

1. Klonuj repozitář:
   git clone https://github.com/uzivatel/discord-bot-project.git

2. Vytvoř virtuální prostředí:
   python -m venv venv
   pro windows: .\venv\Scripts\Activate.ps1
   pro linux: source venv/bin/activate

3. Nainstaluj knihovny:
   pip install -r requirements.txt

4. Vytvoř soubor `.env` a vlož token:
   DISCORD_TOKEN=tvuj_token_z_discord_portalu

5. Spusť bota passive:
   python main.py --mode passive --out .\exports

6. Spusť bota active:
   python main.py --mode active --out .\exports --channels "channel ID"


## Instalace pro linux

1. Klonuj repozitář:  
   git clone https://github.com/uzivatel/discord-bot-project.git
   cd discord-bot-project

2. Vytvoř virtuální prostředí:

python -m venv venv

3. Aktivuj virtuální prostředí:

source venv/bin/activate

4. Nainstaluj potřebné knihovny:

pip install -r requirements.txt

5. Vytvoř soubor .env a vlož svůj Discord token:

DISCORD_TOKEN=tvuj_token_z_discord_portalu

6. Spuštění bota

Passive režim:

python main.py --mode passive --out ./exports


Active režim (uved konkrétní ID kanálů):

python main.py --mode active --out ./exports --channels "ID_kanalu1,ID_kanalu2"