"""
╔══════════════════════════════════════════════════════════════════╗
║        NIGHTLIFE CONCIERGE BKK — Streamlit App                  ║
║        Google Sheets Edition · Thonglor-Ekkamai Focus            ║
╚══════════════════════════════════════════════════════════════════╝

Google Sheet Headers (copy-paste ไปใส่ Row 1 ใน Sheets ได้เลย):
──────────────────────────────────────────────────────────────────
VenueName | Zone | Category | PriceLevel | VibeScore | AgeGroup |
MusicType | InsiderReview | CrowdType | LanguageSupport
──────────────────────────────────────────────────────────────────

PriceLevel: 1=฿  2=฿฿  3=฿฿฿  4=฿฿฿฿
VibeScore : 0–100
"""

import streamlit as st
import pandas as pd
import time

# ─── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Nightlife Concierge BKK",
    page_icon="🌃",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS (ported 1-to-1 from HTML demo) ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

:root{
  --bg:#080B12; --surface:#0D1120; --card:#111827; --border:#1E2A3A;
  --neon:#3B82F6; --neon-glow:rgba(59,130,246,.22); --accent:#06B6D4;
  --text:#E2E8F0; --muted:#64748B; --radius:14px;
}

/* ── Global ── */
html,body,[data-testid="stApp"]{background:var(--bg)!important;color:var(--text)!important;font-family:'DM Sans',sans-serif!important}
h1,h2,h3{font-family:'Syne',sans-serif!important}

/* ── Sidebar ── */
[data-testid="stSidebar"]{background:var(--surface)!important;border-right:1px solid var(--border)!important}
[data-testid="stSidebar"] *{color:var(--text)!important}
[data-testid="stSidebar"] label{font-family:'Syne',sans-serif!important;font-size:.68rem!important;letter-spacing:.13em!important;text-transform:uppercase!important;color:var(--muted)!important}

/* ── Inputs ── */
[data-testid="stTextInput"] input{background:var(--card)!important;border:1px solid var(--border)!important;border-radius:var(--radius)!important;color:var(--text)!important;font-family:'DM Sans',sans-serif!important;font-size:1rem!important;padding:.75rem 1rem!important}
[data-testid="stTextInput"] input:focus{border-color:var(--neon)!important;box-shadow:0 0 0 3px var(--neon-glow)!important}

/* ── Selectbox ── */
[data-testid="stSelectbox"]>div>div{background:var(--card)!important;border:1px solid var(--border)!important;border-radius:var(--radius)!important;color:var(--text)!important}

