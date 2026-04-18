import streamlit as st
import base64
from designs import get_poster_html
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from google import genai
import urllib.parse
import asyncio
from playwright.async_api import async_playwright
import tempfile

import os
import subprocess
import qrcode
from io import BytesIO
from datetime import datetime, timedelta
import gspread
from google.oauth2.service_account import Credentials
import time

import random



#def read_sheet_direct():
#    g = st.secrets["connections"]["gsheets"]
#    creds_dict = {
#        "type" : "service_account",
#        "project_id" : g["project_id"],
#        "private_key_id" : g["private_key_id"],
#        "private_key" : g["private_key"].replace("\\n","\\n"),
#        "client_email" : g["client_email"],
#        "client_id" : g["client_id"],
#        "auth_uri" : "https://accounts.google.com/o/oauth2/auth",
#        "token_uri" : "https://oauth2.googleapis.com/token",
#        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
#        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/{gs['client_email']}",
#        }
            
    
#    scopes = [
#        "https://www.googleapis.com/auth/spreadsheets",
#        "https://www.googleapis.com/auth/drive"
#        ]
#    creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
#    gc = gspread.authorize(creds)

#    for attempt in range(3):
#        try:
            
#            sh = gc.open_by_url(str(g["spreadsheet"]))
#            records = sh.sheet1.get_all_records()  # always returns list of dicts
#            return pd.DataFrame(records)
#        except Exception as e:
#            if attempt < 2:
#                time.sleep(2)
#                continue
#            else:
#                raise e    
#def write_sheet_direct(df):
#    g = st.secrets["connections"]["gsheets"]
#    creds_dict = {
#        "type": "service_account",
#        "project_id": g["project_id"],
#        "private_key_id": g["private_key_id"],
#        "private_key": g["private_key"].replace("\\n", "\n"),
#        "client_email": g["client_email"],
#        "client_id": g["client_id"],
#        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#        "token_uri": "https://oauth2.googleapis.com/token",
#        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
#        "client_x509_cert_url": f"https://www.googleapis.com/robot/v1/metadata/x509/{g['client_email']}"
#    }
#    scopes = [
#        "https://www.googleapis.com/auth/spreadsheets",
#        "https://www.googleapis.com/auth/drive"
#    ]
#    creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
#    gc = gspread.authorize(creds)
#    for attempt in range(3):
#        try:
#            sh = gc.open_by_url(str(g["spreadsheet"]))
#            worksheet = sh.sheet1
#            worksheet.clear()
#            worksheet.update(
#                [df.columns.tolist()] + df.fillna("").astype(str).values.tolist()
#            )
#            return  # success
#        except Exception as e:
#            if attempt < 2:
#                time.sleep(2)
#                continue
#            else:
#                raise e
    
    

if not os.path.exists("/home/adminuser/.cache/ms-playwright"):
    subprocess.run(["playwright","install","chromium"])

# ---------------- CONFIG ----------------
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

st.set_page_config(page_title="AI Poster Generator", layout="centered")
st.title("🎨 AI Poster Generator")

# ---------------- PREMIUM PAYMENT ----------------
#PAYMENT_LINK = "https://rzp.io"   # your real UPI
#PLAN_PRICE = 299

#today = datetime.now().strftime("%Y-%m-%d")

if "poster_generated" not in st.session_state:
    st.session_state.poster_generated = False


st.markdown("---")
with st.form("poster_form", clear_on_submit=False):
    customer_phone = st.text_input("📞 Customer Phone")
    shop = st.text_input("🏪 Shop Name")
    offer = st.text_input("🔥 Offer")
    logo = st.file_uploader("📷 Upload Shop Logo", type=["png","jpg","jpeg"],key="logo_upload")
    shop_type = st.selectbox("Select Shop Type", [
        "Grocery shop","Tiffin center","Tea shop & Snacks","Clothing store",
        "Mobile shop","Salon","Medical store","Bakery","Fruit shop",
        "Bike repair","Tuition center","Real estate"
    ])
    customer_address = st.text_input("📍 Customer Address")
    language = st.selectbox("Language", ["English", "Telugu"])
    festival = st.selectbox("Festival", ["Special Offer","Ugadi","Diwali","Sankranti"])
    submitted = st.form_submit_button("🚀 Generate AI Poster")


