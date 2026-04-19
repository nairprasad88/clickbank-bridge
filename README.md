# ClickBank Bridge Page

A Flask-based bridge page that sits between Facebook Ads and a ClickBank hoplink. Captures lead details and Facebook ad parameters, stores them in Google Sheets, fires a Meta Pixel Lead event, and redirects to the ClickBank offer.

## Prerequisites

- Python 3.8+
- A Google Cloud service account with Sheets API enabled
- A Meta (Facebook) Pixel ID
- A ClickBank affiliate account (vendor ID + affiliate ID)

## Google Sheets Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project (or select existing)
3. Enable the **Google Sheets API** and **Google Drive API**
4. Create a **Service Account** and download the JSON credentials file
5. Save the credentials file as `credentials.json` in this directory
6. Create a Google Sheet and share it (Editor access) with the service account email (found in `credentials.json` under `client_email`)
7. Copy the Sheet ID from the URL: `https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit`
8. Optionally add headers to Row 1: `Timestamp, Name, Email, Phone, IP Address, User Agent, fbclid, ad_id, adset_id, campaign_id, ad_name, adset_name, campaign_name`

## Meta Pixel Setup

1. Go to [Meta Events Manager](https://business.facebook.com/events_manager)
2. Create or select a Pixel
3. Copy the Pixel ID

## Installation

```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your values
```

## Configuration

Edit `.env` with your actual values:

| Variable | Description |
|---|---|
| `VENDOR_ID` | ClickBank vendor (product) ID |
| `AFFILIATE_ID` | Your ClickBank affiliate ID |
| `META_PIXEL_ID` | Facebook/Meta Pixel ID |
| `GOOGLE_SHEET_ID` | Google Sheets document ID |
| `GOOGLE_CREDENTIALS_FILE` | Path to service account JSON (default: `credentials.json`) |
| `FLASK_SECRET_KEY` | A random secret key for Flask sessions |
| `PORT` | Port to run the server on (default: 5000) |

## Running

```bash
python app.py
```

Open in browser: `http://localhost:5000/`

## Testing with Facebook Ad Parameters

Open with sample URL params to simulate traffic from Facebook Ads:

```
http://localhost:5000/?fbclid=test123&ad_id=456&adset_id=789&campaign_id=101&ad_name=TestAd&adset_name=TestAdset&campaign_name=TestCampaign
```

Verify:
- The form renders with hidden fields populated
- Submitting the form posts to `/submit`
- A redirect URL is returned and the browser navigates to the hoplink
- Without `credentials.json`, the submit still returns a redirect (Sheets failure is logged but non-blocking)
