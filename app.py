import os
from datetime import datetime

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-key")

VENDOR_ID = os.getenv("VENDOR_ID", "VENDOR")
AFFILIATE_ID = os.getenv("AFFILIATE_ID", "AFFILIATE")
META_PIXEL_ID = os.getenv("META_PIXEL_ID", "")
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID", "")
GOOGLE_CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS_FILE", "credentials.json")


def append_to_sheet(row_data):
    """Append a row to the configured Google Sheet."""
    import gspread
    from google.oauth2.service_account import Credentials

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = Credentials.from_service_account_file(GOOGLE_CREDENTIALS_FILE, scopes=scopes)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(GOOGLE_SHEET_ID).sheet1
    sheet.append_row(row_data)


@app.route("/")
def index():
    return render_template("index.html", meta_pixel_id=META_PIXEL_ID)


@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "error": "Invalid request"}), 400

    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    phone = data.get("phone", "").strip()

    if not name or not email or not phone:
        return jsonify({"success": False, "error": "Name, email, and phone are required"}), 400

    row = [
        datetime.utcnow().isoformat(),
        name,
        email,
        phone,
        request.remote_addr,
        request.headers.get("User-Agent", ""),
        data.get("fbclid", ""),
        data.get("ad_id", ""),
        data.get("adset_id", ""),
        data.get("campaign_id", ""),
        data.get("ad_name", ""),
        data.get("adset_name", ""),
        data.get("campaign_name", ""),
    ]

    try:
        append_to_sheet(row)
    except Exception as e:
        app.logger.error(f"Failed to write to Google Sheet: {e}")

    hoplink = f"https://{AFFILIATE_ID}.{VENDOR_ID}.hop.clickbank.net"
    return jsonify({"success": True, "redirect_url": hoplink})


if __name__ == "__main__":
    port = int(os.getenv("DATABRICKS_APP_PORT", os.getenv("PORT", 5000)))
    app.run(host="0.0.0.0", port=port)