#sheet_data = pd.DataFrame()
#user_row = pd.DataFrame()

#if "last_phone" not in st.session_state:
#    st.session_state.last_phone = ""

#if customer_phone.strip() and customer_phone != st.session_state.last_phone:
   
#    try:
#        sheet_data = read_sheet_direct()
#        st.session_state.sheet_data = sheet_data
#        st.session_state.last_phone = customer_phone
#    except Exception as e:
#        st.error(f"Google sheet error: {e}")
#        st.stop()

#if "sheet_data" in st.session_state:
#    sheet_data = st.session_state.sheet_data
#    if isinstance(sheet_data, pd.DataFrame) and not sheet_data.empty and "Phone" in sheet_data.columns:
#        sheet_data["Phone"] = sheet_data["Phone"].astype(str)
#        user_row = sheet_data[sheet_data["Phone"] == str(customer_phone)]

# ---- USER STATUS ----
#if not user_row.empty:
#    st.session_state.poster_count = int(user_row.iloc[0]["PosterCount"]) if user_row.iloc[0]["PosterCount"] else 0
#    st.session_state.is_premium = str(user_row.iloc[0]["Premium"]).upper() == "TRUE"
#    expiry_col = str(user_row.iloc[0]["ExpiryDate"]) if "ExpiryDate" in user_row.columns else ""
#    if st.session_state.is_premium and expiry_col:
#        try:
#            expiry = datetime.strptime(expiry_col.strip(), "%Y-%m-%d")
#            if datetime.now() > expiry:
#                st.session_state.is_premium = False
#                st.warning("⚠️ Premium expired. Please renew ₹299.")
#            else:
#                days_left = (expiry - datetime.now()).days
#                st.success(f"💎 Premium active | {days_left} days left")
#        except:
#            pass
#else:
#    if "poster_count" not in st.session_state:
#        st.session_state.poster_count = 0
#    if "is_premium" not in st.session_state:
#        st.session_state.is_premium = False

# ---- STATUS DISPLAY ----
#FREE_LIMIT = 30
#remaining = FREE_LIMIT - st.session_state.poster_count

#if st.session_state.is_premium:
    #st.success("💎 Premium active: posters")
#elif remaining > 0:
    #st.info(f"🎁 Posters left: {remaining}")
    #st.markdown(f"Want unlimited? [💎 Upgrade to Premium ₹{PLAN_PRICE}]({PAYMENT_LINK})")
#else:
    #st.error("🚫 Posters used up!")
    #st.markdown(f"""
   # <a href="{PAYMENT_LINK}" target="_blank">
       # <button style="background:#25D366;color:white;padding:14px 28px;
       # border:none;border-radius:10px;font-size:18px;width:100%;cursor:pointer;">
       # 💎 Pay ₹{PLAN_PRICE} — Get 30 Posters / Month
       # </button>
   # </a>
    #""", unsafe_allow_html=True)

# ---- PAYMENT ----
#if st.button("✅ I Have Paid"):
    #if not customer_phone.strip():
   #     st.error("Please enter phone number first.")
    #else:
    #    expiry_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
    #    premium_code = f"RAMA{customer_phone[-4:]}"
    #    latest = read_sheet_direct()
    #    latest["Phone"] = latest["Phone"].astype(str) if "Phone" in latest.columns else latest["Phone"]
    #    idx = latest[latest["Phone"] == str(customer_phone)].index if "Phone" in latest.columns else []
    #    if len(idx) > 0:
    #        latest.loc[idx[0], "Premium"] = True
    #        latest.loc[idx[0], "Status"] = "Active"
    #        latest.loc[idx[0], "ExpiryDate"] = expiry_date
    #        latest.loc[idx[0], "PremiumCode"] = premium_code
    #        latest.loc[idx[0], "PosterCount"] = 0
    #        latest.loc[idx[0], "LastPostDate"] = ""
    #    else:
     #       new_row = pd.DataFrame([{
    #            "Phone": customer_phone,
    #            "PremiumCode": premium_code,
    #            "Status": "Active",
    #            "PosterCount": 0,
    #            "Premium": True,
    #            "ExpiryDate": expiry_date,
    #            "LastPostDate": ""
    #        }])
    #        latest = pd.concat([latest, new_row], ignore_index=True)
    #    write_sheet_direct(latest)
    #    st.session_state.is_premium = True
    #    st.session_state.poster_count = 0
    #    st.session_state.last_phone = ""  # force refresh
    #    st.success(f"🎉 Premium activated till {expiry_date}!")
    #    st.rerun()

    # ---- FORM ----



