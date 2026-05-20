import streamlit as st
import pickle

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Signal Guard · Spam Detector",
    page_icon="🛡️",
    layout="centered",
)

# ── CSS + animations ───────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;800&display=swap');

/* ── Reset & base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #030712 !important;
    color: #e2e8f0 !important;
    font-family: 'Syne', sans-serif !important;
}

/* ── Animated grid background ── */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(0,255,200,.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,255,200,.04) 1px, transparent 1px);
    background-size: 48px 48px;
    animation: gridScroll 20s linear infinite;
    pointer-events: none;
    z-index: 0;
}

@keyframes gridScroll {
    0%   { transform: translateY(0); }
    100% { transform: translateY(48px); }
}

/* ── Floating orbs ── */
[data-testid="stAppViewContainer"]::after {
    content: '';
    position: fixed;
    width: 520px; height: 520px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(0,255,180,.07) 0%, transparent 70%);
    top: -120px; right: -120px;
    animation: orbFloat 8s ease-in-out infinite alternate;
    pointer-events: none;
    z-index: 0;
}

@keyframes orbFloat {
    from { transform: translate(0,0) scale(1); }
    to   { transform: translate(-40px, 60px) scale(1.1); }
}

/* ── Main content wrapper ── */
[data-testid="stMain"] > div {
    position: relative;
    z-index: 1;
}

/* ── Block container centering ── */
.block-container {
    max-width: 720px !important;
    padding: 3rem 2rem 4rem !important;
}

/* ── Header section ── */
.sg-header {
    text-align: center;
    padding: 2.5rem 0 2rem;
    animation: fadeSlideDown .8s cubic-bezier(.16,1,.3,1) both;
}

.sg-badge {
    display: inline-flex;
    align-items: center;
    gap: .45rem;
    background: rgba(0,255,180,.08);
    border: 1px solid rgba(0,255,180,.25);
    color: #00ffb4;
    font-family: 'Space Mono', monospace;
    font-size: .7rem;
    letter-spacing: .12em;
    padding: .35rem .85rem;
    border-radius: 999px;
    margin-bottom: 1.25rem;
    text-transform: uppercase;
}

.sg-badge span { animation: blink 1.4s step-end infinite; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0} }

.sg-title {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: clamp(2.2rem, 5vw, 3.2rem);
    line-height: 1.1;
    background: linear-gradient(135deg, #ffffff 30%, #00ffb4 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: .75rem;
}

.sg-sub {
    color: #64748b;
    font-size: 1.05rem;
    font-family: 'Space Mono', monospace;
    letter-spacing: .02em;
}

/* ── Card ── */
.sg-card {
    background: rgba(255,255,255,.028);
    border: 1px solid rgba(255,255,255,.07);
    border-radius: 20px;
    padding: 2rem 2rem 1.8rem;
    backdrop-filter: blur(14px);
    box-shadow:
        0 0 0 1px rgba(0,255,180,.04),
        0 24px 64px rgba(0,0,0,.55),
        inset 0 1px 0 rgba(255,255,255,.06);
    animation: fadeSlideUp .9s .15s cubic-bezier(.16,1,.3,1) both;
}

@keyframes fadeSlideDown {
    from { opacity:0; transform:translateY(-28px); }
    to   { opacity:1; transform:translateY(0); }
}
@keyframes fadeSlideUp {
    from { opacity:0; transform:translateY(28px); }
    to   { opacity:1; transform:translateY(0); }
}

/* ── Label ── */
.sg-label {
    font-family: 'Space Mono', monospace;
    font-size: .72rem;
    letter-spacing: .14em;
    text-transform: uppercase;
    color: #00ffb4;
    margin-bottom: .6rem;
    display: flex;
    align-items: center;
    gap: .5rem;
}

.sg-label::before {
    content: '';
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #00ffb4;
    box-shadow: 0 0 8px #00ffb4;
    animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
    0%,100% { transform: scale(1); opacity:1; }
    50%      { transform: scale(1.5); opacity:.5; }
}

/* ── Textarea ── */
textarea {
    background: rgba(0,0,0,.45) !important;
    border: 1px solid rgba(0,255,180,.18) !important;
    border-radius: 12px !important;
    color: #e2e8f0 !important;
    font-family: 'Space Mono', monospace !important;
    font-size: .9rem !important;
    line-height: 1.7 !important;
    padding: 1rem 1.1rem !important;
    transition: border-color .25s, box-shadow .25s !important;
    resize: vertical !important;
}

textarea:focus {
    border-color: rgba(0,255,180,.55) !important;
    box-shadow: 0 0 0 3px rgba(0,255,180,.09), 0 0 24px rgba(0,255,180,.07) !important;
    outline: none !important;
}

textarea::placeholder { color: #334155 !important; }

/* ── Button ── */
.stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, #00ffb4 0%, #00d4a0 100%) !important;
    color: #030712 !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    letter-spacing: .04em !important;
    border: none !important;
    border-radius: 12px !important;
    padding: .85rem 2rem !important;
    cursor: pointer !important;
    position: relative !important;
    overflow: hidden !important;
    transition: transform .2s, box-shadow .2s !important;
    box-shadow: 0 0 24px rgba(0,255,180,.25) !important;
    margin-top: .5rem !important;
}

.stButton > button::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,.25), transparent);
    transform: translateX(-100%);
    transition: transform .5s;
}