/* ── Button ── */
.stButton>button{background:var(--neon)!important;color:#fff!important;border:none!important;border-radius:var(--radius)!important;font-family:'Syne',sans-serif!important;font-weight:600!important;letter-spacing:.05em!important;padding:.65rem 1.4rem!important;transition:opacity .2s,box-shadow .2s!important}
.stButton>button:hover{opacity:.83!important;box-shadow:0 0 18px var(--neon-glow)!important}

/* ── Neon divider ── */
.neon-line{height:2px;background:linear-gradient(90deg,transparent,var(--neon),transparent);margin:1.2rem 0}

/* ── Hero ── */
.hero-eyebrow{font-family:'Syne',sans-serif;font-size:.68rem;letter-spacing:.15em;text-transform:uppercase;color:var(--muted);margin-bottom:.5rem}
.hero-title{font-family:'Syne',sans-serif;font-size:2.1rem;font-weight:800;line-height:1.15;color:#fff}
.hero-title span{color:var(--neon)}
.hero-sub{color:var(--muted);font-size:.92rem;margin-top:.5rem}

/* ── Stats ── */
.stat-chip{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:.75rem 1rem;text-align:center}
.stat-num{font-family:'Syne',sans-serif;font-size:1.5rem;font-weight:800;color:var(--neon)}
.stat-lbl{font-size:.68rem;color:var(--muted);text-transform:uppercase;letter-spacing:.08em;margin-top:.15rem}

/* ── Section label ── */
.section-label{font-family:'Syne',sans-serif;font-size:.68rem;letter-spacing:.15em;text-transform:uppercase;color:var(--muted);margin-bottom:.5rem}

/* ── Results badge ── */
.results-header{display:flex;align-items:center;gap:.75rem;margin-bottom:1rem}
.results-title{font-family:'Syne',sans-serif;font-size:1rem;font-weight:700;color:#fff}
.results-badge{font-size:.7rem;color:var(--neon);background:rgba(59,130,246,.12);border:1px solid rgba(59,130,246,.28);border-radius:999px;padding:.15rem .6rem}

/* ── Venue Card ── */
.venue-card{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:1.2rem 1.4rem;margin-bottom:.9rem;position:relative;transition:border-color .2s,box-shadow .2s}
.venue-card:hover{border-color:var(--neon);box-shadow:0 0 22px var(--neon-glow)}
.match-badge{position:absolute;top:.9rem;right:1rem;background:linear-gradient(135deg,#1D4ED8,#0EA5E9);color:#fff;font-family:'Syne',sans-serif;font-weight:700;font-size:.75rem;padding:.2rem .6rem;border-radius:999px;letter-spacing:.03em}
.next-badge{position:absolute;top:.9rem;right:1rem;background:linear-gradient(135deg,#065f46,#0d9488);color:#fff;font-family:'Syne',sans-serif;font-weight:700;font-size:.75rem;padding:.2rem .6rem;border-radius:999px}
.venue-name{font-family:'Syne',sans-serif;font-size:1.08rem;font-weight:700;color:#fff;margin-bottom:.2rem;padding-right:5rem}
.venue-meta{font-size:.8rem;color:var(--muted);margin-bottom:.55rem}
.tag{display:inline-block;background:rgba(59,130,246,.1);border:1px solid rgba(59,130,246,.28);color:var(--accent);font-size:.68rem;padding:.12rem .5rem;border-radius:999px;margin-right:.3rem;font-family:'Syne',sans-serif;letter-spacing:.04em}
.price-tag{display:inline-block;background:rgba(245,158,11,.08);border:1px solid rgba(245,158,11,.3);color:#F59E0B;font-size:.68rem;padding:.12rem .5rem;border-radius:999px;margin-right:.3rem;font-family:'Syne',sans-serif}
.vibe-bar-wrap{margin-top:.7rem}
.vibe-label{font-size:.67rem;color:var(--muted);font-family:'Syne',sans-serif;letter-spacing:.06em;text-transform:uppercase;margin-bottom:.25rem}
.vibe-bar-bg{background:var(--border);border-radius:999px;height:4px;overflow:hidden}
.vibe-bar-fill{height:4px;border-radius:999px;background:linear-gradient(90deg,var(--neon),var(--accent))}
.insider-quote{font-style:italic;color:#94A3B8;font-size:.82rem;border-left:2px solid var(--neon);padding-left:.7rem;margin-top:.7rem;line-height:1.6}

/* ── Next spot section ── */
.next-section-title{font-family:'Syne',sans-serif;font-size:1rem;font-weight:700;color:#fff;margin-bottom:.3rem}
.next-section-sub{font-size:.82rem;color:var(--muted);margin-bottom:1rem}
.next-arrow{text-align:center;font-size:1.6rem;color:var(--neon);padding-top:1.8rem}

/* ── Warning / info ── */
.warn-box{background:rgba(245,158,11,.07);border:1px solid rgba(245,158,11,.25);border-radius:var(--radius);padding:.9rem 1.1rem;font-size:.85rem;color:#FCD34D;margin:.5rem 0}
.info-box{background:rgba(59,130,246,.07);border:1px solid rgba(59,130,246,.2);border-radius:var(--radius);padding:.9rem 1.1rem;font-size:.85rem;color:#93C5FD;margin:.5rem 0}

/* ── Footer ── */
.app-footer{text-align:center;font-size:.68rem;color:#1E2A3A;padding:1.5rem 0;border-top:1px solid var(--border);margin-top:2rem}

/* ── Spinner text ── */
[data-testid="stSpinner"] p{font-family:'Syne',sans-serif!important;font-size:.82rem!important;letter-spacing:.08em!important}

/* ── Expander ── */
[data-testid="stExpander"]{background:var(--card)!important;border:1px solid var(--border)!important;border-radius:var(--radius)!important}
[data-testid="stExpander"] summary{color:var(--muted)!important;font-family:'Syne',sans-serif!important;font-size:.8rem!important}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
#  GOOGLE SHEETS SCHEMA  (แสดงใน sidebar เป็น guide)
# ══════════════════════════════════════════════════════════════════
SHEET_COLUMNS = [
    "VenueName", "Zone", "Category", "PriceLevel",
    "VibeScore", "AgeGroup", "MusicType",
    "InsiderReview", "CrowdType", "LanguageSupport",
]

PRICE_MAP = {1: "฿", 2: "฿฿", 3: "฿฿฿", 4: "฿฿฿฿"}

BUDGET_MAX = {
    "Any": 4,
    "Budget (฿)": 1,
    "Mid-range (฿฿)": 2,
    "Premium (฿฿฿)": 3,
    "Luxury (฿฿฿฿)": 4,
}


# ══════════════════════════════════════════════════════════════════
#  DATA LAYER — Google Sheets (with fallback seed data)
# ══════════════════════════════════════════════════════════════════
@st.cache_data(ttl=180)   # refresh every 3 min
def load_venues() -> pd.DataFrame:
    """
    ── PRODUCTION ──────────────────────────────────────────────────
    Uncomment the block below and fill in your Sheet URL.
    ใน secrets.toml ให้เพิ่ม:

        [connections.gsheets]
        spreadsheet = "https://docs.google.com/spreadsheets/d/YOUR_ID"
        type = "public"          # หรือ "service_account" ถ้า private

    แล้ว run:  pip install streamlit-gsheets-connection
    ────────────────────────────────────────────────────────────────
    from streamlit_gsheets import GSheetsConnection
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(
        worksheet="VenueMasterData",   # ชื่อ sheet tab
        usecols=SHEET_COLUMNS,
        ttl=180,
    )
    df["PriceLevel"] = pd.to_numeric(df["PriceLevel"], errors="coerce").fillna(2).astype(int)
    df["VibeScore"]  = pd.to_numeric(df["VibeScore"],  errors="coerce").fillna(80).astype(int)
    return df
    ────────────────────────────────────────────────────────────────
    """
    # ── SEED DATA (จาก PDF Thonglor-Ekkamai Edition + venues เดิม) ──
    data = {
        "VenueName": [
            "TUBA Design Furniture & Restaurant",
            "Soho Hospitality (Soho House)",
            "Tichuca Rooftop Bar",
            "The Iron Fairies",
            "BEAM",
            "Rabbit Hole",
            "Cassette Music Bar",
            "Terra Thonglor 10",
            "Find The Locker Room",
            "BKK Social Club",
            "Havana Social",
            "Tropic City",
            "Octave Rooftop",
            "Sing Sing Theater",
        ],
        "Zone": [
            "Ekkamai", "Sukhumvit", "Thonglor", "Thonglor",
            "Ekkamai", "Thonglor", "Ekkamai", "Thonglor",
            "Thonglor", "Silom", "Sukhumvit", "Riverside",
            "Sukhumvit", "Chinatown",
        ],
        "Category": [
            "Artsy Bar & Resto", "Members Club / Elite Lounge",
            "Rooftop Bar", "Hidden Bar",
            "Club", "Speakeasy",
            "Chill Bar", "Lounge / Club",
            "Hidden Bar", "Rooftop Bar",
            "Speakeasy", "Tropical Bar",
            "Rooftop Bar", "Club",
        ],
        "PriceLevel": [2, 4, 4, 3, 2, 3, 2, 3, 3, 3, 3, 3, 3, 3],
        "VibeScore":  [92, 95, 96, 94, 88, 91, 85, 87, 89, 92, 88, 91, 89, 90],
        "AgeGroup":   [
            "21-45", "25-45", "21-35", "25-38",
            "21-30", "25-40", "21-35", "25-35",
            "28-40", "25-35", "21-35", "25-38",
            "25-35", "21-35",
        ],
        "MusicType": [
            "Easy Listening / Retro", "Curated Playlists / Vinyl",
            "House / EDM", "Live Jazz",
            "Techno / Electronic", "Jazz / Deep House",
            "90s Thai Pop", "Live Band / Pop",
            "Classic Cocktails", "Jazz / House",
            "Latin / Salsa", "Chill / Ambient",
            "Commercial / Pop", "Hip-Hop / RnB",
        ],
        "InsiderReview": [
            "ตำนานย่านเอกมัย ของตกแต่งสไตล์วินเทจเยอะมาก อาหารอร่อย ค็อกเทลแก้วใหญ่สะใจ เหมาะกับกลุ่มเพื่อนหรือมานั่งคุยยาวๆ",
            "สุดยอดความ Exclusive แหล่งรวม Creative และคนเทสดีระดับ High-end บรรยากาศหรูหราแต่ดูอบอุ่น มีความเป็นส่วนตัวสูงมาก",
            "ต้นไม้ไฟ LED คือ landmark ถ่ายรูปสวยมาก สาวเยอะ หนุ่มสาวออฟฟิศหน้าตาดีมารวมตัวกันที่นี่",
            "Vibe เหมือนหลุดไปในโลกแฟนตาซี มืดๆ ขรึมๆ แต่เทสดีมาก เหมาะกับคนชอบความต่าง",
            "ถ้าชอบเพลงดีๆ ระบบเสียงระดับโลก ต้องมา แสงสีล้ำหน้ากว่าคลับอื่นในย่านนี้เยอะ",
            "บาร์ลับที่คนโสดมานั่งที่เคาน์เตอร์แล้วไม่เขิน บาร์เทนเดอร์เก่ง คุยสนุก ค็อกเทลคุณภาพเน้นๆ",
            "สาย Retro ต้องจัด เพลงไทยยุค 90 ตลอดคืน บรรยากาศสนุกสนาน ไม่ต้องพิธีรีตองเยอะ",
            "แหล่งรวมคนทำงานย่านทองหล่อ ดนตรีสดดีมาก คนแน่นเกือบทุกคืน ใครชอบฟีลคึกคักต้องที่นี่",
            "ทางเข้าลึกลับแต่คุ้มค่าที่หาเจอ บรรยากาศส่วนตัวสูงมาก เหมาะกับการมาคุยกับคนรู้ใจหรือเพื่อนสนิท",
            "ทิวทัศน์กรุงเทพฯ ยามค่ำคืนสุดอลังการ เหมาะกับ first date หรือคืนพิเศษ ราคาโอเคถ้าเทียบกับวิว",
            "บรรยากาศเหมือนคิวบา 1950s เพลงลาตินตลอดคืน บาร์เทนเดอร์เก่งมาก signature cocktail ห้ามพลาด",
            "Tropical cocktail bar ที่ creative มาก Bartender award-winning ทุกแก้วเหมือนงานศิลปะ",
            "Rooftop ที่ดีที่สุดสำหรับ panoramic view of Bangkok แนะนำมาก",
            "Club ที่เก่าแก่ที่สุดและดีที่สุดในย่าน Chinatown ถ้าอยากปาร์ตี้หนักมาที่นี่",
        ],
        "CrowdType": [
            "Creative & Chill", "Elite & Exclusive", "Trendy & Photogenic",
            "Indie & Artsy", "Techno Heads", "Solo & Social",
            "Retro Lovers", "Working Crowd", "Intimate & Selective",
            "Chill & Sophisticated", "Speakeasy Lovers", "Tropical Chill",
            "Mixed Crowd", "Party Crowd",
        ],
        "LanguageSupport": [
            "EN/TH", "EN/TH/FR", "EN/TH", "EN/TH",
            "EN/TH", "EN/TH", "TH", "EN/TH",
            "EN/TH", "EN/TH", "EN/TH/ES", "EN/TH/JP",
            "EN/TH", "EN/TH",
        ],
    }
    return pd.DataFrame(data)


# ══════════════════════════════════════════════════════════════════
#  MATCHING ENGINE  (same weights as HTML demo)
# ══════════════════════════════════════════════════════════════════
def compute_match(row: pd.Series, query: str, budget: str, zone: str) -> float:
    """40% User Vibe · 30% Crowd Quality · 30% Location"""
    vibe_norm = row["VibeScore"] / 100.0

    keywords  = [k for k in query.lower().split() if len(k) > 1]
    haystack  = f"{row['Category']} {row['CrowdType']} {row['MusicType']} {row['InsiderReview']}".lower()
    kw_hit    = (sum(1 for k in keywords if k in haystack) / len(keywords)) if keywords else 0.5

    user_vibe  = 0.6 * vibe_norm + 0.4 * kw_hit       # 40%
    crowd_q    = vibe_norm                              # 30%
    loc_match  = 1.0 if (zone == "All Zones" or row["Zone"] == zone) else 0.5  # 30%

    max_price  = BUDGET_MAX.get(budget, 4)
    budget_ok  = 1.0 if row["PriceLevel"] <= max_price else 0.3

    score = (0.40 * user_vibe + 0.30 * crowd_q + 0.30 * loc_match) * budget_ok
    return round(score * 100, 1)


# ══════════════════════════════════════════════════════════════════
#  LANGUAGE BRIDGE
# ══════════════════════════════════════════════════════════════════
def translate_review(text: str, lang: str) -> str:
    """
    Production → เรียก Claude API:
        import anthropic
        client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
        msg = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=256,
            messages=[{"role":"user","content":f"Translate to {lang}: {text}"}]
        )
        return msg.content[0].text
    """
    prefixes = {"EN": "", "TH": "[🇹🇭] ", "ZH": "[🇨🇳] ", "JA": "[🇯🇵] "}
    return prefixes.get(lang, "") + text


# ══════════════════════════════════════════════════════════════════
#  CARD RENDERER
# ══════════════════════════════════════════════════════════════════
def render_card(row: pd.Series, score: float, lang: str, badge_style: str = "match"):
    price_str = PRICE_MAP.get(int(row["PriceLevel"]), "฿฿")
    review    = translate_review(row["InsiderReview"], lang)
    vibe_w    = int(row["VibeScore"])

    if badge_style == "next":
        badge = '<span class="next-badge">Next Stop ✦</span>'
    else:
        badge = f'<span class="match-badge">✦ {score}% Match</span>'

    st.markdown(f"""
    <div class="venue-card">
      {badge}
      <div class="venue-name">{row['VenueName']}</div>
      <div class="venue-meta">📍 {row['Zone']} &nbsp;·&nbsp; 🎵 {row['MusicType']}</div>
      <span class="tag">{row['Category']}</span>
      <span class="tag">{row['CrowdType']}</span>
      <span class="tag">{row['AgeGroup']}</span>
      <span class="price-tag">{price_str}</span>
      <div class="vibe-bar-wrap">
        <div class="vibe-label">Vibe Score — {vibe_w}/100</div>
        <div class="vibe-bar-bg">
          <div class="vibe-bar-fill" style="width:{vibe_w}%"></div>
        </div>
      </div>
      <div class="insider-quote">💬 {review}</div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="padding:.5rem 0 .75rem">
      <div style="font-family:'Syne',sans-serif;font-size:1.25rem;font-weight:800;color:#fff">🌃 Concierge</div>
      <div style="font-size:.68rem;color:#3B82F6;letter-spacing:.12em;text-transform:uppercase;margin-top:.1rem">Bangkok Nightlife AI</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="neon-line"></div>', unsafe_allow_html=True)

    # ── Filters ──
    st.markdown('<div class="section-label">Zone</div>', unsafe_allow_html=True)
    zone_filter = st.selectbox("zone", [
        "All Zones", "Thonglor", "Ekkamai", "Sukhumvit",
        "Silom", "Sathorn", "Chinatown", "Riverside",
    ], label_visibility="collapsed")

    st.markdown('<div class="section-label" style="margin-top:.9rem">Budget</div>', unsafe_allow_html=True)
    budget_filter = st.selectbox("budget", [
        "Any", "Budget (฿)", "Mid-range (฿฿)", "Premium (฿฿฿)", "Luxury (฿฿฿฿)",
    ], label_visibility="collapsed")

    st.markdown('<div class="section-label" style="margin-top:.9rem">Category</div>', unsafe_allow_html=True)
    cat_filter = st.multiselect("cat", [
        "Rooftop Bar", "Speakeasy", "Club", "Hidden Bar",
        "Lounge / Club", "Artsy Bar & Resto", "Chill Bar",
        "Members Club / Elite Lounge", "Tropical Bar",
    ], default=[], label_visibility="collapsed")

    st.markdown('<div class="section-label" style="margin-top:.9rem">Music Vibe</div>', unsafe_allow_html=True)
    music_filter = st.multiselect("music", [
        "Jazz / House", "Live Jazz", "Techno / Electronic",
        "House / EDM", "Latin / Salsa", "90s Thai Pop",
        "Live Band / Pop", "Easy Listening / Retro",
        "Chill / Ambient", "Hip-Hop / RnB",
    ], default=[], label_visibility="collapsed")

    st.markdown('<div class="neon-line"></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-label">Language Bridge 🌐</div>', unsafe_allow_html=True)
    lang = st.selectbox("lang", ["EN", "TH", "ZH", "JA"], label_visibility="collapsed")

    st.markdown('<div class="neon-line"></div>', unsafe_allow_html=True)

    # ── Google Sheets Schema Guide ──
    st.markdown("""
    <div style="font-family:'Syne',sans-serif;font-size:.65rem;letter-spacing:.1em;text-transform:uppercase;color:#3B82F6;margin-bottom:.5rem">
      📋 Sheets Schema
    </div>
    """, unsafe_allow_html=True)
    schema_df = pd.DataFrame({
        "Column": SHEET_COLUMNS,
        "Type":   ["text","text","text","int 1-4","int 0-100",
                   "text","text","text","text","text"],
    })
    st.dataframe(
        schema_df,
        hide_index=True,
        use_container_width=True,
        height=210,
    )

    st.markdown("""
    <div style="font-size:.68rem;color:#1E3A5F;line-height:1.7;margin-top:.75rem">
      Data · Urban Collective BKK<br>
      Locals 21–40 · Thonglor-Ekkamai Ed.<br>
      🔒 PDPA Compliant
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
#  LOAD DATA
# ══════════════════════════════════════════════════════════════════
df = load_venues()

# ── Data health check ──
missing_cols = [c for c in SHEET_COLUMNS if c not in df.columns]
if missing_cols:
    st.markdown(f"""
    <div class="warn-box">
      ⚠️ Google Sheet missing columns: <strong>{', '.join(missing_cols)}</strong><br>
      ตรวจสอบ Header row ใน Sheets ให้ตรงกับ Schema ด้านซ้ายครับ
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  HERO
# ══════════════════════════════════════════════════════════════════
st.markdown("""
<div style="padding:1.5rem 0 .5rem">
  <div class="hero-eyebrow">AI-Powered Nightlife Discovery</div>
  <div class="hero-title">Find Your<br><span>Perfect Night</span> in BKK</div>
  <div class="hero-sub">Matched by locals. Curated by AI. Built for explorers.</div>
</div>
""", unsafe_allow_html=True)
st.markdown('<div class="neon-line"></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  STATS ROW
# ══════════════════════════════════════════════════════════════════
total_v  = len(df)
zones_n  = df["Zone"].nunique()
avg_vibe = int(df["VibeScore"].mean())
avg_price_sym = PRICE_MAP.get(round(df["PriceLevel"].mean()), "฿฿฿")

c1, c2, c3, c4 = st.columns(4)
for col, num, lbl in zip(
    [c1, c2, c3, c4],
    [total_v, zones_n, avg_vibe, avg_price_sym],
    ["Venues", "Zones", "Avg Vibe", "Avg Price"],
):
    col.markdown(f"""
    <div class="stat-chip">
      <div class="stat-num">{num}</div>
      <div class="stat-lbl">{lbl}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  VIBE SEARCH
# ══════════════════════════════════════════════════════════════════
st.markdown('<div class="section-label">✦ Vibe Search</div>', unsafe_allow_html=True)
col_s, col_b = st.columns([5, 1])
with col_s:
    vibe_query = st.text_input(
        "vibe",
        placeholder="e.g. rooftop chill jazz · hidden speakeasy · techno underground · retro Thai pop ...",
        label_visibility="collapsed",
    )
with col_b:
    search_btn = st.button("Match →", use_container_width=True)

st.markdown('<div class="neon-line"></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  FILTER + SCORE
# ══════════════════════════════════════════════════════════════════
filtered = df.copy()
if cat_filter:
    filtered = filtered[filtered["Category"].isin(cat_filter)]
if music_filter:
    filtered = filtered[filtered["MusicType"].isin(music_filter)]
if zone_filter != "All Zones":
    filtered = filtered[filtered["Zone"] == zone_filter]

query = vibe_query.strip() or "chill bar"

if search_btn or vibe_query:
    with st.spinner("🔍 AI กำลัง match vibe ให้..."):
        time.sleep(0.4)

filtered = filtered.copy()
filtered["_score"] = filtered.apply(
    lambda r: compute_match(r, query, budget_filter, zone_filter), axis=1
)
filtered = filtered.sort_values("_score", ascending=False).reset_index(drop=True)

top3 = filtered.head(3)
rest = filtered.iloc[3:]

# ── Results header ──
st.markdown(f"""
<div class="results-header">
  <span class="results-title">Top Matches</span>
  <span class="results-badge">{len(filtered)} venues found</span>
</div>
""", unsafe_allow_html=True)

if top3.empty:
    st.markdown('<div class="info-box">ℹ️ ไม่เจอร้านที่ตรง ลองปรับ filter หรือเปลี่ยน Vibe Search ดูครับ</div>',
                unsafe_allow_html=True)
else:
    for _, row in top3.iterrows():
        render_card(row, row["_score"], lang)

# ── More venues ──
if not rest.empty:
    with st.expander(f"▾ แสดง {len(rest)} ร้านอื่นเพิ่มเติม"):
        for _, row in rest.iterrows():
            render_card(row, row["_score"], lang)

st.markdown('<div class="neon-line"></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  WHERE TO GO NEXT
# ══════════════════════════════════════════════════════════════════
st.markdown("""
<div class="next-section-title">🗺️ Where to Go Next?</div>
<div class="next-section-sub">เลือกร้านที่กำลังนั่งอยู่ → AI แนะนำ next stop ในย่านเดียวกันให้เลย</div>
""", unsafe_allow_html=True)

col_cur, col_arr, col_nxt = st.columns([2, 0.25, 2])
with col_cur:
    current = st.selectbox(
        "You're at:",
        ["— เลือกร้านที่อยู่ตอนนี้ —"] + df["VenueName"].tolist(),
    )
with col_arr:
    st.markdown('<div class="next-arrow">→</div>', unsafe_allow_html=True)
with col_nxt:
    if current != "— เลือกร้านที่อยู่ตอนนี้ —":
        cur_row   = df[df["VenueName"] == current].iloc[0]
        same_zone = df[(df["Zone"] == cur_row["Zone"]) & (df["VenueName"] != current)]
        pool      = same_zone if not same_zone.empty else df[df["VenueName"] != current]
        # Score next candidates too
        pool = pool.copy()
        pool["_score"] = pool.apply(
            lambda r: compute_match(r, query, budget_filter, zone_filter), axis=1
        )
        next_row = pool.sort_values("_score", ascending=False).iloc[0]
        render_card(next_row, next_row["_score"], lang, badge_style="next")

# ══════════════════════════════════════════════════════════════════
#  FOOTER
# ══════════════════════════════════════════════════════════════════
st.markdown('<div class="neon-line"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="app-footer">
  Nightlife Concierge BKK · Thonglor-Ekkamai Edition · Powered by Urban Collective<br>
  PDPA Compliant · Data encrypted · Locals aged 21–40
</div>
""", unsafe_allow_html=True)
