def get_poster_html(design, shop, offer, festival, result,
                    customer_phone, customer_address, shop_type,
                    shop_icon, festival_icon, bg_color,
                    logo=None, logo_base64=None):

    logo_html = (
        f"<img src='data:image/png;base64,{logo_base64}' style='width:100%;height:100%;object-fit:cover;'>"
        if logo and logo_base64
        else f"<img src='{shop_icon}' style='width:70px;height:70px;object-fit:contain;'>"
    )

    if design == 1:
        # ---- DESIGN 1: BOLD DARK BLACK & GOLD ----
        return f"""
        <html><head><meta charset="UTF-8">
        <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@700;900&family=Raleway:wght@400;600;800&family=Noto+Sans+Telugu:wght@400;700&display=swap" rel="stylesheet">
        <style>
        * {{ margin:0; padding:0; box-sizing:border-box; }}
        body {{ background:#111; display:flex; justify-content:center; padding:40px; }}
        .poster {{
            width:900px; min-height:1100px;
            background:linear-gradient(160deg,#0a0a0a 0%,#1a1a1a 50%,#0d0d0d 100%);
            border-radius:32px; overflow:hidden;
            box-shadow:0 40px 100px rgba(0,0,0,0.8), 0 0 0 2px #B8860B;
            position:relative; font-family:'Raleway','Noto Sans Telugu',sans-serif;
        }}
        .gold-bar {{ height:8px; background:linear-gradient(90deg,#B8860B,#FFD700,#B8860B,#FFD700,#B8860B); }}
        .corner-tl,.corner-tr,.corner-bl,.corner-br {{
            position:absolute; width:80px; height:80px;
            border-color:#B8860B; border-style:solid;
        }}
        .corner-tl {{ top:20px; left:20px; border-width:3px 0 0 3px; }}
        .corner-tr {{ top:20px; right:20px; border-width:3px 3px 0 0; }}
        .corner-bl {{ bottom:20px; left:20px; border-width:0 0 3px 3px; }}
        .corner-br {{ bottom:20px; right:20px; border-width:0 3px 3px 0; }}
        .content {{ padding:60px; position:relative; z-index:2; }}
        .header {{ display:flex; align-items:center; gap:30px; margin-bottom:40px; }}
        .logo-wrap {{
            width:120px; height:120px; border-radius:20px;
            border:3px solid #B8860B; overflow:hidden;
            box-shadow:0 0 20px rgba(184,134,11,0.4);
            background:#1a1a1a; display:flex; align-items:center; justify-content:center; flex-shrink:0;
        }}
        .shop-name {{
            font-family:'Cinzel',serif; font-size:60px; font-weight:900;
            background:linear-gradient(135deg,#FFD700,#B8860B,#FFD700);
            -webkit-background-clip:text; -webkit-text-fill-color:transparent;
            line-height:1.1;
        }}
        .shop-tag {{
            display:inline-block; border:1px solid #B8860B;
            color:#B8860B; font-size:14px; font-weight:700;
            padding:6px 20px; border-radius:50px; margin-top:10px;
            letter-spacing:3px; text-transform:uppercase;
        }}
        .festival-pill {{
            display:inline-flex; align-items:center; gap:12px;
            border:1px solid #B8860B44; border-radius:50px;
            padding:10px 25px; background:rgba(184,134,11,0.1); margin-bottom:28px;
        }}
        .festival-pill img {{ width:30px; height:30px; filter:sepia(1) saturate(3) hue-rotate(5deg); }}
        .festival-pill span {{ font-size:20px; font-weight:700; color:#FFD700; }}
        .offer-box {{
            background:linear-gradient(135deg,#B8860B22,#FFD70033);
            border:2px solid #B8860B; border-radius:24px;
            padding:35px 45px; margin:25px 0;
            box-shadow:0 0 40px rgba(184,134,11,0.2);
            display:flex; align-items:center; gap:25px;
        }}
        .offer-label {{ font-size:13px; font-weight:800; color:#B8860B; letter-spacing:4px; text-transform:uppercase; margin-bottom:8px; }}
        .offer-value {{
            font-family:'Cinzel',serif; font-size:60px; font-weight:900;
            background:linear-gradient(135deg,#FFD700,#FFF8DC);
            -webkit-background-clip:text; -webkit-text-fill-color:transparent;
        }}
        .offer-icon {{ width:80px; height:80px; opacity:0.3; filter:sepia(1) saturate(3); flex-shrink:0; }}
        .caption-box {{
            border-left:4px solid #B8860B; padding:25px 30px; margin:25px 0;
            background:rgba(184,134,11,0.05);
        }}
        .caption-text {{ font-size:28px; line-height:1.8; color:#DDD; font-family:'Noto Sans Telugu','Raleway',sans-serif; }}
        .divider {{ height:1px; background:linear-gradient(90deg,transparent,#B8860B,transparent); margin:30px 0; }}
        .contact-item {{ display:flex; align-items:center; gap:18px; margin-bottom:18px; }}
        .contact-icon-box {{
            width:46px; height:46px; border-radius:12px;
            border:1px solid #B8860B; display:flex; align-items:center; justify-content:center;
            background:rgba(184,134,11,0.1); flex-shrink:0;
        }}
        .contact-icon-box img {{ width:24px; height:24px; filter:sepia(1) saturate(3) hue-rotate(5deg); }}
        .contact-text {{ font-size:26px; font-weight:700; color:#DDD; }}
        .watermark {{ position:absolute; bottom:50px; right:55px; width:130px; height:130px; opacity:0.05; }}
        </style></head><body>
        <div class="poster">
        <div class="gold-bar"></div>
        <div class="corner-tl"></div><div class="corner-tr"></div>
        <div class="corner-bl"></div><div class="corner-br"></div>
        <div class="content">
        <div class="header">
        <div class="logo-wrap">{logo_html}</div>
        <div>
        <div class="shop-name">{shop}</div>
        <div class="shop-tag">{shop_type}</div>
        </div></div>
        <div class="festival-pill">
        <img src="{festival_icon}">
        <span>{festival} Special</span>
        </div>
        <div class="offer-box">
        <div style="flex:1">
        <div class="offer-label">Exclusive Offer</div>
        <div class="offer-value">{offer}</div>
        </div>
        <img class="offer-icon" src="{shop_icon}">
        </div>
        <div class="caption-box"><div class="caption-text">{result}</div></div>
        <div class="divider"></div>
        <div class="contact-item">
        <div class="contact-icon-box"><img src="https://cdn-icons-png.flaticon.com/512/597/597177.png"></div>
        <div class="contact-text">{customer_phone}</div>
        </div>
        <div class="contact-item">
        <div class="contact-icon-box"><img src="https://cdn-icons-png.flaticon.com/512/684/684908.png"></div>
        <div class="contact-text">{customer_address}</div>
        </div>
        </div>
        <img class="watermark" src="{shop_icon}">
        <div class="gold-bar"></div>
        </div></body></html>"""

    elif design == 2:
        # ---- DESIGN 2: FESTIVE COLORFUL INDIAN STYLE ----
        return f"""
        <html><head><meta charset="UTF-8">
        <link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@700;800&family=Hind:wght@400;600&family=Noto+Sans+Telugu:wght@400;700&display=swap" rel="stylesheet">
        <style>
        * {{ margin:0; padding:0; box-sizing:border-box; }}
        body {{ background:#f5f5f5; display:flex; justify-content:center; padding:40px; }}
        .poster {{
            width:900px; min-height:1100px;
            background:linear-gradient(160deg,#FF6B35 0%,#FF8C42 30%,#FFA726 60%,#FFD93D 100%);
            border-radius:32px; overflow:hidden;
            box-shadow:0 40px 100px rgba(255,107,53,0.4);
            position:relative; font-family:'Hind','Noto Sans Telugu',sans-serif;
        }}
        .pattern-top {{
            height:70px;
            background:repeating-linear-gradient(
                45deg, rgba(255,255,255,0.1) 0px, rgba(255,255,255,0.1) 10px,
                transparent 10px, transparent 20px
            );
        }}
        .white-card {{
            background:white; margin:0 20px 20px 20px; border-radius:24px;
            padding:45px; box-shadow:0 20px 60px rgba(0,0,0,0.15);
        }}
        .header {{ display:flex; align-items:center; gap:25px; margin-bottom:30px; padding-bottom:25px; border-bottom:3px dashed #FFD93D; }}
        .logo-wrap {{
            width:120px; height:120px; border-radius:20px;
            border:4px solid #FF6B35; overflow:hidden;
            box-shadow:0 8px 20px rgba(255,107,53,0.3);
            background:#fff8f0; display:flex; align-items:center; justify-content:center; flex-shrink:0;
        }}
        .shop-name {{ font-family:'Baloo 2',serif; font-size:60px; font-weight:800; color:#1a1a1a; line-height:1.0; }}
        .shop-tag {{
            display:inline-block; background:#FF6B35; color:white;
            font-size:15px; font-weight:700; padding:6px 18px;
            border-radius:50px; margin-top:10px; letter-spacing:2px; text-transform:uppercase;
        }}
        .festival-pill {{
            display:inline-flex; align-items:center; gap:12px;
            background:linear-gradient(135deg,#FF6B35,#FFD93D);
            border-radius:50px; padding:12px 28px; margin-bottom:22px;
            box-shadow:0 4px 15px rgba(255,107,53,0.3);
        }}
        .festival-pill img {{ width:32px; height:32px; filter:brightness(10); }}
        .festival-pill span {{ font-size:22px; font-weight:800; color:white; }}
        .offer-box {{
            background:linear-gradient(135deg,#FF6B35,#FF3D71);
            border-radius:20px; padding:30px 40px; margin:20px 0;
            box-shadow:0 12px 35px rgba(255,60,60,0.35);
            display:flex; align-items:center; gap:20px; position:relative; overflow:hidden;
        }}
        .offer-box::after {{
            content:''; position:absolute; right:-20px; top:-20px;
            width:120px; height:120px; border-radius:50%; background:rgba(255,255,255,0.1);
        }}
        .offer-label {{ font-size:14px; color:rgba(255,255,255,0.8); font-weight:800; letter-spacing:3px; text-transform:uppercase; }}
        .offer-value {{ font-family:'Baloo 2',serif; font-size:60px; font-weight:800; color:white; text-shadow:2px 4px 12px rgba(0,0,0,0.2); }}
        .offer-icon {{ width:80px; height:80px; opacity:0.25; filter:brightness(10); position:relative; z-index:1; flex-shrink:0; }}
        .caption-box {{
            background:#FFF8F0; border-left:6px solid #FF6B35;
            border-radius:0 16px 16px 0; padding:22px 28px; margin:20px 0;
        }}
        .caption-text {{ font-size:28px; line-height:1.75; color:#333; font-family:'Noto Sans Telugu','Hind',sans-serif; }}
        .divider {{ height:2px; background:linear-gradient(90deg,transparent,#FFD93D,transparent); margin:25px 0; }}
        .contact-item {{ display:flex; align-items:center; gap:16px; margin-bottom:16px; }}
        .contact-icon-box {{
            width:46px; height:46px; border-radius:12px;
            background:#FF6B35; display:flex; align-items:center; justify-content:center;
            box-shadow:0 4px 12px rgba(255,107,53,0.3); flex-shrink:0;
        }}
        .contact-icon-box img {{ width:24px; height:24px; filter:brightness(10); }}
        .contact-text {{ font-size:26px; font-weight:700; color:#1a1a1a; }}
        </style></head><body>
        <div class="poster">
        <div class="pattern-top"></div>
        <div class="white-card">
        <div class="header">
        <div class="logo-wrap">{logo_html}</div>
        <div>
        <div class="shop-name">{shop}</div>
        <div class="shop-tag">{shop_type}</div>
        </div></div>
        <div class="festival-pill">
        <img src="{festival_icon}">
        <span>{festival} Special</span>
        </div>
        <div class="offer-box">
        <div style="flex:1">
        <div class="offer-label">Exclusive Offer</div>
        <div class="offer-value">{offer}</div>
        </div>
        <img class="offer-icon" src="{shop_icon}">
        </div>
        <div class="caption-box"><div class="caption-text">{result}</div></div>
        <div class="divider"></div>
        <div class="contact-item">
        <div class="contact-icon-box"><img src="https://cdn-icons-png.flaticon.com/512/597/597177.png"></div>
        <div class="contact-text">{customer_phone}</div>
        </div>
        <div class="contact-item">
        <div class="contact-icon-box"><img src="https://cdn-icons-png.flaticon.com/512/684/684908.png"></div>
        <div class="contact-text">{customer_address}</div>
        </div>
        </div>
        </div></body></html>"""   

    elif design == 3:
                # ---- DESIGN 3: MODERN MINIMAL ----
        return f"""
        <html><head><meta charset="UTF-8">
        <link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@400;500;700&family=Noto+Sans+Telugu:wght@400;700&display=swap" rel="stylesheet">
        <style>
        * {{ margin:0; padding:0; box-sizing:border-box; }}
        body {{ background:#f0f0f0; display:flex; justify-content:center; padding:40px; }}
        .poster {{
            width:900px; min-height:1100px; background:#FAFAFA;
            border-radius:32px; overflow:hidden;
            box-shadow:0 40px 100px rgba(0,0,0,0.15);
            position:relative; font-family:'DM Sans','Noto Sans Telugu',sans-serif;
            border:1px solid #E0E0E0;
        }}
        .accent-bar {{ height:8px; background:{bg_color}; }}
        .content {{ padding:60px; }}
        .header {{ display:flex; align-items:center; gap:28px; margin-bottom:50px; }}
        .logo-wrap {{
            width:110px; height:110px; border-radius:22px;
            border:2px solid #E0E0E0; overflow:hidden;
            background:white; display:flex; align-items:center; justify-content:center;
            box-shadow:0 4px 20px rgba(0,0,0,0.08); flex-shrink:0;
        }}
        .shop-name {{ font-family:'DM Serif Display',serif; font-size:65px; color:#111; line-height:1.0; letter-spacing:-1px; }}
        .shop-tag {{
            display:inline-block; background:#111; color:white;
            font-size:13px; font-weight:700; padding:6px 18px;
            border-radius:4px; margin-top:12px; letter-spacing:2px; text-transform:uppercase;
        }}
        .festival-pill {{
            display:inline-flex; align-items:center; gap:10px;
            border:2px solid #111; border-radius:4px;
            padding:10px 22px; margin-bottom:28px;
        }}
        .festival-pill img {{ width:28px; height:28px; }}
        .festival-pill span {{ font-size:20px; font-weight:700; color:#111; }}
        .offer-box {{
            background:#111; border-radius:20px;
            padding:40px 45px; margin:28px 0;
            display:flex; align-items:center; gap:25px;
        }}
        .offer-label {{ font-size:13px; color:rgba(255,255,255,0.5); font-weight:700; letter-spacing:4px; text-transform:uppercase; margin-bottom:8px; }}
        .offer-value {{ font-family:'DM Serif Display',serif; font-size:65px; color:white; line-height:1.0; }}
        .offer-icon {{ width:80px; height:80px; opacity:0.15; filter:invert(1); flex-shrink:0; }}
        .caption-box {{
            border-left:4px solid #111; padding:22px 28px; margin:25px 0; background:#F5F5F5;
        }}
        .caption-text {{ font-size:28px; line-height:1.8; color:#444; font-family:'Noto Sans Telugu','DM Sans',sans-serif; }}
        .divider {{ height:1px; background:#E0E0E0; margin:30px 0; }}
        .contact-item {{ display:flex; align-items:center; gap:16px; margin-bottom:16px; }}
        .contact-icon-box {{
            width:44px; height:44px; border-radius:10px;
            background:#111; display:flex; align-items:center; justify-content:center; flex-shrink:0;
        }}
        .contact-icon-box img {{ width:22px; height:22px; filter:invert(1); }}
        .contact-text {{ font-size:26px; font-weight:600; color:#111; }}
        .watermark {{ position:absolute; bottom:50px; right:55px; width:120px; height:120px; opacity:0.04; }}
        </style></head><body>
        <div class="poster">
        <div class="accent-bar"></div>
        <div class="content">
        <div class="header">
        <div class="logo-wrap">{logo_html}</div>
        <div>
        <div class="shop-name">{shop}</div>
        <div class="shop-tag">{shop_type}</div>
        </div></div>
        <div class="festival-pill">
        <img src="{festival_icon}">
        <span>{festival} Special</span>
        </div>
        <div class="offer-box">
        <div style="flex:1">
        <div class="offer-label">Exclusive Offer</div>
        <div class="offer-value">{offer}</div>
        </div>
        <img class="offer-icon" src="{shop_icon}">
        </div>
        <div class="caption-box"><div class="caption-text">{result}</div></div>
        <div class="divider"></div>
        <div class="contact-item">
        <div class="contact-icon-box"><img src="https://cdn-icons-png.flaticon.com/512/597/597177.png"></div>
        <div class="contact-text">{customer_phone}</div>
        </div>
        <div class="contact-item">
        <div class="contact-icon-box"><img src="https://cdn-icons-png.flaticon.com/512/684/684908.png"></div>
        <div class="contact-text">{customer_address}</div>
        </div>
        </div>
        <img class="watermark" src="{shop_icon}">
        <div class="accent-bar"></div>
        </div></body></html>"""  

    elif design == 4:
        # ---- DESIGN 4: VIBRANT GRADIENT SOCIAL MEDIA ----
        return f"""
        <html><head><meta charset="UTF-8">
        <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;700;900&family=Noto+Sans+Telugu:wght@400;700&display=swap" rel="stylesheet">
        <style>
        * {{ margin:0; padding:0; box-sizing:border-box; }}
        body {{ background:#1a1a2e; display:flex; justify-content:center; padding:40px; }}
        .poster {{
            width:900px; min-height:1100px;
            background:linear-gradient(135deg,#667eea 0%,#764ba2 30%,#f64f59 60%,#c471ed 80%,#12c2e9 100%);
            border-radius:32px; overflow:hidden;
            box-shadow:0 40px 100px rgba(102,126,234,0.5);
            position:relative; font-family:'Outfit','Noto Sans Telugu',sans-serif;
            padding:4px;
        }}
        .inner {{
            background:linear-gradient(135deg,rgba(255,255,255,0.12),rgba(255,255,255,0.05));
            border-radius:30px; min-height:100%;
            backdrop-filter:blur(10px); padding:55px;
        }}
        .header {{ display:flex; align-items:center; gap:28px; margin-bottom:40px; }}
        .logo-wrap {{
            width:120px; height:120px; border-radius:24px;
            border:3px solid rgba(255,255,255,0.5); overflow:hidden;
            background:rgba(255,255,255,0.15);
            display:flex; align-items:center; justify-content:center;
            box-shadow:0 8px 32px rgba(0,0,0,0.2); flex-shrink:0;
        }}
        .shop-name {{ font-size:64px; font-weight:900; color:white; line-height:1.0; text-shadow:2px 4px 20px rgba(0,0,0,0.3); }}
        .shop-tag {{
            display:inline-block; background:rgba(255,255,255,0.2);
            border:1px solid rgba(255,255,255,0.4); color:white;
            font-size:14px; font-weight:700; padding:6px 18px;
            border-radius:50px; margin-top:10px; letter-spacing:2px; text-transform:uppercase;
        }}
        .festival-pill {{
            display:inline-flex; align-items:center; gap:12px;
            background:rgba(255,255,255,0.2); border:1px solid rgba(255,255,255,0.3);
            border-radius:50px; padding:12px 28px; margin-bottom:28px;
        }}
        .festival-pill img {{ width:30px; height:30px; filter:brightness(10); }}
        .festival-pill span {{ font-size:22px; font-weight:700; color:white; }}
        .offer-box {{
            background:rgba(255,255,255,0.15); border:1px solid rgba(255,255,255,0.3);
            border-radius:24px; padding:35px 45px; margin:25px 0;
            backdrop-filter:blur(20px); box-shadow:0 8px 32px rgba(0,0,0,0.1);
            display:flex; align-items:center; gap:25px;
        }}
        .offer-label {{ font-size:13px; color:rgba(255,255,255,0.7); font-weight:700; letter-spacing:4px; text-transform:uppercase; margin-bottom:8px; }}
        .offer-value {{ font-size:64px; font-weight:900; color:white; line-height:1.0; text-shadow:2px 4px 20px rgba(0,0,0,0.2); }}
        .offer-icon {{ width:80px; height:80px; opacity:0.2; filter:brightness(10); flex-shrink:0; }}
        .caption-box {{
            background:rgba(255,255,255,0.1); border:1px solid rgba(255,255,255,0.2);
            border-radius:16px; padding:25px 30px; margin:25px 0;
        }}
        .caption-text {{ font-size:28px; line-height:1.75; color:rgba(255,255,255,0.9); font-family:'Noto Sans Telugu','Outfit',sans-serif; }}
        .divider {{ height:1px; background:rgba(255,255,255,0.2); margin:28px 0; }}
        .contact-item {{ display:flex; align-items:center; gap:16px; margin-bottom:16px; }}
        .contact-icon-box {{
            width:46px; height:46px; border-radius:12px;
            background:rgba(255,255,255,0.2); border:1px solid rgba(255,255,255,0.3);
            display:flex; align-items:center; justify-content:center; flex-shrink:0;
        }}
        .contact-icon-box img {{ width:24px; height:24px; filter:brightness(10); }}
        .contact-text {{ font-size:26px; font-weight:700; color:white; }}
        .watermark {{ position:absolute; bottom:50px; right:55px; width:130px; height:130px; opacity:0.08; filter:brightness(10); }}
        </style></head><body>
        <div class="poster">
        <div class="inner">
        <div class="header">
        <div class="logo-wrap">{logo_html}</div>
        <div>
        <div class="shop-name">{shop}</div>
        <div class="shop-tag">{shop_type}</div>
        </div></div>
        <div class="festival-pill">
        <img src="{festival_icon}">
        <span>{festival} Special</span>
        </div>
        <div class="offer-box">
        <div style="flex:1">
        <div class="offer-label">Exclusive Offer</div>
        <div class="offer-value">{offer}</div>
        </div>
        <img class="offer-icon" src="{shop_icon}">
        </div>
        <div class="caption-box"><div class="caption-text">{result}</div></div>
        <div class="divider"></div>
        <div class="contact-item">
        <div class="contact-icon-box"><img src="https://cdn-icons-png.flaticon.com/512/597/597177.png"></div>
        <div class="contact-text">{customer_phone}</div>
        </div>
        <div class="contact-item">
        <div class="contact-icon-box"><img src="https://cdn-icons-png.flaticon.com/512/684/684908.png"></div>
        <div class="contact-text">{customer_address}</div>
        </div>
        </div>
        <img class="watermark" src="{shop_icon}">
        </div></body></html>"""

    else:
        return f"""
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