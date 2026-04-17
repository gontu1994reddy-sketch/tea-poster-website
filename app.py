import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
#from google import genai
from groq import Groq
import urllib.parse
import asyncio
from playwright.async_api import async_playwright
import tempfile
import base64
import os
import subprocess
import qrcode
from io import BytesIO
from datetime import datetime, timedelta
import gspread
from google.oauth2.service_account import Credentials
import random
import time



def read_sheet_direct():
    g = st.secrets["connections"]["gsheets"]
    creds_dict = {
        "type" : "service_account",
        "project_id" : g["project_id"],
        "private_key_id" : g["private_key_id"],
        "private_key" : g["private_key"].replace("\\n","\\n"),
        "client_email" : g["client_email"],
        "client_id" : g["client_id"],
        "auth_uri" : "https://accounts.google.com/o/oauth2/auth",
        "token_uri" : "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/{gs['client_email']}",
        }
            
    
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
        ]
    creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    gc = gspread.authorize(creds)

    for attempt in range(3):
        try:
            
            sh = gc.open_by_url(str(g["spreadsheet"]))
            records = sh.sheet1.get_all_records()  # always returns list of dicts
            return pd.DataFrame(records)
        except Exception as e:
            if attempt < 2:
                time.sleep(2)
                continue
            else:
                raise e    
def write_sheet_direct(df):
    g = st.secrets["connections"]["gsheets"]
    creds_dict = {
        "type": "service_account",
        "project_id": g["project_id"],
        "private_key_id": g["private_key_id"],
        "private_key": g["private_key"].replace("\\n", "\n"),
        "client_email": g["client_email"],
        "client_id": g["client_id"],
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": f"https://www.googleapis.com/robot/v1/metadata/x509/{g['client_email']}"
    }
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    gc = gspread.authorize(creds)
    for attempt in range(3):
        try:
            sh = gc.open_by_url(str(g["spreadsheet"]))
            worksheet = sh.sheet1
            worksheet.clear()
            worksheet.update(
                [df.columns.tolist()] + df.fillna("").astype(str).values.tolist()
            )
            return  # success
        except Exception as e:
            if attempt < 2:
                time.sleep(2)
                continue
            else:
                raise e
    
    

if not os.path.exists("/home/adminuser/.cache/ms-playwright"):
    subprocess.run(["playwright","install","chromium"])

# ---------------- CONFIG ----------------
groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.set_page_config(page_title="AI Poster Generator", layout="centered")
st.title("🎨 AI Poster Generator")

# ---------------- PREMIUM PAYMENT ----------------
PAYMENT_LINK = "https://rzp.io"   # your real UPI
PLAN_PRICE = 299

today = datetime.now().strftime("%Y-%m-%d")

if "poster_generated" not in st.session_state:
    st.session_state.poster_generated = False


st.markdown("---")
with st.form("poster_form", clear_on_submit=False):
    customer_phone = st.text_input("📞 Customer Phone")
    shop = st.text_input("🏪 Shop Name")
    offer = st.text_input("🔥 Offer")
    logo = st.file_uploader("📷 Upload Shop Logo", type=["png","jpg","jpeg"])
    shop_type = st.selectbox("Select Shop Type", [
        "Grocery shop","Tiffin center","Tea shop & Snacks","Clothing store",
        "Mobile shop","Salon","Medical store","Bakery","Fruit shop",
        "Bike repair","Tuition center","Real estate"
    ])
    customer_address = st.text_input("📍 Customer Address")
    language = st.selectbox("Language", ["English", "Telugu"])
    festival = st.selectbox("Festival", ["Special Offer","Ugadi","Diwali","Sankranti"])
    submitted = st.form_submit_button("🚀 Generate AI Poster")


sheet_data = pd.DataFrame()
user_row = pd.DataFrame()

if "last_phone" not in st.session_state:
    st.session_state.last_phone = ""

