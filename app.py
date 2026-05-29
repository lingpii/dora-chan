import streamlit as st
import streamlit.components.v1 as components
import datetime
import html as html_lib
import base64
from chat import DoraChat
import speech_recognition as sr
import io
from voice import Speech_Recognition

st.set_page_config(
    page_title="Dora-chan 1.0 ",
    page_icon=":)",
    layout="centered",
    initial_sidebar_state="collapsed",
)
def now_time():
    return datetime.datetime.now().strftime("%-I:%M %p")


if "messages" not in st.session_state:
    st.session_state.messages = [
    {"role": "dora", "content": " Ciao ~ Dora chào bạn ", "time": now_time()},
    ]
 
if "dora"  not in st.session_state:
    st.session_state.dora = DoraChat()

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None
if "dora_voice" not in st.session_state:
    st.session_state.dora_voice = Speech_Recognition()
if "pending_audio" not in st.session_state:
    st.session_state.pending_audio = None
if "mode" not in st.session_state:
    st.session_state.mode = "text"
if "audio_key" not in st.session_state:
    st.session_state.audio_key = 0


# ── SVG definitions (injected once, referenced by all avatars) ──────────────
GLOBAL_SVG_DEFS = """
<svg width="0" height="0" style="position:absolute">
  <defs>
    <radialGradient id="doraBg" cx="50%" cy="40%" r="60%">
      <stop offset="0%" stop-color="#ffeaf3"/>
      <stop offset="100%" stop-color="#e9d4ff"/>
    </radialGradient>
    <radialGradient id="doraPetal" cx="50%" cy="40%" r="60%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#ffc6dc"/>
    </radialGradient>
  </defs>
</svg>
"""

def avatar_svg(size=28):
    return f"""<svg width="{size}" height="{size}" viewBox="0 0 40 40" fill="none"
      xmlns="http://www.w3.org/2000/svg"
      style="display:block;flex-shrink:0;min-width:{size}px">
  <circle cx="20" cy="20" r="20" fill="url(#doraBg)"/>
  <g transform="translate(20 20)">
    <ellipse cx="0" cy="-7.5" rx="3.6" ry="5.4" fill="url(#doraPetal)" stroke="#ffb6cf" stroke-width="0.6"/>
    <ellipse cx="0" cy="-7.5" rx="3.6" ry="5.4" fill="url(#doraPetal)" stroke="#ffb6cf" stroke-width="0.6" transform="rotate(72)"/>
    <ellipse cx="0" cy="-7.5" rx="3.6" ry="5.4" fill="url(#doraPetal)" stroke="#ffb6cf" stroke-width="0.6" transform="rotate(144)"/>
    <ellipse cx="0" cy="-7.5" rx="3.6" ry="5.4" fill="url(#doraPetal)" stroke="#ffb6cf" stroke-width="0.6" transform="rotate(216)"/>
    <ellipse cx="0" cy="-7.5" rx="3.6" ry="5.4" fill="url(#doraPetal)" stroke="#ffb6cf" stroke-width="0.6" transform="rotate(288)"/>
    <circle cx="0" cy="0" r="2.2" fill="#ffd166"/>
    <circle cx="0" cy="0" r="2.2" fill="#fff3b0" opacity="0.5"/>
  </g>
</svg>"""

# ── CSS ──────────────────────────────────────────────────────────────────────
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

/* ── page background ── */
html, body, [data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 70% 55% at 22% 35%, rgba(255,200,225,0.55), transparent 65%),
        radial-gradient(ellipse 65% 60% at 78% 65%, rgba(208,180,245,0.55), transparent 65%),
        radial-gradient(ellipse 80% 50% at 50% 100%, rgba(255,220,235,0.45), transparent 70%),
        linear-gradient(180deg, #fbf6ff 0%, #fdf2f8 100%) !important;
    font-family: "Plus Jakarta Sans", -apple-system, BlinkMacSystemFont, sans-serif;
}

