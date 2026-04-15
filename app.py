import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from google import genai
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
    spreadsheet_url = str(st.secrets["connections"]["gsheets"]["spreadsheet"])
    sh = gc.open_by_url(spreadsheet_url)
    worksheet = sh.sheet1
    records = worksheet.get_all_records()  # always returns list of dicts
    return pd.DataFrame(records)

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
    sh = gc.open_by_url(str(g["spreadsheet"]))
    worksheet = sh.sheet1
    worksheet.clear()
    worksheet.update(
        [df.columns.tolist()] + df.fillna("").astype(str).values.tolist()
    )

   

if not os.path.exists("/home/adminuser/.cache/ms-playwright"):
    subprocess.run(["playwright","install","chromium"])

# ---------------- CONFIG ----------------
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

st.set_page_config(page_title="AI Poster Generator", layout="centered")
st.title("🎨 AI Poster Generator")

# ---------------- PREMIUM PAYMENT ----------------
pay_link = "https://rzp.io"   # your real UPI
plan_price = 299

today = datetime.now().strftime("%Y-%m-%d")

if "poster_generated" not in st.session_state:
    st.session_state.poster_generated = False

customer_phone = st.text_input("📞 Customer Phone")

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
        import traceback
        st.error(f"Google sheet error: {e}")
        st.code(traceback.format_exc())
        st.stop()

# restore cache
if "sheet_data" in st.session_state:
    cached = st.session_state.sheet_data

    if isinstance(cached, pd.DataFrame):
        sheet_data = cached.copy()
    else:
        sheet_data = pd.DataFrame()

# safe filter
if not sheet_data.empty and "Phone" in sheet_data.columns:
    sheet_data["Phone"] = sheet_data["Phone"].astype(str)

    user_row = sheet_data[
        sheet_data["Phone"] == str(customer_phone)
    ] 




if not user_row.empty:
    st.session_state.poster_count = int(user_row.iloc[0]["PosterCount"])
    st.session_state.is_premium = user_row.iloc[0]["Premium"] == "TRUE" or user_row.iloc[0]["Premium"] == True

    expiry_col = user_row.iloc[0]["ExpiryDate"] if "ExpiryDate" in user_row.columns else ""
    if st.session_state.is_premium and expiry_col:
        try:
            expiry = datetime.strptime(str(expiry_col), "%Y-%m-%d")
            if datetime.now() > expiry:
                st.session_state.is_premium = False
                st.warning("⚠️ Premium expired. Please renew ₹299.")
            else:
                days_left = (expiry - datetime.now()).days
                st.success(f"💎 Premium active | {days_left} days left")
        except:
            pass
else:
    st.session_state.poster_count = 0
    st.session_state.is_premium = False

# ---------------- SHOW STATUS ----------------
FREE_LIMIT = 3
if "poster_count" not in st.session_state:
    st.session_state.poster_count = 0
if "is_premium" not in st.session_state:
    st.session_state.is_premium = False

remaining = FREE_LIMIT - st.session_state.poster_count

if st.session_state.is_premium:
    st.success("💎 Premium active: Unlimited posters")
elif remaining > 0:
    st.info(f"🎁 Free posters left: {remaining}")
else:
    st.warning("🚫 Free posters used up. Please pay ₹299 for premium.")

# ---------------- PAYMENT BUTTON ----------------
if customer_phone:
    st.markdown(f"""
    <a href="{pay_link}" target="_blank">
        <button style="background:#25D366;color:white;padding:14px 28px;
        border:none;border-radius:10px;font-size:18px;">
        💎 Pay ₹{plan_price} with GPay / PhonePe / Paytm
        </button>
    </a>
    """, unsafe_allow_html=True)

