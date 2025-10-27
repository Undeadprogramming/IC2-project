# main.py
import os
import argparse
import asyncio
import json
import csv
from datetime import datetime, timezone
import logging
from dotenv import load_dotenv
import discord  # py-cord

# -----------------------
# Načtení tokenu z .env
# -----------------------
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# -----------------------
# Logování
# -----------------------
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
logger = logging.getLogger("extractor")

# -----------------------
# Funkce pro uložení dat
# -----------------------
def save_json(items, out_path):
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
    logger.info(f"Uloženo JSON: {out_path}")

def save_csv(items, out_path):
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    if not items:
        logger.warning("Žádná data k uložení do CSV.")
        return
    keys = sorted({k for it in items for k in it.keys()})
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for it in items:
            writer.writerow({k: it.get(k, "") for k in keys})
    logger.info(f"Uloženo CSV: {out_path}")

# -----------------------
# Převod zprávy na dict
# -----------------------
def message_to_record(msg: discord.Message):
    return {
        "id": str(msg.id),
        "channel_id": str(msg.channel.id),
        "channel_name": getattr(msg.channel, "name", ""),
        "guild_id": str(msg.guild.id) if msg.guild else "",
        "guild_name": msg.guild.name if msg.guild else "",
        "author_id": str(msg.author.id),
        "author_name": str(msg.author),
        "timestamp": msg.created_at.replace(tzinfo=timezone.utc).isoformat(),
        "content": msg.content,
        "attachments": [a.url for a in msg.attachments],
        "embeds": [str(e.to_dict()) for e in msg.embeds],
        "pinned": msg.pinned,
        "edited_timestamp": msg.edited_at.isoformat() if msg.edited_at else "",
    }

# -----------------------
# Hlavní třída bota
# -----------------------
class ExtractorBot(discord.Client):
    def __init__(self, out_dir, active=False, channel_filter=None, **kwargs):
        super().__init__(**kwargs)
        self.out_dir = out_dir
        self.active = active
        self.channel_filter = channel_filter
        logger.info(f"Bot inicializován. Režim active={active}, výstupní složka={out_dir}")

    async def on_ready(self):
        logger.info(f"Přihlášen jako {self.user} (id: {self.user.id})")

        # 🟢 Vypiš všechny servery a kanály
        logger.info("============== DISCORD PŘEHLED ==============")
        for guild in self.guilds:
            logger.info(f"Server: {guild.name} ({guild.id})")
            for channel in guild.text_channels:
                logger.info(f" ├─ #{channel.name} ({channel.id})")
        logger.info("=============================================")

        if self.active:
            await self.bulk_export()
        else:
            logger.info("Pasivní režim: čekám na nové zprávy...")

    async def bulk_export(self):
        """Aktivní režim – stáhne historii zpráv"""
        all_records = []
        for guild in self.guilds:
            logger.info(f"Zpracovávám server: {guild.name} ({guild.id})")
            for channel in guild.text_channels:
                if self.channel_filter:
                    if (str(channel.id) not in self.channel_filter) and (channel.name not in self.channel_filter):
                        continue
                logger.info(f"Stahuji historii kanálu: #{channel.name}")
                try:
                    async for msg in channel.history(limit=500):
                        all_records.append(message_to_record(msg))
                except Exception as e:
                    logger.error(f"Chyba při čtení kanálu {channel.name}: {e}")

        timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        save_json(all_records, os.path.join(self.out_dir, f"export_{timestamp}.json"))
        save_csv(all_records, os.path.join(self.out_dir, f"export_{timestamp}.csv"))
        logger.info("Aktivní export dokončen.")

    async def on_message(self, message):
        """Pasivní režim – ukládá nové zprávy v reálném čase"""
        if message.author == self.user:
            return
        if self.channel_filter:
            if (str(message.channel.id) not in self.channel_filter) and (message.channel.name not in self.channel_filter):
                return
        record = message_to_record(message)
        date_key = message.created_at.strftime("%Y-%m-%d")
        out_json = os.path.join(self.out_dir, f"live_{date_key}.json")

        existing = []
        if os.path.exists(out_json):
            try:
                with open(out_json, "r", encoding="utf-8") as f:
                    existing = json.load(f)
            except Exception:
                existing = []
        existing.append(record)
        save_json(existing, out_json)
        logger.info(f"Zachycena nová zpráva ({record['id']}) v {out_json}")

# -----------------------
# Nastavení Intents
# -----------------------
def build_intents():
    intents = discord.Intents.default()
    intents.guilds = True
    intents.members = True
    intents.messages = True
    intents.message_content = True
    return intents

# -----------------------
# Hlavní funkce
# -----------------------
def main():
    parser = argparse.ArgumentParser(description="Discord Data Extractor")
    parser.add_argument("--mode", choices=["passive", "active", "both"], default="both",
                        help="Režim běhu: passive, active nebo both")
    parser.add_argument("--out", default="./exports", help="Výstupní složka")
    parser.add_argument("--channels", nargs="*", help="Seznam kanálů (ID nebo názvy) pro filtraci")
    args = parser.parse_args()

    if not TOKEN:
        logger.error("Nebyl nalezen DISCORD_TOKEN v .env! Ukončuji.")
        return

    intents = build_intents()
    bot = ExtractorBot(
        out_dir=args.out,
        active=(args.mode in ("active", "both")),
        channel_filter=args.channels or None,
        intents=intents
    )

    bot.run(TOKEN)

if __name__ == "__main__":
    main()
