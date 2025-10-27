# Discord Bot

## Instalace

1. Klonuj repozitář:
   git clone https://github.com/uzivatel/discord-bot-project.git

2. Vytvoř virtuální prostředí:
   python -m venv venv
   pro windows: .\venv\Scripts\Activate.ps1
   pro linux: source venv/bin/activate


4. Nainstaluj knihovny:
   pip install -r requirements.txt

5. Vytvoř soubor `.env` a vlož token:
   DISCORD_TOKEN=tvuj_token_z_discord_portalu

6. Spusť bota passive:
   python main.py --mode passive --out .\exports

7. Spusť bota active:
   python main.py --mode active --out .\exports --channels "channel ID"
