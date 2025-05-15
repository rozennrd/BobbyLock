#!/usr/bin/env python3
"""
PcAlertListenerEmail.py
Écoute le topic MQTT /Junia/Bobby/alert et envoie un e-mail dès qu’une alerte est reçue.
"""

import json
import os
import ssl
import smtplib
from email.mime.text import MIMEText
import paho.mqtt.client as mqtt

# ─── Configuration MQTT ─────────────────────────────────────────────────────────
BROKER = "10.40.150.20"
PORT   = 1883
TOPIC  = "/Junia/Bobby/request"

# ─── Configuration e-mail ───────────────────────────────────────────────────────
SENDER    = "dave.junia.ap4@gmail.com"
PASSWORD  = "otlpdjsmjaycgstx"
RECIPIENT = "bobby.alert@yopmail.com"
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587           # TLS

# ────────────────────────────────────────────────────────────────────────────────
def send_mail(body: str) -> None:
    """Envoie un courriel via SMTP/TLS (Gmail)."""
    msg = MIMEText(body)
    msg["Subject"] = "Alerte – Présence détectée"
    msg["From"]    = SENDER
    msg["To"]      = RECIPIENT

    context = ssl.create_default_context()
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as server:
        server.starttls(context=context)
        server.login(SENDER, PASSWORD)
        server.send_message(msg)

    print(f"[MAIL] Message envoyé à {RECIPIENT}")

# ─── Callbacks MQTT ─────────────────────────────────────────────────────────────
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"[MQTT] Connecté à {BROKER}")
        client.subscribe(TOPIC)
        print(f"[MQTT] Abonné au topic {TOPIC}")
    else:
        print(f"[MQTT] Connexion échouée (code {rc})")

def on_message(client, userdata, msg):
    print(f"[MQTT] {msg.topic}: {msg.payload.decode()}")
    try:
        payload = json.loads(msg.payload.decode())
        texte = payload.get("message", "Alerte reçue (pas de champ 'message')")
    except json.JSONDecodeError:
        texte = msg.payload.decode()

    try:
        send_mail(texte)
    except Exception as e:
        print(f"[ERR] Envoi e-mail échoué : {e}")

# ─── Boucle principale ─────────────────────────────────────────────────────────
def main() -> None:
    # Optionnel : autoriser le mot de passe via variable d’environnement
    global PASSWORD
    if not PASSWORD:
        PASSWORD = os.getenv("MAIL_PWD", "")

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(BROKER, PORT, keepalive=60)
    except Exception as e:
        print(f"[ERR] Impossible de se connecter au broker : {e}")
        return

    print("[SYS] En écoute – Ctrl-C pour quitter")
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("\n[SYS] Arrêt demandé. À bientôt !")

if __name__ == "__main__":
    main()
