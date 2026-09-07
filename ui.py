import streamlit as st

PALETTES = {
    "Dark": {
        "bg":"#111214","surface":"#17191d","surface2":"#1d2025","surface3":"#242830","text":"#f5f7fb","muted":"#9aa3b2",
        "border":"#2b3038","border2":"#39404b","accent":"#5b8cff","accent2":"#8c6cff","accent3":"#70d6c3","success":"#6dd4a8",
        "warning":"#f0c66d","danger":"#ef7c7c","shadow":"rgba(0,0,0,.28)","input":"#15171b",
    },
    "Light": {
        "bg":"#f4f5f6","surface":"#ffffff","surface2":"#f8f8f9","surface3":"#eff1f4","text":"#17191d","muted":"#717987",
        "border":"#e2e5e9","border2":"#d4d8de","accent":"#4d7df3","accent2":"#8668ee","accent3":"#5ebead","success":"#3d9b76",
        "warning":"#b88931","danger":"#c75c5c","shadow":"rgba(31,39,55,.08)","input":"#ffffff",
    },
}


def apply_theme(mode="Dark"):
    p = PALETTES.get(mode, PALETTES["Dark"])
    st.markdown(f"""
    <style>
      :root{{--bg:{p['bg']};--surface:{p['surface']};--surface2:{p['surface2']};--surface3:{p['surface3']};--text:{p['text']};--muted:{p['muted']};--border:{p['border']};--border2:{p['border2']};--accent:{p['accent']};--accent2:{p['accent2']};--accent3:{p['accent3']};--success:{p['success']};--warning:{p['warning']};--danger:{p['danger']};--shadow:{p['shadow']};--input:{p['input']};}}
      html,body,[data-testid="stAppViewContainer"],.stApp{{background:var(--bg)!important;color:var(--text)!important;}}
      [data-testid="stHeader"]{{background:transparent!important;}}
      .block-container{{max-width:1440px;padding-top:1.55rem;padding-bottom:4rem;padding-left:2rem;padding-right:2rem;}}
      h1,h2,h3,h4,h5,p,span,label,div{{font-family:Inter,ui-sans-serif,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;}}
      h1,h2,h3,h4,h5{{letter-spacing:-.035em;color:var(--text)!important;}}
      p,li,label,[data-testid="stCaptionContainer"]{{color:var(--text);}}
      [data-testid="stSidebar"]{{background:linear-gradient(180deg,color-mix(in srgb,var(--surface) 96%,var(--accent) 4%),var(--surface2))!important;border-right:1px solid var(--border);}}
      [data-testid="stSidebar"] > div{{padding-top:1.1rem;}}
      [data-testid="stSidebar"] .stRadio > div{{gap:.28rem;}}
      [data-testid="stSidebar"] .stRadio label{{padding:.66rem .72rem;border-radius:12px;transition:.15s ease;border:1px solid transparent;}}
      [data-testid="stSidebar"] .stRadio label:hover{{background:var(--surface3);border-color:var(--border);}}
      [data-testid="stSidebar"] .stRadio label:has(input:checked){{background:linear-gradient(135deg,color-mix(in srgb,var(--accent) 18%,var(--surface3)),color-mix(in srgb,var(--accent2) 11%,var(--surface3)));border-color:color-mix(in srgb,var(--accent) 32%,var(--border2));box-shadow:0 8px 22px color-mix(in srgb,var(--accent) 10%,transparent);}}
      [data-testid="stSidebar"] .stRadio label p{{font-weight:720!important;font-size:.91rem!important;}}
      .brand{{padding:.45rem .3rem 1rem .3rem;}}
      .brand-mark{{width:40px;height:40px;border-radius:13px;display:grid;place-items:center;background:linear-gradient(135deg,var(--accent),var(--accent2));color:white;font-weight:900;font-size:1.06rem;box-shadow:0 10px 28px color-mix(in srgb,var(--accent) 24%,transparent);}}
      .brand-title{{font-size:1rem;font-weight:850;letter-spacing:-.03em;margin-top:.7rem;}}
      .brand-sub{{font-size:.73rem;color:var(--muted)!important;margin-top:.1rem;}}
      .hero-v13{{position:relative;overflow:hidden;padding:1.35rem 1.45rem;border-radius:24px;border:1px solid var(--border);background:linear-gradient(135deg,color-mix(in srgb,var(--surface) 92%,var(--accent) 8%),color-mix(in srgb,var(--surface2) 90%,var(--accent2) 10%));box-shadow:0 24px 70px var(--shadow);margin-bottom:1.25rem;}}
      .hero-v13:after{{content:"";position:absolute;width:300px;height:300px;border-radius:50%;right:-100px;top:-150px;background:radial-gradient(circle,color-mix(in srgb,var(--accent3) 28%,transparent),transparent 70%);}}
      .hero-kicker{{font-size:.72rem;font-weight:850;letter-spacing:.13em;text-transform:uppercase;color:var(--accent3)!important;}}
      .hero-v13 h1{{font-size:2.45rem;margin:.22rem 0 .3rem;line-height:1.0;}}
      .hero-v13 p{{max-width:850px;color:var(--muted)!important;margin:0;font-size:1rem;}}
      .hero-chip{{display:inline-flex;margin-top:.8rem;margin-right:.4rem;padding:.3rem .58rem;border-radius:999px;background:var(--surface3);border:1px solid var(--border2);font-size:.72rem;font-weight:760;}}
      .metric-card,.panel,.pipeline-card,.goal-card,.credential-card{{background:linear-gradient(180deg,var(--surface),color-mix(in srgb,var(--surface2) 93%,transparent));border:1px solid var(--border);border-radius:18px;box-shadow:0 10px 32px color-mix(in srgb,var(--shadow) 58%,transparent);}}
      .metric-card{{padding:1rem 1.05rem;min-height:106px;}}
      .metric-label{{font-size:.69rem;font-weight:850;text-transform:uppercase;letter-spacing:.1em;color:var(--muted)!important;}}
      .metric-value{{font-size:1.7rem;font-weight:860;letter-spacing:-.045em;margin-top:.18rem;}}
      .metric-sub{{font-size:.75rem;color:var(--muted)!important;margin-top:.12rem;}}
      .goal-card{{padding:1.1rem 1.15rem;}}
      .goal-head{{display:flex;justify-content:space-between;align-items:center;gap:.5rem;}}
      .goal-title{{font-weight:820;font-size:1.02rem;}}
      .goal-value{{font-size:1.85rem;font-weight:880;letter-spacing:-.04em;margin:.4rem 0 .25rem;}}
      .goal-track{{height:9px;background:var(--surface3);border-radius:999px;overflow:hidden;border:1px solid var(--border);}}
      .goal-fill{{height:100%;background:linear-gradient(90deg,var(--accent),var(--accent2),var(--accent3));border-radius:999px;}}
      .goal-foot{{font-size:.74rem;color:var(--muted)!important;margin-top:.45rem;}}
      .section-banner{{display:flex;align-items:center;justify-content:space-between;gap:1rem;margin:.25rem 0 .85rem;padding:.9rem 1rem;border-radius:15px;border:1px solid var(--border);background:var(--surface);}}
      .section-banner-title{{font-size:1rem;font-weight:820;}}
      .section-banner-sub{{color:var(--muted)!important;font-size:.78rem;margin-top:.1rem;}}
      .status-pill{{display:inline-flex;border-radius:999px;padding:.25rem .5rem;background:var(--surface3);border:1px solid var(--border2);font-size:.7rem;font-weight:770;white-space:nowrap;}}
      .pipeline-card{{padding:.75rem .82rem;min-height:84px;position:relative;overflow:hidden;}}
      .pipeline-card:before{{content:"";position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,var(--accent),var(--accent2),var(--accent3));}}
      .pipeline-label{{color:var(--muted)!important;font-size:.66rem;font-weight:830;letter-spacing:.08em;text-transform:uppercase;}}
      .pipeline-count{{font-size:1.45rem;font-weight:850;margin-top:.16rem;}}
      .soft-note{{border-left:3px solid var(--accent);padding:.7rem .85rem;background:var(--surface2);border-radius:0 11px 11px 0;}}
      .calendar-grid{{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:.45rem;}}
      .calendar-day{{min-height:100px;border:1px solid var(--border);border-radius:14px;padding:.55rem;background:var(--surface);}}
      .calendar-num{{font-weight:800;font-size:.8rem;margin-bottom:.35rem;}}
      .calendar-event{{font-size:.67rem;padding:.22rem .35rem;border-radius:8px;background:color-mix(in srgb,var(--accent) 13%,var(--surface3));margin:.18rem 0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}}
      div[data-baseweb="input"] > div,div[data-baseweb="base-input"],div[data-baseweb="select"] > div,div[data-baseweb="textarea"] > div,[data-testid="stTextInputRootElement"],[data-testid="stNumberInputContainer"]{{background:var(--input)!important;border-color:var(--border)!important;border-radius:12px!important;}}
      input,textarea,select,div[data-baseweb="select"] input{{color:var(--text)!important;-webkit-text-fill-color:var(--text)!important;background:var(--input)!important;}}
      .stButton>button,.stDownloadButton>button{{border-radius:12px!important;font-weight:740!important;min-height:2.45rem;border-width:1px!important;transition:.14s ease!important;}}
      .stButton>button:hover,.stDownloadButton>button:hover{{transform:translateY(-1px);box-shadow:0 8px 22px color-mix(in srgb,var(--shadow) 60%,transparent);}}
      .stButton>button[kind="primary"]{{background:linear-gradient(135deg,var(--accent),var(--accent2))!important;color:#fff!important;border-color:transparent!important;}}
      div[data-testid="stExpander"],div[data-testid="stVerticalBlockBorderWrapper"]>div{{background:var(--surface)!important;border:1px solid var(--border)!important;border-radius:15px!important;}}
      [data-testid="stProgress"]>div>div>div{{background:linear-gradient(90deg,var(--accent),var(--accent2),var(--accent3))!important;}}
      [data-testid="stAlert"]{{border-radius:12px!important;}}
      hr{{border-color:var(--border)!important;}}
      @media(max-width:900px){{.block-container{{padding-left:.9rem;padding-right:.9rem;}}.hero-v13 h1{{font-size:1.9rem;}}}}
    </style>
    """, unsafe_allow_html=True)