if customer_phone.strip() and customer_phone != st.session_state.last_phone:
   
    try:
        sheet_data = read_sheet_direct()
        st.session_state.sheet_data = sheet_data
        st.session_state.last_phone = customer_phone
    except Exception as e:
        st.error(f"Google sheet error: {e}")
        st.stop()

if "sheet_data" in st.session_state:
    sheet_data = st.session_state.sheet_data
    if isinstance(sheet_data, pd.DataFrame) and not sheet_data.empty and "Phone" in sheet_data.columns:
        sheet_data["Phone"] = sheet_data["Phone"].astype(str)
        user_row = sheet_data[sheet_data["Phone"] == str(customer_phone)]

# ---- USER STATUS ----
if not user_row.empty:
    st.session_state.poster_count = int(user_row.iloc[0]["PosterCount"]) if user_row.iloc[0]["PosterCount"] else 0
    st.session_state.is_premium = str(user_row.iloc[0]["Premium"]).upper() == "TRUE"
    expiry_col = str(user_row.iloc[0]["ExpiryDate"]) if "ExpiryDate" in user_row.columns else ""
    if st.session_state.is_premium and expiry_col:
        try:
            expiry = datetime.strptime(expiry_col.strip(), "%Y-%m-%d")
            if datetime.now() > expiry:
                st.session_state.is_premium = False
                st.warning("⚠️ Premium expired. Please renew ₹299.")
            else:
                days_left = (expiry - datetime.now()).days
                st.success(f"💎 Premium active | {days_left} days left")
        except:
            pass
else:
    if "poster_count" not in st.session_state:
        st.session_state.poster_count = 0
    if "is_premium" not in st.session_state:
        st.session_state.is_premium = False

# ---- STATUS DISPLAY ----
FREE_LIMIT = 3
remaining = FREE_LIMIT - st.session_state.poster_count

if st.session_state.is_premium:
    st.success("💎 Premium active: Unlimited posters")
elif remaining > 0:
    st.info(f"🎁 Free posters left: {remaining}")
    st.markdown(f"Want unlimited? [💎 Upgrade to Premium ₹{PLAN_PRICE}]({PAYMENT_LINK})")
else:
    st.error("🚫 Free posters used up!")
    st.markdown(f"""
    <a href="{PAYMENT_LINK}" target="_blank">
        <button style="background:#25D366;color:white;padding:14px 28px;
        border:none;border-radius:10px;font-size:18px;width:100%;cursor:pointer;">
        💎 Pay ₹{PLAN_PRICE} — Get 30 Posters / Month
        </button>
    </a>
    """, unsafe_allow_html=True)

# ---- PAYMENT ----
if st.button("✅ I Have Paid"):
    if not customer_phone.strip():
        st.error("Please enter phone number first.")
    else:
        expiry_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        premium_code = f"RAMA{customer_phone[-4:]}"
        latest = read_sheet_direct()
        latest["Phone"] = latest["Phone"].astype(str) if "Phone" in latest.columns else latest["Phone"]
        idx = latest[latest["Phone"] == str(customer_phone)].index if "Phone" in latest.columns else []
        if len(idx) > 0:
            latest.loc[idx[0], "Premium"] = True
            latest.loc[idx[0], "Status"] = "Active"
            latest.loc[idx[0], "ExpiryDate"] = expiry_date
            latest.loc[idx[0], "PremiumCode"] = premium_code
            latest.loc[idx[0], "PosterCount"] = 0
            latest.loc[idx[0], "LastPostDate"] = ""
        else:
            new_row = pd.DataFrame([{
                "Phone": customer_phone,
                "PremiumCode": premium_code,
                "Status": "Active",
                "PosterCount": 0,
                "Premium": True,
                "ExpiryDate": expiry_date,
                "LastPostDate": ""
            }])
            latest = pd.concat([latest, new_row], ignore_index=True)
        write_sheet_direct(latest)
        st.session_state.is_premium = True
        st.session_state.poster_count = 0
        st.session_state.last_phone = ""  # force refresh
        st.success(f"🎉 Premium activated till {expiry_date}!")
        st.rerun()

    # ---- FORM ----



