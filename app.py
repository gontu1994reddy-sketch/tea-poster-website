import streamlit as st
from google import genai
import urllib.parse
import asyncio
from playwright.async_api import async_playwright
import tempfile
import base64
import os
import subprocess
import json
from pathlib import Path
import qrcode
from io import BytesIO




if not os.path.exists("/home/adminuser/.cache/ms-playwright"):
    subprocess.run(["playwright","install","chromium"])

# ---------------- CONFIG ----------------
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

st.set_page_config(page_title="AI Poster Generator", layout="centered")
st.title("🎨 AI Poster Generator")

# ---------------- PREMIUM PAYMENT ----------------
UPI_ID = "9866730504@ybl"   # your real UPI
PLAN_PRICE = 299

if "is_premium" not in st.session_state:
    st.session_state.is_premium = False

st.subheader("💎 Premium Plan")



pay_url = f"upi://pay?pa={UPI_ID}&pn=AI Poster App&am={PLAN_PRICE}&cu=INR"

qr = qrcode.make(pay_url)
buffer = BytesIO()
qr.save(buffer, format="PNG")
buffer.seek(0)

st.image(buffer, caption="📲 Scan QR to Pay ₹299", width=250)

if "poster_count" not in st.session_state:
    st.session_state.poster_count = 0

FREE_LIMIT = 3

remaining = FREE_LIMIT - st.session_state.poster_count

if not st.session_state.is_premium:
    st.info(f"🎁 Free posters left today: {remaining}")
else:
    st.success("💎 Premium active: Unlimited posters")

st.markdown(f"""
<a href="{pay_url}">
    <button style="
        background:#25D366;
        color:white;
        padding:14px 28px;
        border:none;
        border-radius:10px;
        font-size:18px;
        border-radius:10px;
        cursor:pointer;">
        💎 Pay ₹{PLAN_PRICE}
    </button>
</a>
""", unsafe_allow_html=True)

utr = st.text_input("💳 Enter UPI Transaction ID after payment")

if utr and customer_phone:
    with open(file_path, "r") as f:
        premium_users = json.load(f)

    
    premium_users[customer_phone]["premium"] = True
    premium_users[customer_phone]["utr"] = utr


    with open(file_path, "w") as f:
        json.dump(premium_users, f, indent=2)

    st.session_state.is_premium = True
    st.success("🎉 Premium activated successful")

# ---------------- INPUTS ----------------
shop = st.text_input("🏪 Shop Name")
offer = st.text_input("🔥 Offer")
logo = st.file_uploader("📷 Upload Shop Logo", type=["png", "jpg", "jpeg"])