if st.button("✅ I Have Paid"):
    if not customer_phone.strip():
        st.error("Please enter your phone number first.")
    else:
        expiry_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        premium_code = f"RAMA{customer_phone[-4:]}"

        if not user_row.empty:
            # existing user — update their row
            row_index = user_row.index[0]
            sheet_data.loc[row_index, "Premium"] = True
            sheet_data.loc[row_index, "Status"] = "Active"
            sheet_data.loc[row_index, "ExpiryDate"] = expiry_date
            sheet_data.loc[row_index, "PremiumCode"] = premium_code
            sheet_data.loc[row_index, "PosterCount"] = 0
            sheet_data.loc[row_index, "LastPostDate"] = ""
        else:
            # new user — add to sheet
            new_row = pd.DataFrame([{
                "Phone": customer_phone,
                "PremiumCode": premium_code,
                "Status": "Active",
                "PosterCount": 0,
                "Premium": True,
                "ExpiryDate": expiry_date,
                "LastPostDate": ""
            }])
            sheet_data = pd.concat([sheet_data, new_row], ignore_index=True)

        conn.update(data=sheet_data)
        st.session_state.is_premium = True
        st.session_state.poster_count = 0
        st.success(f"🎉 Premium activated till {expiry_date}! You can now generate unlimited posters.")
        st.rerun()
# ---------------- INPUTS ----------------
shop = st.text_input("🏪 Shop Name")
offer = st.text_input("🔥 Offer")
logo = st.file_uploader("📷 Upload Shop Logo", type=["png", "jpg", "jpeg"])
# Reset flag if user changes shop or offer
if "last_shop" not in st.session_state:
    st.session_state.last_shop = ""
if shop != st.session_state.last_shop:
    st.session_state.poster_generated = False
    st.session_state.last_shop = shop




shop_type = st.selectbox(
    "Select Shop Type",
    [
        "Grocery shop",
        "Tiffin center",
        "Tea shop & Snacks",
        "Clothing store",
        "Mobile shop",
        "Salon",
        "Medical store",
        "Bakery",
        "Fruit shop",
        "Bike repair",
        "Tuition center",
        "Real estate"
    ]
)

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



customer_address = st.text_input("📍 Customer Address")
language = st.selectbox("Language", ["English", "Telugu"])
festival = st.selectbox(
    "Festival",
    ["Special Offer", "Ugadi", "Diwali", "Sankranti"]
)