/* ── hide Streamlit chrome ── */
[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
#MainMenu,
footer { display: none !important; }

/* ── content area ── */
.main .block-container {
    padding-top: 90px !important;
    padding-bottom: 40px !important;
    max-width: 540px !important;
    padding-left: 0 !important;
    padding-right: 0 !important;
}
[data-testid="stMainBlockContainer"] {
    max-width: 540px !important;
}

/* ── fixed header ── */
.dora-header {
    position: fixed;
    top: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 100%;
    max-width: 540px;
    z-index: 999;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px 20px 14px;
    background: rgba(255,255,255,0.72);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-bottom: 1px solid rgba(179,136,255,0.14);
    box-sizing: border-box;
}
.dora-header-left { display: flex; align-items: center; gap: 10px; }
.dora-name {
    font-size: 17px; font-weight: 600; color: #2c1e3f;
    letter-spacing: -0.01em;
    display: flex; align-items: center; gap: 6px;
}
.dora-status {
    display: flex; align-items: center; gap: 5px;
    font-size: 12px; color: #7a6b94; font-weight: 500; margin-top: 2px;
}
.online-dot {
    width: 7px; height: 7px; border-radius: 50%;
    background: #4ade80;
    box-shadow: 0 0 0 2.5px rgba(74,222,128,0.22);
    display: inline-block; flex-shrink: 0;
}
.header-more-btn {
    width: 32px; height: 32px; border: none; background: transparent;
    border-radius: 10px; cursor: pointer; color: #b5aac8;
    display: flex; align-items: center; justify-content: center;
}

/* ── date chip ── */
.date-chip {
    display: block; text-align: center; width: fit-content;
    margin: 4px auto 12px;
    font-size: 11px; color: #8b7aaa; font-weight: 500;
    letter-spacing: 0.04em; text-transform: uppercase;
    padding: 4px 12px;
    background: rgba(255,255,255,0.55);
    border-radius: 999px;
}

/* ── message wrappers ── */
.msg-row {
    display: flex;
    flex-direction: column;
    gap: 4px;
    margin-bottom: 6px;
}
.dora-row { align-items: flex-start; }
.user-row  { align-items: flex-end; }

.dora-bubble-wrap { display: flex; gap: 8px; align-items: flex-end; max-width: 78%; }

/* ── dora bubble ── */
.dora-bubble {
    background: #ffffff;
    color: #2c1e3f;
    padding: 11px 15px;
    border-radius: 18px 18px 18px 4px;
    font-size: 14.5px; line-height: 1.55;
    box-shadow: 0 1px 2px rgba(110,70,180,0.04), 0 6px 16px rgba(140,90,200,0.06);
    border: 1px solid rgba(179,136,255,0.08);
    word-break: break-word;
}

/* ── user bubble ── */
.user-bubble {
    background: #f0e6fa;
    color: #4a3a64;
    padding: 11px 15px;
    border-radius: 18px 18px 4px 18px;
    font-size: 14.5px; line-height: 1.55; font-weight: 500;
    box-shadow: 0 1px 2px rgba(110,70,180,0.04), 0 6px 16px rgba(140,90,200,0.07);
    border: 1px solid rgba(179,136,255,0.12);
    max-width: 76%;
    word-break: break-word;
}

/* ── timestamps ── */
.bubble-time {
    font-size: 11px; color: #9a8ab8;
    margin-left: 6px; margin-top: 0;
}
.bubble-time-right {
    font-size: 11px; color: #9a8ab8;
    margin-right: 6px; margin-top: 0; text-align: right;
}

/* ── typing indicator ── */
@keyframes doraDot {
    0%, 80%, 100% { transform: translateY(0); opacity: 0.35; }
    40%            { transform: translateY(-3px); opacity: 1; }
}
.typing-bubble {
    display: flex; gap: 8px; align-items: flex-end; margin-bottom: 6px;
}
.typing-inner {
    background: #ffffff;
    padding: 12px 16px;
    border-radius: 18px 18px 18px 4px;
    box-shadow: 0 1px 2px rgba(110,70,180,0.04), 0 6px 16px rgba(140,90,200,0.06);
    border: 1px solid rgba(179,136,255,0.08);
    display: flex; gap: 4px; align-items: center;
}
.dot {
    width: 6px; height: 6px; border-radius: 50%;
    background: #b388ff; opacity: 0.6; display: inline-block;
}
.dot:nth-child(1) { animation: doraDot 1.2s 0.0s  infinite ease-in-out; }
.dot:nth-child(2) { animation: doraDot 1.2s 0.15s infinite ease-in-out; }
.dot:nth-child(3) { animation: doraDot 1.2s 0.30s infinite ease-in-out; }

/* ── mode tabs (rendered above chat input) ── */
.mode-tabs-wrap {
    display: flex; align-items: center; gap: 4px;
    padding: 4px;
    background: rgba(179,136,255,0.08);
    border-radius: 999px;
    width: fit-content;
    margin: 12px 0 4px;
}
.tab-btn {
    display: flex; align-items: center; gap: 6px;
    border: none; border-radius: 999px; cursor: pointer;
    font-size: 13px; font-weight: 600;
    font-family: "Plus Jakarta Sans", sans-serif;
    transition: all 0.15s;
    line-height: 1;
}
.tab-active  { padding: 7px 13px; background: #ffffff; color: #9466e8;
               box-shadow: 0 2px 8px rgba(179,136,255,0.15); }
.tab-idle    { padding: 7px 10px; background: transparent; color: #7a6b94; }
.tab-disabled{ padding: 7px 10px; background: transparent; color: #c4b8d8; cursor: not-allowed; }
.soon-badge  {
    font-size: 9px; font-weight: 700; padding: 2px 5px;
    border-radius: 4px; background: rgba(179,136,255,0.12);
    color: #a99cc4; letter-spacing: 0.04em; margin-left: 2px;
}

/* ── override Streamlit chat input ── */
[data-testid="stChatInputContainer"] {
    background: rgba(255,255,255,0.92) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border-top: 1px solid rgba(179,136,255,0.14) !important;
    max-width: 540px !important;
}
[data-testid="stChatInput"] textarea {
    font-family: "Plus Jakarta Sans", sans-serif !important;
    font-size: 14.5px !important;
    color: #2c1e3f !important;
    background: #ffffff !important;
    border: 1px solid rgba(179,136,255,0.18) !important;
    border-radius: 14px !important;
}
[data-testid="stChatInput"] textarea::placeholder { color: #b5aac8 !important; }
[data-testid="stChatInputSubmitButton"] button {
    background: linear-gradient(135deg, #b388ff, #9466e8) !important;
    border-radius: 10px !important;
    box-shadow: 0 4px 10px rgba(148,102,232,0.35) !important;
    border: none !important;
}

/* ── scrollbar hide ── */
::-webkit-scrollbar { display: none; }
* { scrollbar-width: none; }


/* ── tab buttons ── */
div[data-testid="stHorizontalBlock"] {
    background: rgba(179,136,255,0.08);
    border-radius: 999px;
    padding: 4px;
    width: fit-content;
    gap: 0 !important;
    align-items:center;
}
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
    padding: 0 !important;     
    width: fit-content !important;
    flex: unset !important;

button[data-testid="stBaseButton-secondary"] {
    background: transparent !important; border: none !important;
    color: #7a6b94 !important; border-radius: 999px !important;
    font-size: 13px !important; font-weight: 600 !important;
    font-family: "Plus Jakarta Sans", sans-serif !important;
    padding: 7px 10px !important; box-shadow: none !important;
    min-height: unset !important;
}
button[data-testid="stBaseButton-primary"] {
    background: #ffffff !important; border: none !important;
    color: #9466e8 !important; border-radius: 999px !important;
    font-size: 13px !important; font-weight: 600 !important;
    font-family: "Plus Jakarta Sans", sans-serif !important;
    padding: 7px 13px !important;
    box-shadow: 0 2px 8px rgba(179,136,255,0.15) !important;
    min-height: unset !important;
}


</style>
"""

# ── helpers ──────────────────────────────────────────────────────────────────

def dora_bubble_html(content, time_str=None, show_avatar=True):
    esc = html_lib.escape(content)
    av = avatar_svg(28) if show_avatar else f'<div style="width:28px;flex-shrink:0"></div>'
    time_part = f'<div class="bubble-time">{time_str}</div>' if time_str else ""
    return f"""
<div class="msg-row dora-row">
  <div class="dora-bubble-wrap">
    {av}
    <div>
      <div class="dora-bubble">{esc}</div>
      {time_part}
    </div>
  </div>
</div>"""

def user_bubble_html(content, time_str=None):
    esc = html_lib.escape(content)
    time_part = f'<div class="bubble-time-right">{time_str}</div>' if time_str else ""
    return f"""
<div class="msg-row user-row">
  <div class="user-bubble">{esc}</div>
  {time_part}
</div>"""

TYPING_HTML = f"""
<div class="typing-bubble">
  {avatar_svg(28)}
  <div class="typing-inner">
    <span class="dot"></span><span class="dot"></span><span class="dot"></span>
  </div>
</div>"""
# ── render ───────────────────────────────────────────────────────────────────

st.markdown(CSS, unsafe_allow_html=True)
st.markdown(GLOBAL_SVG_DEFS, unsafe_allow_html=True)

# Fixed header
st.markdown(f"""
<div class="dora-header">
  <div class="dora-header-left">
    {avatar_svg(36)}
    <div>
      <div class="dora-name">Dora-chan <span style="font-size:14px">🌸</span></div>
      <div class="dora-status">
        <span class="online-dot"></span>
        Online · usually replies instantly
      </div>
    </div>
  </div>
  <button class="header-more-btn" aria-label="More">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
      <circle cx="5"  cy="12" r="1.7" fill="currentColor"/>
      <circle cx="12" cy="12" r="1.7" fill="currentColor"/>
      <circle cx="19" cy="12" r="1.7" fill="currentColor"/>
    </svg>
  </button>
</div>
""", unsafe_allow_html=True)

# Messages
parts = ['<div class="date-chip">Today</div>']
msgs = st.session_state.messages
for i, msg in enumerate(msgs):
    if msg["role"] == "dora":
        parts.append(dora_bubble_html(msg["content"], msg.get("time"), msg.get("show_avatar", True)))
    else:
        parts.append(user_bubble_html(msg["content"], msg.get("time")))

# Show typing indicator when last message is from user
if msgs and msgs[-1]["role"] == "user":
    parts.append(TYPING_HTML)

st.markdown("".join(parts), unsafe_allow_html=True)
if st.session_state.pending_prompt:
    prompt = st.session_state.pending_prompt
    st.session_state.pending_prompt = None
    dora_reply = st.write_stream(
        st.session_state.dora.chat_stream(prompt)
    )
    st.session_state.messages.append({
        "role": "dora",
        "content": dora_reply,
        "time": now_time(),
        "show_avatar": True,
    })
    if st.session_state.mode == "voice":
        audio_path = st.session_state.dora_voice.generate_wav(dora_reply)
        fmt = "audio/mpeg" if audio_path.endswith(".mp3") else "audio/wav"
        with open(audio_path, "rb") as f:
            st.session_state.pending_audio = (f.read(), fmt)
    st.rerun()

if st.session_state.pending_audio:
    audio_bytes, fmt = st.session_state.pending_audio
    b64 = base64.b64encode(audio_bytes).decode()
    components.html(
        f'<audio autoplay style="display:none"><source src="data:{fmt};base64,{b64}" type="{fmt}"></audio>',
        height=0,
    )
    st.session_state.pending_audio = None 


# choose mode text/voice/file 
col1, col2, col3 = st.columns([1, 1, 1.5])
with col1:
    if st.button("📝 Text", use_container_width=True,
                 type="primary" if st.session_state.mode == "text" else "secondary"):
        st.session_state.mode = "text"; st.rerun()
with col2:
    if st.button("🎙️ Voice", use_container_width=True,
                 type="primary" if st.session_state.mode == "voice" else "secondary"):
        st.session_state.mode = "voice"; st.rerun()
with col3:
    st.markdown(
        '<p style="padding-top:6px;font-size:13px;font-weight:600;color:#c4b8d8">'
        '📎 File <span style="font-size:9px;background:rgba(179,136,255,0.12);'
        'color:#a99cc4;padding:2px 5px;border-radius:4px">SOON</span></p>',
        unsafe_allow_html=True)

# Chat input / voice input 
if st.session_state.mode == "text":
    if prompt := st.chat_input("Chat với Dora nè ... "):
        t = now_time()
        st.session_state.messages.append({"role": "user", "content": prompt, "time": t})
        st.session_state.pending_prompt = prompt
        st.rerun()
else: 
    audio_data = st.audio_input("Talk to me babe ~ ", key=f"audio_{st.session_state.audio_key}")
    if audio_data is not None:
        recognizer = sr.Recognizer()
        recognizer.energy_threshold = 400
        recognizer.dynamic_energy_threshold = False
        with sr.AudioFile(io.BytesIO(audio_data.read())) as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.record(source)
        try: 
            text = recognizer.recognize_google(audio, language = "vi-VN")
            st.session_state.messages.append({
            "role": "user",
            "content": text,
            "time": now_time(),
            "show_avatar": True,
        })
            st.session_state.pending_prompt = text
            st.session_state.audio_key += 1
            st.rerun()
        except sr.UnknownValueError:
            st.warning("Nói to lên xíu ik. Dora nghe hong có rõ")
        except sr.RequestError:
            st.error("Dora bận xíu ời. Hồi rep nhe >-< ")