# ---- GENERATE ----
if submitted:
    if not customer_phone.strip():
        st.warning("⚠️ Please enter Customer Phone first.")
        st.stop()
    if not shop.strip() or not offer.strip() or not customer_address.strip():
        st.warning("⚠️ Please fill all fields.")
        st.stop()
    if st.session_state.poster_generated:
        st.warning("🚫 Already generated today. Come back tomorrow!")
        st.stop()

    # fresh check
    fresh_check = read_sheet_direct()
    if not fresh_check.empty and "Phone" in fresh_check.columns:
        fresh_check["Phone"] = fresh_check["Phone"].astype(str)
        fresh_user = fresh_check[fresh_check["Phone"] == str(customer_phone)]
        if not fresh_user.empty:
            total_posts = int(fresh_user.iloc[0]["PosterCount"]) if fresh_user.iloc[0]["PosterCount"] else 0
            last_post_date = str(fresh_user.iloc[0]["LastPostDate"]).strip()[:10] if "LastPostDate" in fresh_user.columns else ""
        else:
            total_posts = 0
            last_post_date = ""
    else:
        total_posts = 0
        last_post_date = ""

    if last_post_date == today:
        st.warning("🚫 You already generated a poster today. Come back tomorrow!")
        st.stop()

    if not st.session_state.is_premium:
        if st.session_state.poster_count >= FREE_LIMIT:
            st.warning("💎 Your 3 free posters are used. Please pay ₹299.")
            st.stop()
    else:
        if total_posts >= 30:
            st.warning("🚫 You have used all 30 posts. Please renew ₹299.")
            st.stop()


    



    st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Telugu&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)
    
    
    
    prompt = f"write a 25 word ad for {shop} shop. offer:{offer}. Festival:{festival}"
    response = groq_client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user","content":prompt}],
        max_tokens=200,
        temperature=1.0
    )
    result = response.choices[0].message.content.strip()
    result = result.strip('"').strip('"')
    if not result or len(result) < 15:
        raise ValueError("Too short")

    #except Exception:
     #   if language == "Telugu":
      #      result = f"{festival} స్పెషల్ ఆఫర్! {shop} వద్ద {offer} మాత్రమే. వెంటనే వచ్చి ఆఫర్ పొందండి!"
      #  else:
      #      result = f"{festival} special offer at {shop}! Get {offer} today. Visit now!"

    # ---------------- ICON URLS ----------------
    themes = {
        "Grocery shop": "#DFF6DD",
        "Tiffin center": "#FFF3CD",
        "Tea shop & Snacks": "#FFF4E0",
        "Clothing store": "#E8DAEF",
        "Mobile shop": "#D6EAF8",
        "Salon": "#FADBD8",
        "Medical store": "#D5F5E3",
        "Bakery": "#FCF3CF",
        "Fruit shop": "#F9E79F",
        "Bike repair": "#D6DBDF",
        "Tuition center": "#EBDEF0",
        "Real estate": "#D4E6F1"
    }

    shop_icons = {
        "Grocery shop":     "https://cdn-icons-png.flaticon.com/512/3724/3724788.png",
        "Tiffin center":    "https://cdn-icons-png.flaticon.com/512/857/857681.png",
        "Tea shop & Snacks":"https://cdn-icons-png.flaticon.com/512/590/590836.png",
        "Clothing store":   "https://cdn-icons-png.flaticon.com/512/892/892458.png",
        "Mobile shop":      "https://cdn-icons-png.flaticon.com/512/545/545245.png",
        "Salon":            "https://cdn-icons-png.flaticon.com/512/2553/2553627.png",
        "Medical store":    "https://cdn-icons-png.flaticon.com/512/2382/2382461.png",
        "Bakery":           "https://cdn-icons-png.flaticon.com/512/3082/3082053.png",
        "Fruit shop":       "https://cdn-icons-png.flaticon.com/512/415/415733.png",
        "Bike repair":      "https://cdn-icons-png.flaticon.com/512/2972/2972185.png",
        "Tuition center":   "https://cdn-icons-png.flaticon.com/512/2436/2436874.png",
        "Real estate":      "https://cdn-icons-png.flaticon.com/512/1040/1040993.png"
    }
    festival_icons = {
        "Special Offer": "https://cdn-icons-png.flaticon.com/512/1828/1828884.png",
        "Ugadi": "https://cdn-icons-png.flaticon.com/512/616/616490.png",
        "Diwali": "https://cdn-icons-png.flaticon.com/512/616/616494.png",
        "Sankranti": "https://cdn-icons-png.flaticon.com/512/2933/2933245.png"
    }
    festival_icon = festival_icons.get(festival, "https://cdn-icons-png.flaticon.com/512/1828/1828884.png")
    bg_color = themes.get(shop_type, "#FFF8E7")
    shop_icon = shop_icons.get(shop_type, "https://cdn-icons-png.flaticon.com/512/590/590836.png")

    # ---------------- LOGO ----------------
    logo_html = ""
    if logo:
        logo_bytes = logo.read()
        logo_base64 = base64.b64encode(logo_bytes).decode()
        logo_html = f"""
        <img src="data:image/png;base64,{logo_base64}"
            style="width:150px;height:150px;border-radius:80px;
            object-fit:cover;margin-bottom:20px;">
        """

    # ---------------- POSTER HTML ----------------
    poster_html = f"""
    <html>
    <head>
    <meta charset="UTF-8">
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Poppins:wght@400;600;700;800&family=Noto+Sans+Telugu:wght@400;700&display=swap" rel="stylesheet">
    <style>
    * {{ margin:0; padding:0; box-sizing:border-box; }}
    body {{ background:#e8e8e8; display:flex; justify-content:center; padding:40px; }}
    .poster {{
        width: 900px;
        background: linear-gradient(150deg, #fffdf7 0%, {bg_color} 50%, #ffffff 100%);
        border-radius: 36px;
        overflow: hidden;
        box-shadow: 0 40px 100px rgba(0,0,0,0.3);
        position: relative;
    }}
    .top-bar {{
        height: 16px;
        background: linear-gradient(90deg, #FF6B35 0%, #FFD93D 30%, #6BCB77 60%, #4D96FF 100%);
    }}
    .bg-circle1 {{
        position:absolute; width:400px; height:400px; border-radius:50%;
        background: radial-gradient(circle, {bg_color}88, transparent);
        top:-100px; right:-100px; z-index:0;
    }}
    .bg-circle2 {{
        position:absolute; width:250px; height:250px; border-radius:50%;
        background: radial-gradient(circle, {bg_color}66, transparent);
        bottom:150px; left:-80px; z-index:0;
    }}
    .content {{ padding: 55px 65px; position:relative; z-index:2; }}

    .header {{
        display:flex; align-items:center; gap:30px; margin-bottom:40px;
        border-bottom: 2px solid {bg_color}; padding-bottom: 30px;
    }}
    .logo-wrap {{
        width:130px; height:130px; border-radius:22px;
        overflow:hidden; border:5px solid white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        flex-shrink:0; background:white;
        display:flex; align-items:center; justify-content:center;
    }}
    .logo-wrap img {{ width:100%; height:100%; object-fit:cover; }}
    .shop-name {{
        font-family:'Playfair Display', serif;
        font-size:72px; font-weight:900;
        color:#1a1a2e; line-height:1.0;
        letter-spacing:-1px;
    }}
    .shop-tag {{
        display:inline-block;
        background:#1a1a2e; color:white;
        font-size:17px; font-weight:700;
        padding:7px 20px; border-radius:50px;
        margin-top:12px; letter-spacing:2px;
        text-transform:uppercase;
    }}

    .festival-row {{
        display:flex; align-items:center; gap:14px;
        margin-bottom:28px;
    }}
    .festival-pill {{
        display:inline-flex; align-items:center; gap:10px;
        background:white; border:3px solid #FFD93D;
        border-radius:50px; padding:12px 30px;
        box-shadow: 0 4px 20px rgba(255,217,61,0.25);
    }}
    .festival-pill img {{ width:24px; height:24px; }}
    .festival-pill span {{
        font-size:24px; font-weight:800; color:#1a1a2e;
    }}

    .offer-box {{
        background: linear-gradient(135deg, #FF6B35 0%, #e8203e 100%);
        border-radius:28px; padding:35px 45px;
        margin:28px 0;
        box-shadow: 0 16px 45px rgba(255,60,60,0.4);
        display:flex; align-items:center; gap:28px;
        position:relative; overflow:hidden;
    }}
    .offer-box::before {{
        content:'';
        position:absolute; top:-30px; right:-30px;
        width:180px; height:180px; border-radius:50%;
        background:rgba(255,255,255,0.1);
    }}
    .offer-box::after {{
        content:'';
        position:absolute; bottom:-40px; right:80px;
        width:120px; height:120px; border-radius:50%;
        background:rgba(255,255,255,0.08);
    }}
    .offer-left {{ flex:1; }}
    .offer-label {{
        font-size:15px; font-weight:800;
        color:rgba(255,255,255,0.75);
        letter-spacing:3px; text-transform:uppercase;
        margin-bottom:8px;
    }}
    .offer-value {{
        font-family:'Playfair Display', serif;
        font-size:64px; font-weight:900;
        color:white; line-height:1.0;
        text-shadow: 3px 5px 15px rgba(0,0,0,0.25);
    }}
    .offer-shop-icon {{
        width:90px; height:90px;
        opacity:0.25; filter:brightness(10);
        position:relative; z-index:1;
    }}

    .caption-box {{
        background:rgba(255,255,255,0.8);
        backdrop-filter:blur(8px);
        border-left:7px solid #4D96FF;
        border-radius:0 20px 20px 0;
        padding:28px 35px;
        margin:28px 0;
        box-shadow: 0 4px 20px rgba(77,150,255,0.1);
    }}
    .caption-text {{
        font-size:30px; line-height:1.75;
        color:#2d2d2d; font-weight:500;
        font-family:'Noto Sans Telugu','Poppins',sans-serif;
    }}

    .divider {{
        height:2px;
        background:linear-gradient(90deg, transparent, #ddd 30%, #ddd 70%, transparent);
        margin:32px 0;
    }}

    .contact-row {{
        display:flex; flex-direction:column; gap:16px;
    }}
    .contact-item {{
        display:flex; align-items:center; gap:18px;
    }}
    .contact-icon-box {{
        width:50px; height:50px; border-radius:14px;
        background:#1a1a2e; display:flex;
        align-items:center; justify-content:center;
        flex-shrink:0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }}
    .contact-icon-box img {{ width:26px; height:26px; filter:invert(1); }}
    .contact-text {{
        font-size:28px; font-weight:700;
        color:#1a1a2e; font-family:'Poppins',sans-serif;
    }}

    .watermark {{
        position:absolute; bottom:50px; right:55px;
        width:140px; height:140px;
        opacity:0.08; z-index:1;
    }}
    .bottom-bar {{
        height:14px;
        background:linear-gradient(90deg, #4D96FF 0%, #6BCB77 30%, #FFD93D 60%, #FF6B35 100%);
        margin-top:45px;
    }}
    </style>
    </head>
    <body>
    <div class="poster">
    <div class="top-bar"></div>
    <div class="bg-circle1"></div>
    <div class="bg-circle2"></div>

    <div class="content">

        <div class="header">
        <div class="logo-wrap">
            {"<img src='data:image/png;base64," + logo_base64 + "'>" if logo else f'<img src="{shop_icon}" style="width:80px;height:80px;object-fit:contain;">'}
        </div>
        <div>
            <div class="shop-name">{shop}</div>
            <div class="shop-tag">{shop_type}</div>
        </div>
        </div>

        <div class="festival-row">
        <div class="festival-pill">
            
            <img src="{festival_icon}">
            <span>{festival} Special</span>
            
        </div>
        </div>

        <div class="offer-box">
        <div class="offer-left">
            <div class="offer-label">Exclusive Offer</div>
            <div class="offer-value">{offer}</div>
        </div>
        <img class="offer-shop-icon" src="{shop_icon}">
        </div>

        <div class="caption-box">
        <div class="caption-text">{result}</div>
        </div>

        <div class="divider"></div>

        <div class="contact-row">
        <div class="contact-item">
            <div class="contact-icon-box">
            <img src="https://cdn-icons-png.flaticon.com/512/597/597177.png">
            </div>
            <div class="contact-text">{customer_phone}</div>
        </div>
        <div class="contact-item">
            <div class="contact-icon-box">
            <img src="https://cdn-icons-png.flaticon.com/512/684/684908.png">
            </div>
            <div class="contact-text">{customer_address}</div>
        </div>
        </div>

    </div>

    <img class="watermark" src="{shop_icon}">
    <div class="bottom-bar"></div>
    </div>
    </body>
    </html>
    """

    # ---------------- HTML TO PNG ----------------
    async def render_html_to_png(html):
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page(viewport={"width": 900, "height": 1400})
            await page.set_content(html)
            await page.wait_for_timeout(2000)

            file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
            await page.screenshot(path=file.name, full_page=True)

            await browser.close()
            return file.name

    png_file = asyncio.run(render_html_to_png(poster_html))

    st.image(png_file, use_container_width=True)

    with open(png_file, "rb") as f:
        st.download_button(
            "Download Poster",
            f.read(),
            file_name="poster.png",
            mime="image/png"
        )

    # ---------------- WHATSAPP SHARE ----------------
    share_text = urllib.parse.quote(
        f"{shop}\n{offer}\n{result}\nPhone: {customer_phone}"
    )
    whatsapp_url = f"https://api.whatsapp.com/send?text={share_text}"
    APP_URL = "https://tea-poster-website.streamlit.app"
    st.markdown(f"""
    <a href="{whatsapp_url} {APP_URL}" target="_blank">
        <button style="
            background:#25D366;
            color:white;
            padding:15px 30px;
            border:none;
            border-radius:10px;
            font-size:20px;
            cursor:pointer;">
            Share to WhatsApp
        </button>
    </a>
    """, unsafe_allow_html=True)

    # ---------------- SAVE POSTER COUNT (free users only tracked in session) ----------------
    st.session_state.poster_count += 1
    st.session_state.poster_generated = True

    # Save to sheet for ALL users after poster generated
    latest_sheet = read_sheet_direct()
    if not latest_sheet.empty and "Phone" in latest_sheet.columns:
        latest_sheet["Phone"] = latest_sheet["Phone"].astype(str)
        idx = latest_sheet[latest_sheet["Phone"] == str(customer_phone)].index

        if len(idx) > 0:
            latest_sheet.loc[idx[0], "PosterCount"] = total_posts + 1
            latest_sheet.loc[idx[0], "LastPostDate"] = today
            write_sheet_direct(latest_sheet)
        else:
            # New user — add row
            new_row = pd.DataFrame([{
                "Phone": customer_phone,
                "PremiumCode": "",
                "Status": "Free",
                "PosterCount": 1,
                "Premium": False,
                "ExpiryDate": "",
                "LastPostDate": today
            }])
            latest_sheet = pd.concat([latest_sheet, new_row], ignore_index=True)
            write_sheet_direct(latest_sheet)
    else:        
        new_sheet = pd.DataFrame([{
            "Phone": customer_phone,
            "PremiumCode": "",
            "Status": "Free",
            "PosterCount": 1,
            "Premium": False,
            "ExpiryDate": "",
            "LastPostDate": today
        }])
        write_sheet_direct(new_sheet)    
    
    # Save count to sheet only if user exists (paid users)
    
    st.success("✅ Poster generated successfully!")