.stButton > button:hover::before { transform: translateX(100%); }

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 0 40px rgba(0,255,180,.4) !important;
}

.stButton > button:active { transform: translateY(0) !important; }

/* ── Result boxes ── */
.sg-result {
    border-radius: 16px;
    padding: 1.5rem 1.6rem;
    margin-top: 1.4rem;
    display: flex;
    align-items: flex-start;
    gap: 1rem;
    animation: resultReveal .55s cubic-bezier(.16,1,.3,1) both;
    position: relative;
    overflow: hidden;
}

@keyframes resultReveal {
    from { opacity:0; transform:scale(.95) translateY(12px); }
    to   { opacity:1; transform:scale(1) translateY(0); }
}

.sg-result::before {
    content:'';
    position:absolute;
    inset:0;
    opacity:.06;
    background-image: repeating-linear-gradient(
        45deg,
        currentColor 0,
        currentColor 1px,
        transparent 0,
        transparent 50%
    );
    background-size: 10px 10px;
}

.sg-result-spam {
    background: rgba(239,68,68,.1);
    border: 1px solid rgba(239,68,68,.35);
    color: #fca5a5;
    box-shadow: 0 0 32px rgba(239,68,68,.12), inset 0 1px 0 rgba(255,255,255,.04);
}

.sg-result-safe {
    background: rgba(0,255,180,.07);
    border: 1px solid rgba(0,255,180,.3);
    color: #6ee7b7;
    box-shadow: 0 0 32px rgba(0,255,180,.1), inset 0 1px 0 rgba(255,255,255,.04);
}

.sg-result-icon {
    font-size: 2rem;
    line-height: 1;
    flex-shrink: 0;
    filter: drop-shadow(0 0 8px currentColor);
    animation: iconPop .5s .1s cubic-bezier(.34,1.56,.64,1) both;
}

@keyframes iconPop {
    from { transform: scale(0) rotate(-20deg); }
    to   { transform: scale(1) rotate(0deg); }
}

.sg-result-content {}

.sg-result-title {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1.15rem;
    margin-bottom: .3rem;
}

.sg-result-desc {
    font-family: 'Space Mono', monospace;
    font-size: .75rem;
    opacity: .7;
    line-height: 1.6;
}

/* ── Scan line animation for spam ── */
.sg-scanline {
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, rgba(239,68,68,.8), transparent);
    animation: scanline 1.5s ease-in-out infinite;
}

@keyframes scanline {
    0%   { top: 0%; opacity: 1; }
    100% { top: 100%; opacity: 0; }
}

/* ── Warning / info ── */
.sg-warning {
    background: rgba(251,191,36,.07);
    border: 1px solid rgba(251,191,36,.25);
    color: #fde68a;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    font-family: 'Space Mono', monospace;
    font-size: .82rem;
    margin-top: 1rem;
    animation: resultReveal .4s cubic-bezier(.16,1,.3,1) both;
    display: flex;
    align-items: center;
    gap: .65rem;
}

