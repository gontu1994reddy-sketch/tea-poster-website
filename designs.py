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
        # Logo: Round with gold glow
        # Offer: Giant centered gold gradient text
        # Content: Italic quote with gold marks
        # Phone/Address: Dark cards with gold circle icons
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
            .corner-tl,.corner-tr,.corner-bl,.corner-br {{ position:absolute; width:80px; height:80px; border-color:#B8860B; border-style:solid; }}
            .corner-tl {{ top:20px; left:20px; border-width:3px 0 0 3px; }}
            .corner-tr {{ top:20px; right:20px; border-width:3px 3px 0 0; }}
            .corner-bl {{ bottom:20px; left:20px; border-width:0 0 3px 3px; }}
            .corner-br {{ bottom:20px; right:20px; border-width:0 3px 3px 0; }}
            .content {{ padding:60px; position:relative; z-index:2; }}
            .header {{ display:flex; align-items:center; gap:30px; margin-bottom:40px; }}
            .logo-wrap {{
                width:130px; height:130px; border-radius:50%;
                border:4px solid #FFD700;
                box-shadow:0 0 30px rgba(255,215,0,0.6), 0 0 60px rgba(255,215,0,0.2);
                overflow:hidden; background:#1a1a1a;
                display:flex; align-items:center; justify-content:center; flex-shrink:0;
            }}
            .shop-name {{
                font-family:'Cinzel',serif; font-size:58px; font-weight:900;
                background:linear-gradient(135deg,#FFD700,#B8860B,#FFD700);
                -webkit-background-clip:text; -webkit-text-fill-color:transparent; line-height:1.1;
            }}
            .shop-tag {{ display:inline-block; border:1px solid #B8860B; color:#B8860B; font-size:14px; font-weight:700; padding:6px 20px; border-radius:50px; margin-top:10px; letter-spacing:3px; text-transform:uppercase; }}
            .festival-pill {{ display:inline-flex; align-items:center; gap:12px; border:1px solid #B8860B44; border-radius:50px; padding:10px 25px; background:rgba(184,134,11,0.1); margin-bottom:28px; }}
            .festival-pill img {{ width:30px; height:30px; filter:sepia(1) saturate(3) hue-rotate(5deg); }}
            .festival-pill span {{ font-size:20px; font-weight:700; color:#FFD700; }}
            .offer-box {{ text-align:center; padding:40px 20px; margin:25px 0; border-top:1px solid #B8860B44; border-bottom:1px solid #B8860B44; }}
            .offer-eyebrow {{ font-size:13px; font-weight:800; color:#B8860B; letter-spacing:5px; margin-bottom:15px; text-transform:uppercase; }}
            .offer-value {{ font-family:'Cinzel',serif; font-size:80px; font-weight:900; background:linear-gradient(135deg,#FFD700,#FFF8DC,#B8860B); -webkit-background-clip:text; -webkit-text-fill-color:transparent; line-height:1.0; }}
            .offer-icon {{ width:50px; height:50px; opacity:0.3; filter:sepia(1) saturate(3); margin-top:10px; }}
            .caption-box {{ padding:30px 40px; margin:28px 0; background:linear-gradient(135deg,rgba(184,134,11,0.08),transparent); border-radius:16px; text-align:center; }}
            .caption-text {{ font-size:26px; line-height:1.9; color:#CCC; font-family:'Noto Sans Telugu','Raleway',sans-serif; font-style:italic; }}
            .quote-mark {{ font-size:60px; color:#B8860B; line-height:0.5; vertical-align:-20px; font-family:'Cinzel',serif; }}
            .divider {{ height:1px; background:linear-gradient(90deg,transparent,#B8860B,transparent); margin:30px 0; }}
            .contact-card {{ background:rgba(184,134,11,0.08); border:1px solid #B8860B44; border-radius:14px; padding:16px 24px; display:flex; align-items:center; gap:18px; margin-bottom:14px; }}
            .contact-icon-circle {{ width:46px; height:46px; border-radius:50%; border:2px solid #B8860B; display:flex; align-items:center; justify-content:center; flex-shrink:0; }}
            .contact-icon-circle img {{ width:22px; height:22px; filter:sepia(1) saturate(3) hue-rotate(5deg); }}
            .contact-label {{ font-size:11px; color:#B8860B; font-weight:800; letter-spacing:2px; text-transform:uppercase; }}
            .contact-text {{ font-size:24px; font-weight:700; color:#EEE; }}
            .watermark {{ position:absolute; bottom:50px; right:55px; width:130px; height:130px; opacity:0.05; }}
            </style></head><body>
            <div class="poster">
            <div class="gold-bar"></div>
            <div class="corner-tl"></div><div class="corner-tr"></div><div class="corner-bl"></div><div class="corner-br"></div>
            <div class="content">
            <div class="header">
            <div class="logo-wrap">{logo_html}</div>
            <div><div class="shop-name">{shop}</div><div class="shop-tag">{shop_type}</div></div>
            </div>
            <div class="festival-pill"><img src="{festival_icon}"><span>{festival} Special</span></div>
            <div class="offer-box">
            <div class="offer-eyebrow">★ Exclusive Offer ★</div>
            <div class="offer-value">{offer}</div>
            <br><img class="offer-icon" src="{shop_icon}">
            </div>
            <div class="caption-box">
            <span class="quote-mark">"</span>
            <div class="caption-text">{result}</div>
            <span class="quote-mark">"</span>
            </div>
            <div class="divider"></div>
            <div class="contact-card">
            <div class="contact-icon-circle"><img src="https://cdn-icons-png.flaticon.com/512/597/597177.png"></div>
            <div><div class="contact-label">Phone</div><div class="contact-text">{customer_phone}</div></div>
            </div>
            <div class="contact-card">
            <div class="contact-icon-circle"><img src="https://cdn-icons-png.flaticon.com/512/684/684908.png"></div>
            <div><div class="contact-label">Address</div><div class="contact-text">{customer_address}</div></div>
            </div>
            </div>
            <img class="watermark" src="{shop_icon}">
            <div class="gold-bar"></div>
            </div></body></html>"""

    elif design == 2:
        # ---- DESIGN 2: MODERN MINIMAL ----
        # Logo: Top-right stamp with rotation
        # Offer: Huge oversized black text with bar
        # Content: Numbered grey card
        # Phone/Address: Underline minimal style
        return f"""
            <html><head><meta charset="UTF-8">
            <link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@400;500;700&family=Noto+Sans+Telugu:wght@400;700&display=swap" rel="stylesheet">
            <style>
            * {{ margin:0; padding:0; box-sizing:border-box; }}
            body {{ background:#f0f0f0; display:flex; justify-content:center; padding:40px; }}
            .poster {{ width:900px; min-height:1100px; background:#FAFAFA; border-radius:32px; overflow:hidden; box-shadow:0 40px 100px rgba(0,0,0,0.15); position:relative; font-family:'DM Sans','Noto Sans Telugu',sans-serif; border:1px solid #E0E0E0; }}
            .accent-bar {{ height:8px; background:{bg_color}; }}
            .content {{ padding:55px 60px; }}
            .header {{ display:flex; align-items:flex-start; justify-content:space-between; margin-bottom:45px; }}
            .shop-info {{ flex:1; }}
            .shop-name {{ font-family:'DM Serif Display',serif; font-size:68px; color:#111; line-height:1.0; letter-spacing:-2px; }}
            .shop-tag {{ display:inline-block; background:#111; color:white; font-size:13px; font-weight:700; padding:6px 18px; border-radius:4px; margin-top:12px; letter-spacing:2px; text-transform:uppercase; }}
            .logo-wrap {{ width:110px; height:110px; border-radius:12px; border:3px solid #111; overflow:hidden; background:white; display:flex; align-items:center; justify-content:center; flex-shrink:0; transform:rotate(3deg); box-shadow:4px 4px 0px #111; }}
            .festival-pill {{ display:inline-flex; align-items:center; gap:10px; border:2px solid #111; border-radius:4px; padding:10px 22px; margin-bottom:35px; }}
            .festival-pill img {{ width:28px; height:28px; }}
            .festival-pill span {{ font-size:20px; font-weight:700; color:#111; }}
            .offer-section {{ margin:10px 0 35px 0; border-top:3px solid #111; padding-top:20px; }}
            .offer-eyebrow {{ font-size:12px; font-weight:800; color:#888; letter-spacing:5px; text-transform:uppercase; margin-bottom:5px; }}
            .offer-value {{ font-family:'DM Serif Display',serif; font-size:90px; color:#111; line-height:0.9; letter-spacing:-3px; word-break:break-word; }}
            .offer-bar {{ height:6px; background:#111; margin-top:15px; border-radius:3px; width:80px; }}
            .caption-box {{ background:#F5F5F5; border-radius:16px; padding:30px 35px; margin:25px 0; position:relative; }}
            .caption-number {{ font-size:80px; font-weight:900; color:#E0E0E0; position:absolute; top:10px; right:20px; font-family:'DM Serif Display',serif; line-height:1; }}
            .caption-text {{ font-size:27px; line-height:1.85; color:#444; font-family:'Noto Sans Telugu','DM Sans',sans-serif; position:relative; z-index:1; }}
            .divider {{ height:1px; background:#E0E0E0; margin:30px 0; }}
            .contact-minimal {{ padding:14px 0; border-bottom:1px solid #E8E8E8; display:flex; align-items:center; gap:20px; }}
            .contact-minimal:last-child {{ border-bottom:none; }}
            .contact-dot {{ width:10px; height:10px; border-radius:50%; background:#111; flex-shrink:0; }}
            .contact-info {{ flex:1; }}
            .contact-label {{ font-size:11px; font-weight:800; color:#999; letter-spacing:2px; text-transform:uppercase; }}
            .contact-text {{ font-size:26px; font-weight:700; color:#111; }}
            .contact-icon-small {{ width:36px; height:36px; opacity:0.3; }}
            .watermark {{ position:absolute; bottom:50px; right:55px; width:120px; height:120px; opacity:0.04; }}
            </style></head><body>
            <div class="poster">
            <div class="accent-bar"></div>
            <div class="content">
            <div class="header">
            <div class="shop-info"><div class="shop-name">{shop}</div><div class="shop-tag">{shop_type}</div></div>
            <div class="logo-wrap">{logo_html}</div>
            </div>
            <div class="festival-pill"><img src="{festival_icon}"><span>{festival} Special</span></div>
            <div class="offer-section">
            <div class="offer-eyebrow">Exclusive Offer</div>
            <div class="offer-value">{offer}</div>
            <div class="offer-bar"></div>
            </div>
            <div class="caption-box">
            <div class="caption-number">01</div>
            <div class="caption-text">{result}</div>
            </div>
            <div class="divider"></div>
            <div class="contact-minimal">
            <div class="contact-dot"></div>
            <div class="contact-info"><div class="contact-label">Phone</div><div class="contact-text">{customer_phone}</div></div>
            <img class="contact-icon-small" src="https://cdn-icons-png.flaticon.com/512/597/597177.png">
            </div>
            <div class="contact-minimal">
            <div class="contact-dot"></div>
            <div class="contact-info"><div class="contact-label">Address</div><div class="contact-text">{customer_address}</div></div>
            <img class="contact-icon-small" src="https://cdn-icons-png.flaticon.com/512/684/684908.png">
            </div>
            </div>
            <img class="watermark" src="{shop_icon}">
            <div class="accent-bar"></div>
            </div></body></html>"""    

    elif design == 3:
        # ---- DESIGN 3: FESTIVE COLORFUL INDIAN STYLE ----
        # Logo: Square with offset shadow border
        # Offer: Full width ribbon banner
        # Content: Yellow sticky note style
        # Phone/Address: Gradient pill badges
        return f"""
            <html><head><meta charset="UTF-8">
            <link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@700;800&family=Hind:wght@400;600&family=Noto+Sans+Telugu:wght@400;700&display=swap" rel="stylesheet">
            <style>
            * {{ margin:0; padding:0; box-sizing:border-box; }}
            body {{ background:#f5f5f5; display:flex; justify-content:center; padding:40px; }}
            .poster {{ width:900px; min-height:1100px; background:linear-gradient(160deg,#FF6B35 0%,#FF8C42 30%,#FFA726 60%,#FFD93D 100%); border-radius:32px; overflow:hidden; box-shadow:0 40px 100px rgba(255,107,53,0.4); position:relative; font-family:'Hind','Noto Sans Telugu',sans-serif; }}
            .pattern-top {{ height:70px; background:repeating-linear-gradient(45deg,rgba(255,255,255,0.1) 0px,rgba(255,255,255,0.1) 10px,transparent 10px,transparent 20px); }}
            .white-card {{ background:white; margin:0 20px 20px 20px; border-radius:24px; padding:45px; box-shadow:0 20px 60px rgba(0,0,0,0.15); }}
            .header {{ display:flex; align-items:center; gap:25px; margin-bottom:30px; padding-bottom:25px; border-bottom:3px dashed #FFD93D; }}
            .logo-wrap {{ width:120px; height:120px; border-radius:16px; border:5px solid #FF6B35; box-shadow:6px 6px 0px #FFD93D; overflow:hidden; background:#fff8f0; display:flex; align-items:center; justify-content:center; flex-shrink:0; }}
            .shop-name {{ font-family:'Baloo 2',serif; font-size:60px; font-weight:800; color:#1a1a1a; line-height:1.0; }}
            .shop-tag {{ display:inline-block; background:#FF6B35; color:white; font-size:15px; font-weight:700; padding:6px 18px; border-radius:50px; margin-top:10px; letter-spacing:2px; text-transform:uppercase; }}
            .festival-pill {{ display:inline-flex; align-items:center; gap:12px; background:linear-gradient(135deg,#FF6B35,#FFD93D); border-radius:50px; padding:12px 28px; margin-bottom:22px; box-shadow:0 4px 15px rgba(255,107,53,0.3); }}
            .festival-pill img {{ width:32px; height:32px; filter:brightness(10); }}
            .festival-pill span {{ font-size:22px; font-weight:800; color:white; }}
            .offer-ribbon {{ background:linear-gradient(135deg,#FF3D00,#FF6B35); margin:0 -45px; padding:28px 60px; position:relative; margin-bottom:25px; box-shadow:0 8px 25px rgba(255,60,0,0.3); }}
            .offer-top {{ font-size:14px; color:rgba(255,255,255,0.8); font-weight:800; letter-spacing:4px; text-transform:uppercase; margin-bottom:5px; }}
            .offer-value {{ font-family:'Baloo 2',serif; font-size:68px; font-weight:800; color:white; line-height:1.0; text-shadow:3px 3px 0px rgba(0,0,0,0.2); }}
            .offer-sub {{ display:flex; align-items:center; gap:10px; margin-top:8px; }}
            .offer-sub img {{ width:30px; height:30px; filter:brightness(10); opacity:0.6; }}
            .offer-sub span {{ font-size:16px; color:rgba(255,255,255,0.7); font-weight:600; }}
            .caption-box {{ background:#FFFDE7; border:2px solid #FFD93D; border-radius:4px 16px 16px 16px; padding:24px 30px; margin:25px 0; box-shadow:4px 4px 0px #FFD93D; position:relative; }}
            .caption-box::before {{ content:'📢'; position:absolute; top:-18px; left:20px; font-size:28px; }}
            .caption-text {{ font-size:27px; line-height:1.75; color:#333; font-family:'Noto Sans Telugu','Hind',sans-serif; }}
            .divider {{ height:3px; background:linear-gradient(90deg,#FF6B35,#FFD93D,#FF6B35); margin:25px 0; border-radius:2px; }}
            .contact-pill {{ display:flex; align-items:center; gap:16px; background:linear-gradient(135deg,#FF6B3515,#FFD93D15); border:2px solid #FF6B3544; border-radius:50px; padding:14px 28px; margin-bottom:14px; }}
            .contact-icon-box {{ width:46px; height:46px; border-radius:50%; background:linear-gradient(135deg,#FF6B35,#FFD93D); display:flex; align-items:center; justify-content:center; flex-shrink:0; box-shadow:0 4px 12px rgba(255,107,53,0.3); }}
            .contact-icon-box img {{ width:24px; height:24px; filter:brightness(10); }}
            .contact-text {{ font-size:26px; font-weight:700; color:#1a1a1a; }}
            </style></head><body>
            <div class="poster">
            <div class="pattern-top"></div>
            <div class="white-card">
            <div class="header">
            <div class="logo-wrap">{logo_html}</div>
            <div><div class="shop-name">{shop}</div><div class="shop-tag">{shop_type}</div></div>
            </div>
            <div class="festival-pill"><img src="{festival_icon}"><span>{festival} Special</span></div>
            <div class="offer-ribbon">
            <div class="offer-top">🔥 Exclusive Offer</div>
            <div class="offer-value">{offer}</div>
            <div class="offer-sub"><img src="{shop_icon}"><span>{shop_type}</span></div>
            </div>
            <div style="height:25px;"></div>
            <div class="caption-box"><div class="caption-text">{result}</div></div>
            <div class="divider"></div>
            <div class="contact-pill">
            <div class="contact-icon-box"><img src="https://cdn-icons-png.flaticon.com/512/597/597177.png"></div>
            <div class="contact-text">{customer_phone}</div>
            </div>
            <div class="contact-pill">
            <div class="contact-icon-box"><img src="https://cdn-icons-png.flaticon.com/512/684/684908.png"></div>
            <div class="contact-text">{customer_address}</div>
            </div>
            </div></div></body></html>""" 

    else:
        # ---- DESIGN 4: VIBRANT GRADIENT SOCIAL MEDIA ----
        # Logo: Hexagon clip with glow
        # Offer: Glass floating card with shop badge
        # Content: Chat bubble style
        # Phone/Address: Neon glow cards with labels
        return f"""
            <html><head><meta charset="UTF-8">
            <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;700;900&family=Noto+Sans+Telugu:wght@400;700&display=swap" rel="stylesheet">
            <style>
            * {{ margin:0; padding:0; box-sizing:border-box; }}
            body {{ background:#1a1a2e; display:flex; justify-content:center; padding:40px; }}
            .poster {{ width:900px; min-height:1100px; background:linear-gradient(135deg,#667eea 0%,#764ba2 30%,#f64f59 60%,#c471ed 80%,#12c2e9 100%); border-radius:32px; overflow:hidden; box-shadow:0 40px 100px rgba(102,126,234,0.5); position:relative; font-family:'Outfit','Noto Sans Telugu',sans-serif; padding:4px; }}
            .inner {{ background:linear-gradient(135deg,rgba(255,255,255,0.12),rgba(255,255,255,0.05)); border-radius:30px; min-height:100%; backdrop-filter:blur(10px); padding:55px; }}
            .header {{ display:flex; align-items:center; gap:28px; margin-bottom:40px; }}
            .logo-wrap {{ width:120px; height:120px; clip-path:polygon(50% 0%,100% 25%,100% 75%,50% 100%,0% 75%,0% 25%); overflow:hidden; background:rgba(255,255,255,0.3); display:flex; align-items:center; justify-content:center; flex-shrink:0; filter:drop-shadow(0 0 20px rgba(255,255,255,0.5)); }}
            .shop-name {{ font-size:62px; font-weight:900; color:white; line-height:1.0; text-shadow:2px 4px 20px rgba(0,0,0,0.3); }}
            .shop-tag {{ display:inline-block; background:rgba(255,255,255,0.2); border:1px solid rgba(255,255,255,0.4); color:white; font-size:14px; font-weight:700; padding:6px 18px; border-radius:50px; margin-top:10px; letter-spacing:2px; text-transform:uppercase; }}
            .festival-pill {{ display:inline-flex; align-items:center; gap:12px; background:rgba(255,255,255,0.15); border:1px solid rgba(255,255,255,0.3); border-radius:50px; padding:12px 28px; margin-bottom:28px; }}
            .festival-pill img {{ width:30px; height:30px; filter:brightness(10); }}
            .festival-pill span {{ font-size:22px; font-weight:700; color:white; }}
            .offer-box {{ background:rgba(255,255,255,0.18); border:1px solid rgba(255,255,255,0.4); border-radius:28px; padding:35px 45px; margin:25px 0; backdrop-filter:blur(30px); box-shadow:0 20px 60px rgba(0,0,0,0.15),inset 0 1px 0 rgba(255,255,255,0.3); position:relative; overflow:hidden; }}
            .offer-box::before {{ content:''; position:absolute; top:-50%; left:-50%; width:200%; height:200%; background:radial-gradient(circle,rgba(255,255,255,0.1) 0%,transparent 60%); }}
            .offer-label {{ font-size:13px; color:rgba(255,255,255,0.6); font-weight:700; letter-spacing:4px; text-transform:uppercase; margin-bottom:10px; }}
            .offer-row {{ display:flex; align-items:center; gap:20px; }}
            .offer-value {{ font-size:70px; font-weight:900; color:white; line-height:1.0; text-shadow:2px 4px 20px rgba(0,0,0,0.2); flex:1; }}
            .offer-badge {{ background:rgba(255,255,255,0.2); border-radius:16px; padding:12px; display:flex; flex-direction:column; align-items:center; gap:6px; }}
            .offer-badge img {{ width:50px; height:50px; opacity:0.6; filter:brightness(10); }}
            .offer-badge span {{ font-size:11px; color:rgba(255,255,255,0.7); font-weight:700; text-transform:uppercase; letter-spacing:1px; }}
            .caption-box {{ background:rgba(255,255,255,0.12); border:1px solid rgba(255,255,255,0.2); border-radius:0 20px 20px 20px; padding:25px 30px; margin:25px 0; position:relative; }}
            .caption-avatar {{ position:absolute; top:-20px; left:10px; width:36px; height:36px; border-radius:50%; background:rgba(255,255,255,0.3); border:2px solid rgba(255,255,255,0.5); display:flex; align-items:center; justify-content:center; font-size:18px; }}
            .caption-text {{ font-size:27px; line-height:1.75; color:rgba(255,255,255,0.95); font-family:'Noto Sans Telugu','Outfit',sans-serif; }}
            .divider {{ height:1px; background:rgba(255,255,255,0.15); margin:28px 0; }}
            .contact-neon {{ display:flex; align-items:center; gap:16px; margin-bottom:16px; background:rgba(255,255,255,0.08); border:1px solid rgba(255,255,255,0.2); border-radius:16px; padding:16px 24px; box-shadow:0 0 20px rgba(255,255,255,0.05); }}
            .contact-icon-glow {{ width:48px; height:48px; border-radius:14px; background:rgba(255,255,255,0.25); border:1px solid rgba(255,255,255,0.4); display:flex; align-items:center; justify-content:center; flex-shrink:0; box-shadow:0 0 15px rgba(255,255,255,0.2); }}
            .contact-icon-glow img {{ width:24px; height:24px; filter:brightness(10); }}
            .contact-info {{ flex:1; }}
            .contact-label {{ font-size:11px; color:rgba(255,255,255,0.5); font-weight:700; letter-spacing:2px; text-transform:uppercase; }}
            .contact-text {{ font-size:26px; font-weight:700; color:white; }}
            .watermark {{ position:absolute; bottom:50px; right:55px; width:130px; height:130px; opacity:0.08; filter:brightness(10); }}
            </style></head><body>
            <div class="poster">
            <div class="inner">
            <div class="header">
            <div class="logo-wrap">{logo_html}</div>
            <div><div class="shop-name">{shop}</div><div class="shop-tag">{shop_type}</div></div>
            </div>
            <div class="festival-pill"><img src="{festival_icon}"><span>{festival} Special</span></div>
            <div class="offer-box">
            <div class="offer-label">✦ Exclusive Offer ✦</div>
            <div class="offer-row">
            <div class="offer-value">{offer}</div>
            <div class="offer-badge"><img src="{shop_icon}"><span>{shop_type}</span></div>
            </div>
            </div>
            <div class="caption-box">
            <div class="caption-avatar">💬</div>
            <div class="caption-text">{result}</div>
            </div>
            <div class="divider"></div>
            <div class="contact-neon">
            <div class="contact-icon-glow"><img src="https://cdn-icons-png.flaticon.com/512/597/597177.png"></div>
            <div class="contact-info"><div class="contact-label">Call Us</div><div class="contact-text">{customer_phone}</div></div>
            </div>
            <div class="contact-neon">
            <div class="contact-icon-glow"><img src="https://cdn-icons-png.flaticon.com/512/684/684908.png"></div>
            <div class="contact-info"><div class="contact-label">Visit Us</div><div class="contact-text">{customer_address}</div></div>
            </div>
            </div>
            <img class="watermark" src="{shop_icon}">
            </div></body></html>"""       