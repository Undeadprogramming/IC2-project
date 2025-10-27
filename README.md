# Discord Bot

## Instalace

1. Klonuj repozitář:
   git clone https://github.com/uzivatel/discord-bot-project.git

2. Vytvoř virtuální prostředí:
   python -m venv venv
   .\venv\Scripts\Activate.ps1

3. Nainstaluj knihovny:
   pip install -r requirements.txt

4. Vytvoř soubor `.env` a vlož token:
   DISCORD_TOKEN=tvuj_token_z_discord_portalu

5. Spusť bota:
   python main.py --mode passive --out .\exports