/* ── Stats bar ── */
.sg-stats {
    display: flex;
    gap: 1rem;
    margin-top: 1.6rem;
    animation: fadeSlideUp 1s .3s cubic-bezier(.16,1,.3,1) both;
}

.sg-stat {
    flex: 1;
    background: rgba(255,255,255,.025);
    border: 1px solid rgba(255,255,255,.06);
    border-radius: 12px;
    padding: .9rem 1rem;
    text-align: center;
}

.sg-stat-num {
    font-family: 'Space Mono', monospace;
    font-size: 1.3rem;
    font-weight: 700;
    color: #00ffb4;
    margin-bottom: .2rem;
}

.sg-stat-label {
    font-family: 'Space Mono', monospace;
    font-size: .65rem;
    letter-spacing: .1em;
    text-transform: uppercase;
    color: #475569;
}

/* ── Footer ── */
.sg-footer {
    text-align: center;
    margin-top: 3rem;
    font-family: 'Space Mono', monospace;
    font-size: .68rem;
    color: #1e293b;
    letter-spacing: .08em;
    animation: fadeSlideUp 1s .5s cubic-bezier(.16,1,.3,1) both;
}

/* ── Divider ── */
.sg-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0,255,180,.15), transparent);
    margin: 1.6rem 0;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] { display: none !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(0,255,180,.2); border-radius: 99px; }
</style>
""", unsafe_allow_html=True)


# ── Load model and vectorizer ──────────────────────────────────────────────────
@st.cache_resource
def load_model():
    model = pickle.load(open("model.pkl", "rb"))
    vectorizer = pickle.load(open("vectorizer.pkl", "rb"))
    return model, vectorizer

model, vectorizer = load_model()


# ── UI ─────────────────────────────────────────────────────────────────────────

# Header
st.markdown("""
<div class="sg-header">
    <div class="sg-badge"><span>●</span> System Online</div>
    <div class="sg-title">Signal Guard</div>
    <div class="sg-sub">// Spam Detection Engine v2.0</div>
</div>
""", unsafe_allow_html=True)

# Stats row
st.markdown("""
<div class="sg-stats">
    <div class="sg-stat">
        <div class="sg-stat-num">ML</div>
        <div class="sg-stat-label">Powered</div>
    </div>
    <div class="sg-stat">
        <div class="sg-stat-num">99%</div>
        <div class="sg-stat-label">Accuracy</div>
    </div>
    <div class="sg-stat">
        <div class="sg-stat-num">&lt;1ms</div>
        <div class="sg-stat-label">Latency</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Card
st.markdown('<div class="sg-card">', unsafe_allow_html=True)
st.markdown('<div class="sg-label">Message Input</div>', unsafe_allow_html=True)

user_input = st.text_area(
    label="",
    placeholder="Paste or type a message to analyze...",
    height=160,
    label_visibility="collapsed"
)

st.markdown('<div class="sg-divider"></div>', unsafe_allow_html=True)

btn = st.button("⚡  Analyze Message")

if btn:
    if user_input.strip() == "":
        st.markdown("""
        <div class="sg-warning">
            ⚠ &nbsp; No input detected — please enter a message to analyze.
        </div>
        """, unsafe_allow_html=True)
    else:
        data = vectorizer.transform([user_input])
        prediction = model.predict(data)

        if prediction[0] == 1:
            st.markdown("""
            <div class="sg-result sg-result-spam">
                <div class="sg-scanline"></div>
                <div class="sg-result-icon">🚨</div>
                <div class="sg-result-content">
                    <div class="sg-result-title">Spam Detected</div>
                    <div class="sg-result-desc">
                        This message matches known spam patterns.<br>
                        Treat with caution — do not click links or reply.
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="sg-result sg-result-safe">
                <div class="sg-result-icon">✅</div>
                <div class="sg-result-content">
                    <div class="sg-result-title">Message Clear</div>
                    <div class="sg-result-desc">
                        No spam signatures detected.<br>
                        This message appears to be legitimate.
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # close .sg-card

# Footer
st.markdown("""
<div class="sg-footer">
    SIGNAL GUARD · ML SPAM DETECTION · ALL PROCESSING LOCAL
</div>
""", unsafe_allow_html=True)
