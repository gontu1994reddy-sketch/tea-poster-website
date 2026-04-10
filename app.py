import streamlit as st
from google import genai
import urllib.parse
import asyncio
from playwright.async_api import async_playwright
import tempfile
import base64
import os

# ---------------- CONFIG ----------------
if not os.path.exists("/home/appuser/.cache/ms-playwright"):
   os.system("playwright install chromium")

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

st.set_page_config(page_title="AI Poster Generator", layout="centered")
st.title("🎨 AI Poster Generator")

# ---------------- INPUTS ----------------
shop = st.text_input("🏪 Shop Name")
offer = st.text_input("🔥 Offer")
logo = st.file_uploader("📷 Upload Shop Logo", type=["png", "jpg", "jpeg"])

shop_type = st.selectbox(
    "🏪 Select Shop Type",
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

customer_phone = st.text_input("📞 Customer Phone")
customer_address = st.text_input("📍 Customer Address")
language = st.selectbox("🌐 Language", ["English", "Telugu"])
festival = st.selectbox(
    "🎉 Festival",
    ["Special Offer", "Ugadi", "Diwali", "Sankranti"]
)

# Telugu font
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Telugu&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# ---------------- BUTTON ----------------
def image_to_base64(path):
    import base64
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

if st.button("🚀 Generate AI Poster"):

    bg_color = themes.get(shop_type, "#FFF8E7")

    # AI Caption Prompt
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
    # Logo handling
    logo_html = ""
    if logo:
        logo_bytes = logo.read()
        logo_base64 = base64.b64encode(logo_bytes).decode()
        logo_html = f"""
        <img src="data:image/png;base64,{logo_base64}"
             style="width:150px;height:150px;border-radius:80px;
             object-fit:cover;margin-bottom:20px;">
        """
<<<<<<< HEAD
    
    tea_icon = image_to_base64("icons/tea.png")
    fire_icon = image_to_base64("icons/fire.png")
    phone_icon = image_to_base64("icons/phone.png")
    location_icon = image_to_base64("icons/location.png")

=======
    tea_icon = "https://cdn-icons-png.flaticon.com/512/590/590836.png"
    fire_icon = "https://cdn-icons-png.flaticon.com/512/1828/1828884.png"
    phone_icon = "https://cdn-icons-png.flaticon.com/512/597/597177.png"
    location_icon = "https://cdn-icons-png.flaticon.com/512/684/684908"
>>>>>>> 72d60b8 (updated icon fix)
    # Poster HTML
    poster_html = f"""
    <html>
    <head>
    <meta charset="UTF-8">
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Telugu&display=swap" rel="stylesheet">
    </head>
    <body>
    <div style="
        width:80%;
        min_height:900px;
        margin:auto;
        background:linear-gradient(135deg, #FFF8E7, {bg_color});
        border-radius:25px;
        padding:50px;
        text-align:center;
        font-family:'Noto Sans Telugu', sans-serif;
        box-shadow:0 10px 25px rgba(0,0,0,0.2);
    ">

    {logo_html}

    <div style="
         display:flex;
         justify-content:center;
         align-items:center;
         gap:20px;
         margin-bottom:25px;
    ">
<<<<<<< HEAD
         <img src="data:image/png;base64,{tea_icon}" style="width:70px;height:70px;">
=======
         <img src="{tea_icon}" style="width:70px;height:70px;">
>>>>>>> 72d60b8 (updated icon fix)
         <h1 style="
             font-size:68px;
             color:#4E342E;
             margin:0;
             font-weight:800;
             letter-spacing:1px;
         ">
           {shop}
         </h1>
    </div>
    <div style="
        display:inline-block;
        background:red;
        color:white;
        padding:15px 35px;
        border-radius:50px;
        font-size:48px;
        font-weight:bold;
        margin:20px 0;
        box-shadow:0 4px 10px rgba(255,0,0,0.3);
    ">
        <img src="data:image/png;base64,{fire_icon}"
        style="width:40px;height:40px;">
        <span
<<<<<<< HEAD
        style="font-size:40px;font-weight:bold;>
         SPECIAL OFFER</span>
=======
        style="font-size:40px;font-weight:bold;">
        SPECIAL OFFER</span>
>>>>>>> 72d60b8 (updated icon fix)
    </div>
 
    
    <div style="
         background:white;
         border-radius:20px;
         padding:25px;
         margin:25px auto;
         width:85%;
         box-shadow:0 6px 20px rgba(0,0,0,0.15);
    ">
         <h2 style="
             font-size:58px;
             color:#D84315;
             margin:0;
             font-weight:bold;
         ">
           <img src="data:image/png;base64,{tea_icon}> {offer}
         </h2>
    </div>


   

    <h3 style="font-size:52px;color:#5D4037;"> {festival}</h3>

    <p style="font-size:38px;line-height:1.6;color:#3E2723;font_weight:500px;">
    {result}
    </p>

    <hr>

<<<<<<< HEAD
    <p style="font-size:45px;"><img src="data:image/png;base64,{phone_icon}">{customer_phone}</p>
    <p style="font-size:45px;"><img src="data:image/png;base64,{location_icon}">{customer_address}</p>
=======
    <p style="font-size:45px;"><img src="{phone_icon}"> {customer_phone}</p>
    <p style="font-size:45px;"><img src="{location_icon}"> {customer_address}</p>
>>>>>>> 72d60b8 (updated icon fix)

    </div>
    </body>
    </html>
    """

    # HTML to PNG
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

    # Preview image
    st.image(png_file,use_container_width=True)

    # Download button
    with open(png_file, "rb") as f:
        st.download_button(
            "⬇️ Download Poster",
            f.read(),
            file_name="poster.png",
            mime="image/png"
        )

    # WhatsApp Share
    share_text = urllib.parse.quote(
        f"{shop}\n{offer}\n{result}\n📞 {customer_phone}"
    )
    whatsapp_url = f"https://wa.me/?text={share_text}"

    st.markdown(f"""
    <a href="{whatsapp_url}" target="_blank">
        <button style="
            background:#25D366;
            color:white;
            padding:15px 30px;
            border:none;
            border-radius:10px;
            font-size:20px;
            cursor:pointer;">
            📲 Share to WhatsApp
        </button>
    </a>
    """, unsafe_allow_html=True)

    st.success("✅ Premium poster generated successfully!")