shop_type = st.selectbox(
    "Select Shop Type",
    [
        "Grocery shop",
        "Tiffin center",
        "Tea shop & Snacks",
        "Clothing store",
        "Mobile shop"
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

customer_phone = st.text_input("📞 Customer Phone")

file_path = Path("premium_users.json")



if not file_path.exists():
    file_path.write_text("{}")


with open(file_path, "r") as f:
    premium_users = json.load(f)

if "poster_count" not in st.session_state:
    st.session_state.poster_count = 0

if "is_premium" not in st.session_state:
    st.session_state.is_premium = False

if customer_phone in premium_users:
    user_data = premium_users[customer_phone]

    st.session_state.poster_count = user_data.get("poster_count", 0)
    st.session_state.is_premium = user_data.get("premium", False)

    expiry_date = user_data.get("expiry_date")

    if expiry_date:
        expiry = datetime.strptime(expiry_date, "%Y-%m-%d")

        if datetime.now() > expiry:
            st.session_state.is_premium = False
            premium_users[customer_phone]["premium"] = False

            with open(file_path, "w") as f:
                json.dump(premium_users, f, indent=2)

            st.warning("⚠️ Premium expired. Renew ₹299 to continue.")

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
FREE_LIMIT = 3

if st.button("🚀 Generate AI Poster"):

    user_data = premium_users.get(customer_phone, {})
    free_used = user_data.get("free_used", False)

    # ✅ expired or old free users must renew
    if not st.session_state.is_premium:
        if free_used or st.session_state.poster_count >= FREE_LIMIT:
            st.warning("💎 Your free trial is over or premium expired. Please renew ₹299.")
            st.stop()

    bg_color = themes.get(shop_type, "#FFF8E7")

    prompt = f"""
    Create a short catchy {language} ad caption for {shop}.
    Shop name: {shop}
    Offer: {offer}
    Festival: {festival}

    Rules:
    - one paragraph only
    - minimum 20 words
    - attractive marketing style
    - use mix English and Telugu if Telugu selected
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        result = response.text.strip().split("\n")[0]

    except Exception:
        if language == "Telugu":
            result = f"{festival} స్పెషల్ ఆఫర్! {shop} వద్ద {offer} మాత్రమే. వెంటనే వచ్చి ఆఫర్ పొందండి!"
        else:
            result = f"{festival} special offer at {shop}! Get {offer} today. Visit now!"

    # ---------------- ICON URLS ----------------
    tea_icon = "https://cdn-icons-png.flaticon.com/512/590/590836.png"
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
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Telugu&display=swap" rel="stylesheet">
    </head>
    <body>
    <div style="
        width:80%;
        min-height:900px;
        margin:auto;
        background:linear-gradient(135deg, #FFF8E7, {bg_color});
        border-radius:25px;
        padding:50px;
        text-align:center;
        font-family:'Noto Sans Telugu', sans-serif;
        box-shadow:0 10px 25px rgba(0,0,0,0.2);
    ">

    {logo_html}

    <div style="display:flex;justify-content:center;align-items:center;gap:20px;margin-bottom:25px;">
         <img src="{tea_icon}" style="width:70px;height:70px;">
         <h1 style="font-size:68px;color:#4E342E;margin:0;font-weight:800;">
           {shop}
         </h1>
    </div>

    <div style="
        display:flex;
        justify-content:center;
        align-items:center;
        gap:15px;
        background:red;
        color:white;
        padding:15px 35px;
        border-radius:50px;
        width:fit-content;
        margin:20px auto;
        box-shadow:0 4px 10px rgba(255,0,0,0.3);
    ">
        <img src="{fire_icon}" style="width:40px;height:40px;">
        <span style="font-size:40px;font-weight:bold;">SPECIAL OFFER</span>
    </div>

    <div style="
         background:white;
         border-radius:20px;
         padding:25px;
         margin:25px auto;
         width:85%;
         box-shadow:0 6px 20px rgba(0,0,0,0.15);
    ">
         <h2 style="font-size:58px;color:#D84315;margin:0;font-weight:bold;">
         <img src="{tea_icon}" style="width:40px;height:40px;">
           {offer}
         </h2>
    </div>

    <div style="display:flex;justify-content:center;align-items:center;gap:10px;">
        <img src="{festival_icon}" style="width:45px;height:45px;">
        <h3 style="font-size:52px;color:#5D4037;">{festival}</h3>
    </div>

    <p style="font-size:38px;line-height:1.6;color:#3E2723;font-weight:500;">
    {result}
    </p>

    <hr>
    
    

    <div style="display:flex;justify-content:center;align-items:center;gap:10px">

        <img src="{phone_icon}" style="width:35px;height:35px;">
        <p style="font-size:45px;">{customer_phone}</p>
    </div>    
    <div style="display:flex;justify-content:center;align-items:center">
        <img src="{location_icon}" style="width:35px;height:35px;">
        <p style="font-size:45px;">{customer_address}</p>
       
    </div>
     
     

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
    with open(file_path, "r") as f:
        premium_users = json.load(f)

    premium_users.setdefault(customer_phone,{
        "premium": False,
        "utr": "",
        "poster_count": 0,
        "free_used": False
    })    

    st.session_state.poster_count += 1
    premium_users[customer_phone]["poster_count"] = st.session_state.poster_count

    if st.session_state.poster_count >= 3:
        premium_users[customer_phone]["free_used"] = True

    with open(file_path, "w") as f:
        json.dump(premium_users, f, indent=2)
    
    st.success("Premium poster generated successfully!")