# Telugu font
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Telugu&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# ---------------- BUTTON ----------------
if st.button("🚀 Generate AI Poster"):

    # ✅ Always fetch fresh data on button click
    fresh_check = read_sheet_direct()
    if fresh_check.empty or "Phone" not in fresh_check.columns:
        total_posts = 0
        last_post_date = ""
    else:
        fresh_check["Phone"] = fresh_check["Phone"].astype(str)
        fresh_user = fresh_check[fresh_check["Phone"] == str(customer_phone)]
        if not fresh_user.empty:
            total_posts = int(fresh_user.iloc[0]["PosterCount"]) if fresh_user.iloc[0]["PosterCount"] else 0
            last_post_date = str(fresh_user.iloc[0]["LastPostDate"]).strip()[:10] if "LastPostDate" in fresh_user.columns else ""
        else:
            total_posts = 0
            last_post_date = ""

    # ✅ Block if already posted today (works after refresh too)
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
                                
    if not shop or not offer:
        st.warning("Please enter shop name and offer") 
        st.stop()     

    bg_color = themes.get(shop_type, "#FFF8E7")
    shop_icon = shop_icons.get(shop_type, "https://cdn-icons-png.flaticon.com/512/590/590836.png")

    prompt = f"""
    You are a creative marketing expert for small businesses in India.
    Create a UNIQUE and catchy advertisement caption in {language} for this specific shop.

    Shop Name: {shop}
    Shop Type: {shop_type}
    Offer: {offer}
    Festival/Occasion: {festival}
    Location: {customer_address}

    Rules:
    - MUST be different and creative every time
    - Include the shop name {shop} naturally
    - Include the exact offer: {offer}
    - Mention {festival} if not "Special Offer"
    - Minimum 25 words, maximum 40 words
    - One paragraph only, no bullet points
    - If Telugu: mix Telugu and English naturally
    - Make it emotional and exciting for local customers
    - Use random seed: {random.randint(1, 99999)}
    Return ONLY the caption text, nothing else.
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config={
                "temperature": 1.0,
                "max_output_tokens": 200,
            }
        )
        result = response.text.strip().split("\n")[0]

        if not result or len(result) < 20:
            raise ValueError("Too short")

    except Exception:
        if language == "Telugu":
            result = f"{festival} స్పెషల్ ఆఫర్! {shop} వద్ద {offer} మాత్రమే. వెంటనే వచ్చి ఆఫర్ పొందండి!"
        else:
            result = f"{festival} special offer at {shop}! Get {offer} today. Visit now!"

    # ---------------- ICON URLS ----------------
    #tea_icon = "https://cdn-icons-png.flaticon.com/512/590/590836.png"
    fire_icon = "https://cdn-icons-png.flaticon.com/512/1828/1828884.png"
    phone_icon = "https://cdn-icons-png.flaticon.com/512/597/597177.png"
    location_icon = "https://cdn-icons-png.flaticon.com/512/684/684908.png"
    festival_icon = "https://cdn-icons-png.flaticon.com/512/616/616490.png"

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
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Poppins:wght@400;600;700&family=Noto+Sans+Telugu:wght@400;700&display=swap" rel="stylesheet">
    <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ background: #f0f0f0; display: flex; justify-content: center; padding: 30px; }}

    .poster {{
        width: 900px;
        min-height: 1100px;
        background: linear-gradient(160deg, {bg_color} 0%, #ffffff 60%, {bg_color}99 100%);
        border-radius: 32px;
        overflow: hidden;
        box-shadow: 0 30px 80px rgba(0,0,0,0.25);
        position: relative;
        font-family: 'Poppins', 'Noto Sans Telugu', sans-serif;
    }}

    /* decorative top bar */
    .top-bar {{
        height: 12px;
        background: linear-gradient(90deg, #FF6B35, #FFD93D, #6BCB77, #4D96FF);
    }}

    /* decorative circles */
    .circle1 {{
        position: absolute;
        width: 300px; height: 300px;
        border-radius: 50%;
        background: radial-gradient(circle, {bg_color}, transparent);
        top: -80px; right: -80px;
        opacity: 0.6;
    }}
    .circle2 {{
        position: absolute;
        width: 200px; height: 200px;
        border-radius: 50%;
        background: radial-gradient(circle, {bg_color}, transparent);
        bottom: 100px; left: -60px;
        opacity: 0.5;
    }}

    .content {{
        padding: 50px 60px;
        position: relative;
        z-index: 2;
    }}

    /* logo + shop name */
    .header {{
        display: flex;
        align-items: center;
        gap: 28px;
        margin-bottom: 36px;
    }}
    .logo-wrap {{
        width: 120px; height: 120px;
        border-radius: 24px;
        overflow: hidden;
        border: 4px solid white;
        box-shadow: 0 8px 24px rgba(0,0,0,0.15);
        flex-shrink: 0;
        background: white;
        display: flex; align-items: center; justify-content: center;
    }}
    .logo-wrap img {{ width: 100%; height: 100%; object-fit: cover; }}
    .shop-info {{ flex: 1; }}
    .shop-name {{
        font-family: 'Playfair Display', serif;
        font-size: 58px;
        font-weight: 900;
        color: #1a1a2e;
        line-height: 1.1;
        text-shadow: 2px 2px 0px rgba(0,0,0,0.08);
    }}
    .shop-type-tag {{
        display: inline-block;
        background: #1a1a2e;
        color: white;
        font-size: 16px;
        font-weight: 600;
        padding: 6px 18px;
        border-radius: 50px;
        margin-top: 10px;
        letter-spacing: 1px;
        text-transform: uppercase;
    }}

    /* offer badge */
    .offer-section {{
        background: linear-gradient(135deg, #FF6B35, #FF3D71);
        border-radius: 24px;
        padding: 30px 40px;
        margin: 30px 0;
        display: flex;
        align-items: center;
        gap: 24px;
        box-shadow: 0 12px 35px rgba(255,107,53,0.35);
    }}
    .offer-icon {{ font-size: 60px; flex-shrink: 0; }}
    .offer-text {{
        flex: 1;
    }}
    .offer-label {{
        font-size: 16px;
        font-weight: 700;
        color: rgba(255,255,255,0.8);
        text-transform: uppercase;
        letter-spacing: 2px;
    }}
    .offer-value {{
        font-family: 'Playfair Display', serif;
        font-size: 52px;
        font-weight: 900;
        color: white;
        line-height: 1.1;
        text-shadow: 2px 4px 12px rgba(0,0,0,0.2);
    }}

    /* festival badge */
    .festival-badge {{
        display: inline-flex;
        align-items: center;
        gap: 12px;
        background: white;
        border: 3px solid #FFD93D;
        border-radius: 50px;
        padding: 12px 28px;
        margin-bottom: 28px;
        box-shadow: 0 4px 16px rgba(255,217,61,0.3);
    }}
    .festival-badge span {{
        font-size: 22px;
        font-weight: 700;
        color: #1a1a2e;
    }}

    /* AI caption */
    .caption-box {{
        background: rgba(255,255,255,0.7);
        backdrop-filter: blur(10px);
        border-left: 6px solid #4D96FF;
        border-radius: 0 16px 16px 0;
        padding: 24px 30px;
        margin: 24px 0;
    }}
    .caption-text {{
        font-size: 28px;
        line-height: 1.7;
        color: #2d2d2d;
        font-family: 'Noto Sans Telugu', 'Poppins', sans-serif;
        font-weight: 500;
    }}

    /* divider */
    .divider {{
        height: 2px;
        background: linear-gradient(90deg, transparent, #ddd, transparent);
        margin: 30px 0;
    }}

    /* contact section */
    .contact-section {{
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
        gap: 20px;
    }}
    .contact-info {{ flex: 1; }}
    .contact-item {{
        display: flex;
        align-items: center;
        gap: 14px;
        margin-bottom: 16px;
    }}
    .contact-icon {{
        width: 44px; height: 44px;
        background: #1a1a2e;
        border-radius: 12px;
        display: flex; align-items: center; justify-content: center;
    }}
    .contact-icon img {{ width: 24px; height: 24px; filter: invert(1); }}
    .contact-text {{
        font-size: 26px;
        font-weight: 600;
        color: #1a1a2e;
    }}

    /* shop icon bottom right */
    .shop-icon-big {{
        width: 130px; height: 130px;
        opacity: 0.15;
        position: absolute;
        bottom: 40px; right: 50px;
    }}

    /* bottom bar */
    .bottom-bar {{
        height: 10px;
        background: linear-gradient(90deg, #4D96FF, #6BCB77, #FFD93D, #FF6B35);
        margin-top: 40px;
    }}
    </style>
    </head>
    <body>
    <div class="poster">
    <div class="top-bar"></div>
    <div class="circle1"></div>
    <div class="circle2"></div>

    <div class="content">

        <!-- HEADER -->
        <div class="header">
        <div class="logo-wrap">
            {"<img src='data:image/png;base64," + logo_base64 + "'>" if logo else f"<img src='{shop_icon}'>"}
        </div>
        <div class="shop-info">
            <div class="shop-name">{shop}</div>
            <div class="shop-type-tag">{shop_type}</div>
        </div>
        </div>

        <!-- FESTIVAL -->
        <div class="festival-badge">
        <img src="{festival_icon}" style="width:32px;height:32px;">
        <span>🎉 {festival} Special</span>
        </div>

        <!-- OFFER -->
        <div class="offer-section">
        <div class="offer-icon">🔥</div>
        <div class="offer-text">
            <div class="offer-label">Exclusive Offer</div>
            <div class="offer-value">{offer}</div>
        </div>
        <img src="{shop_icon}" style="width:80px;height:80px;opacity:0.3;filter:brightness(10);">
        </div>

        <!-- AI CAPTION -->
        <div class="caption-box">
        <div class="caption-text">{result}</div>
        </div>

        <div class="divider"></div>

        <!-- CONTACT -->
        <div class="contact-section">
        <div class="contact-info">
            <div class="contact-item">
            <div class="contact-icon">
                <img src="https://cdn-icons-png.flaticon.com/512/597/597177.png">
            </div>
            <div class="contact-text">{customer_phone}</div>
            </div>
            <div class="contact-item">
            <div class="contact-icon">
                <img src="https://cdn-icons-png.flaticon.com/512/684/684908.png">
            </div>
            <div class="contact-text">{customer_address}</div>
            </div>
        </div>
        </div>

    </div>

    <img class="shop-icon-big" src="{shop_icon}">
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
        # Sheet is empty — create first row
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