def sidebar_nav(default="Home"):
    st.sidebar.markdown('<div class="brand"><div class="brand-mark">IC</div><div class="brand-title">Internship Command Center</div><div class="brand-sub">V13 · Career operating system</div></div>', unsafe_allow_html=True)
    options = [
        "⌂  Home", "✦  Discover", "▣  Applications", "□  Calendar",
        "▤  Resume Studio", "◈  ATS Lab", "◆  Credentials & Honors",
        "◇  Recruiters", "◉  Profile & Info", "⌁  Application Profile",
        "↗  Connections", "◈  AI & Budget", "⚙  Sources",
    ]
    clean_default = next((x for x in options if default in x), options[0])
    selected = st.sidebar.radio("Navigation", options, index=options.index(clean_default), label_visibility="collapsed")
    return selected.split("  ", 1)[1] if "  " in selected else selected


def hero():
    st.markdown('''<div class="hero-v13"><div class="hero-kicker">V13 · Career operating system</div><h1>Build momentum. Ship stronger applications.</h1><p>Discover internships, prioritize the strongest matches, refine ATS-safe materials, grow your credential portfolio, and keep every next action visible.</p><span class="hero-chip">Daily application goals</span><span class="hero-chip">Credential tracker</span><span class="hero-chip">ATS Lab</span><span class="hero-chip">Human-in-the-loop</span></div>''', unsafe_allow_html=True)


def metric_card(label, value, sub=""):
    st.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{value}</div><div class="metric-sub">{sub}</div></div>', unsafe_allow_html=True)


def goal_card(title, current, goal, foot=""):
    pct = min(100, round(100 * current / max(1, goal)))
    st.markdown(f'<div class="goal-card"><div class="goal-head"><div class="goal-title">{title}</div><span class="status-pill">{pct}%</span></div><div class="goal-value">{current} / {goal}</div><div class="goal-track"><div class="goal-fill" style="width:{pct}%"></div></div><div class="goal-foot">{foot}</div></div>', unsafe_allow_html=True)


def section_banner(title, subtitle="", status=""):
    status_html = f'<span class="status-pill">{status}</span>' if status else ""
    st.markdown(f'<div class="section-banner"><div><div class="section-banner-title">{title}</div><div class="section-banner-sub">{subtitle}</div></div>{status_html}</div>', unsafe_allow_html=True)