# ---- GENERATE ----
if submitted:
    if logo is not None:
        try:
            logo.seek(0)
            logo_bytes = logo.read()
            if logo_bytes:
                logo_base64 = base64.b64encode(logo_bytes).decode("utf-8")
        except Exception as e:
            st.warning(f"logo error: {e}")
            logo_base64 = None
    logo_base64 = st.session_state.get("logo_base64"),None

    if not customer_phone.strip():
        st.warning("⚠️ Please enter Customer Phone first.")
        st.stop()
    if not shop.strip() or not offer.strip() or not customer_address.strip():
        st.warning("⚠️ Please fill all fields.")
        st.stop()
    #if st.session_state.poster_generated:
        #st.warning("🚫 Already generated today. Come back tomorrow!")
        #st.stop()

    # fresh check
    #fresh_check = read_sheet_direct()
    #if not fresh_check.empty and "Phone" in fresh_check.columns:
        #fresh_check["Phone"] = fresh_check["Phone"].astype(str)
        #fresh_user = fresh_check[fresh_check["Phone"] == str(customer_phone)]
        #if not fresh_user.empty:
            #total_posts = int(fresh_user.iloc[0]["PosterCount"]) if fresh_user.iloc[0]["PosterCount"] else 0
    #        last_post_date = str(fresh_user.iloc[0]["LastPostDate"]).strip()[:10] if "LastPostDate" in fresh_user.columns else ""
     #   else:
     #       total_posts = 0
    #        last_post_date = ""
    #else:
    #    total_posts = 0
    #    last_post_date = ""

   # if last_post_date == today:
        #st.warning("🚫 You already generated a poster today. Come back tomorrow!")
        #st.stop()

    #if not st.session_state.is_premium:
        #if st.session_state.poster_count >= FREE_LIMIT:
            #st.warning("💎 Your 3 free posters are used. Please pay ₹299.")
           # st.stop()
    #else:
       # if total_posts >= 30:
            #st.warning("🚫 You have used all 30 posts. Please renew ₹299.")
            #st.stop()


    



    st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Telugu&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)
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
        contents=prompt
        )

        result = response.text.strip().split("\n")[0]

        
    except Exception:
        
        if language == "Telugu":
            fallbacks = [
                f"{festival} స్పెషల్ ఆఫర్! {shop} వద్ద {offer} మాత్రమే. వెంటనే వచ్చి ఆఫర్ పొందండి!",
                f"🌟 {shop} లో {festival} స్పెషల్! {offer} మాత్రమే. వెంటనే రండి, అవకాశం మిస్ చేసుకోకండి!",
                f"💥 {shop} వద్ద అద్భుతమైన డీల్! {offer} — ఈరోజే వినియోగించుకోండి!",
                f"🎉 {festival} సందర్భంగా {shop} లో {offer} ఆఫర్! మీ కుటుంబంతో రండి!",
                f"⭐ {shop} లో నాణ్యమైన సేవలు! {festival} స్పెషల్ — {offer}. ఆలస్యం చేయకండి!",
                f"🔥 {shop} వద్ద {festival} కి ప్రత్యేక ఆఫర్! {offer} మాత్రమే. వెంటనే వినియోగించుకోండి!",
                f"✨ {festival} శుభాకాంక్షలు! {shop} లో {offer} స్పెషల్ ఆఫర్ పొందండి!",
                f"🎊 {shop} లో {festival} సందర్భంగా గొప్ప ఆఫర్! {offer} — తొందరగా రండి!",
                f"💫 {shop} వద్ద {offer} ఆఫర్! {festival} కి ప్రత్యేక తగ్గింపు. ఈరోజే రండి!",
                f"🌈 {festival} సంతోషం మీకు అందించడానికి {shop} సిద్ధంగా ఉంది! {offer} పొందండి!",
                f"🏆 {shop} — మీ నమ్మకమైన అంగడి! {festival} స్పెషల్ {offer}. అందరికీ స్వాగతం!",
                f"🎯 {shop} లో {offer} — {festival} కి అద్భుతమైన బహుమతి! నేడే వినియోగించుకోండి!",
                f"💎 {festival} కి {shop} నుండి ప్రత్యేక ఆఫర్! {offer} మాత్రమే. మిస్ చేసుకోకండి!",
                f"🚀 {shop} వద్ద {festival} సూపర్ సేల్! {offer} — అందరికీ అద్భుతమైన అవకాశం!",
                f"🌺 {festival} శుభాకాంక్షలతో {shop} అందిస్తున్న స్పెషల్ ఆఫర్ — {offer}!",
                f"👑 {shop} లో {festival} కి రాజసమైన ఆఫర్! {offer} మాత్రమే. వెంటనే రండి!"
            ]
        else:
            fallbacks = [
                f"{festival} special offer at {shop}! Get {offer} today. Visit now!",
                f"🌟 {festival} Special at {shop}! Get {offer} today only. Don't miss this amazing deal!",
                f"💥 Exclusive {festival} offer at {shop}! {offer} — limited time only. Visit us now!",
                f"🎉 Celebrate {festival} with {shop}! Special deal: {offer}. Come with your family!",
                f"⭐ {shop} brings you the best {festival} offer! {offer} — quality you can trust!",
                f"🔥 Hot {festival} deal at {shop}! {offer} available today. Grab yours before it's gone!",
                f"✨ {shop} wishes you Happy {festival}! Celebrate with our special offer: {offer}!",
                f"🎊 Big {festival} sale at {shop}! {offer} — best prices in town. Visit us today!",
                f"💫 {shop} presents {festival} special: {offer}! Hurry, limited time offer!",
                f"🌈 Make your {festival} special with {shop}! Amazing offer: {offer}. Come visit us!",
                f"🏆 {shop} — your trusted store! {festival} special offer: {offer}. Everyone welcome!",
                f"🎯 {festival} deal you can't miss at {shop}! {offer} — visit us today and save big!",
                f"💎 Premium {festival} offer from {shop}! {offer} only. Don't let this pass you by!",
                f"🚀 Super {festival} sale at {shop}! {offer} — incredible savings for everyone!",
                f"🌺 {shop} celebrates {festival} with you! Special offer: {offer}. Come join us!",
                f"👑 Royal {festival} deal at {shop}! {offer} — best offer of the season. Visit now!"
            ] 
        result = random.choice(fallbacks)       

    
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
    
    logo_base64 = None
    if logo is not None:
        try:
            logo.seek(0)
            logo_bytes = logo.read()
            if logo_bytes:
                logo_base64 = base64.b64encode(logo_bytes).decode("utf-8")
        except Exception as e:
            st.warning(f"logo error: {e}")
            logo_base64 = None

    # ---------------- POSTER HTML ----------------
   
    # Inside your generate button block:
    design = random.randint(1, 4)

    poster_html = get_poster_html(
        design=design,
        shop=shop,
        offer=offer,
        festival=festival,
        result=result,
        customer_phone=customer_phone,
        customer_address=customer_address,
        shop_type=shop_type,
        shop_icon=shop_icon,
        festival_icon=festival_icon,
        bg_color=bg_color,
        logo=logo,
        logo_base64=logo_base64
    )
    

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
        downloaded = st.download_button(
            "Download Poster",
            f.read(),
            file_name="poster.png",
            mime="image/png"
        )

    if downloaded:
        st.session_state.download_count +=1

    st.info(f" Total number of downloads: {st.session_state.download_count}")         

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
    # ---- SAVE AFTER POSTER GENERATED ----
    st.session_state.poster_count += 1
    st.session_state.poster_generated = True

    st.success("☑️ Poster generated successfully!")
    