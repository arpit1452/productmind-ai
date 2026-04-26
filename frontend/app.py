import streamlit as st
import json
import time
import os
import re

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Product Manager Agent",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&family=DM+Sans:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, [data-testid="stAppViewContainer"] {
    background: #0a0a0f; color: #e8e6f0; font-family: 'DM Sans', sans-serif;
}
[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse at 20% 0%, #1a0a2e 0%, #0a0a0f 50%),
                radial-gradient(ellipse at 80% 100%, #0d1a2e 0%, transparent 50%);
    min-height: 100vh;
}
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }
.block-container { padding: 2rem 3rem; max-width: 1200px; margin: 0 auto; }
[data-testid="stSidebar"] {
    background: #0d0d14 !important;
    border-right: 1px solid rgba(255,255,255,0.06) !important;
}
[data-testid="stSidebar"] .block-container { padding: 2rem 1.5rem !important; }
.hero { text-align: center; padding: 3rem 0 2rem; }
.hero-badge {
    display: inline-block; font-family: 'DM Mono', monospace; font-size: 0.7rem;
    letter-spacing: 0.2em; text-transform: uppercase; color: #a78bfa;
    background: rgba(167,139,250,0.1); border: 1px solid rgba(167,139,250,0.3);
    padding: 0.4rem 1rem; border-radius: 100px; margin-bottom: 1.5rem;
}
.hero-title {
    font-family: 'Syne', sans-serif; font-size: clamp(2.5rem, 6vw, 4.5rem);
    font-weight: 800; line-height: 1.05; margin: 0 0 1rem;
    background: linear-gradient(135deg, #fff 0%, #a78bfa 50%, #60a5fa 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.hero-sub { font-size: 1.1rem; color: #7c7a8a; max-width: 500px; margin: 0 auto; line-height: 1.6; font-weight: 300; }
.lock-screen { text-align: center; padding: 4rem 2rem; max-width: 500px; margin: 0 auto; }
.lock-icon { font-size: 3rem; margin-bottom: 1rem; }
.lock-title { font-family: 'Syne', sans-serif; font-size: 1.5rem; font-weight: 700; color: #e8e6f0; margin-bottom: 0.75rem; }
.lock-sub { color: #6b6880; font-size: 0.95rem; line-height: 1.6; margin-bottom: 1.5rem; }
.lock-link {
    display: inline-block; background: linear-gradient(135deg, #7c3aed, #4f46e5);
    color: white !important; text-decoration: none !important; padding: 0.6rem 1.5rem;
    border-radius: 8px; font-family: 'Syne', sans-serif; font-size: 0.85rem; font-weight: 600;
}
.pipeline { display: flex; align-items: center; justify-content: center; gap: 0.5rem; margin: 2rem 0; flex-wrap: wrap; }
.pipe-step {
    font-family: 'DM Mono', monospace; font-size: 0.65rem; letter-spacing: 0.05em; color: #6b6880;
    background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07);
    padding: 0.35rem 0.8rem; border-radius: 6px;
}
.pipe-arrow { color: #3d3a4a; font-size: 0.8rem; }
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.04) !important; border: 1px solid rgba(167,139,250,0.3) !important;
    border-radius: 10px !important; color: #e8e6f0 !important; font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important; padding: 0.85rem 1.2rem !important; transition: border-color 0.2s !important;
}
.stTextInput > div > div > input:focus { border-color: #a78bfa !important; box-shadow: 0 0 0 3px rgba(167,139,250,0.1) !important; }
.stTextInput label { color: #9d9aad !important; font-family: 'DM Mono', monospace !important; font-size: 0.75rem !important; letter-spacing: 0.1em !important; text-transform: uppercase !important; }
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #4f46e5) !important; color: white !important;
    border: none !important; border-radius: 10px !important; padding: 0.75rem 2.5rem !important;
    font-family: 'Syne', sans-serif !important; font-size: 0.95rem !important; font-weight: 600 !important;
    cursor: pointer !important; transition: all 0.2s !important; width: 100% !important;
}
.stButton > button:hover { background: linear-gradient(135deg, #8b5cf6, #6366f1) !important; transform: translateY(-1px) !important; box-shadow: 0 8px 25px rgba(124,58,237,0.4) !important; }
[data-testid="stFileUploader"] { background: rgba(255,255,255,0.02) !important; border: 1px dashed rgba(255,255,255,0.1) !important; border-radius: 12px !important; padding: 1rem !important; }
.stSuccess { background: rgba(52,211,153,0.08) !important; border: 1px solid rgba(52,211,153,0.25) !important; border-radius: 10px !important; }
.stError { background: rgba(248,113,113,0.08) !important; border: 1px solid rgba(248,113,113,0.25) !important; border-radius: 10px !important; }
.stWarning { background: rgba(251,191,36,0.08) !important; border: 1px solid rgba(251,191,36,0.25) !important; border-radius: 10px !important; }
.tools-banner { display: flex; gap: 0.5rem; flex-wrap: wrap; margin: 1rem 0; padding: 1rem 1.5rem; background: rgba(167,139,250,0.05); border: 1px solid rgba(167,139,250,0.15); border-radius: 12px; }
.tool-tag { font-family: 'DM Mono', monospace; font-size: 0.7rem; color: #a78bfa; background: rgba(167,139,250,0.1); border: 1px solid rgba(167,139,250,0.2); padding: 0.25rem 0.7rem; border-radius: 6px; }
.tools-label { font-family: 'DM Mono', monospace; font-size: 0.7rem; color: #5a5768; letter-spacing: 0.1em; text-transform: uppercase; display: flex; align-items: center; margin-right: 0.5rem; }
.output-card { background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; padding: 2.5rem; margin-top: 1.5rem; }
.output-content h1 { font-family: 'Syne', sans-serif !important; font-size: 1.8rem !important; font-weight: 800 !important; color: #fff !important; margin: 2rem 0 1rem !important; padding-bottom: 0.75rem !important; border-bottom: 2px solid rgba(167,139,250,0.3) !important; }
.output-content h2 { font-family: 'Syne', sans-serif !important; font-size: 1.3rem !important; font-weight: 700 !important; color: #a78bfa !important; margin: 2rem 0 0.75rem !important; }
.output-content h3 { font-family: 'Syne', sans-serif !important; font-size: 1rem !important; font-weight: 600 !important; color: #c4b5fd !important; margin: 1.5rem 0 0.5rem !important; }
.output-content p { color: #b8b5c8 !important; line-height: 1.8 !important; }
.output-content ul, .output-content ol { color: #b8b5c8 !important; padding-left: 1.5rem !important; }
.output-content li { margin-bottom: 0.4rem !important; line-height: 1.7 !important; }
.output-content strong { color: #e8e6f0 !important; font-weight: 600 !important; }
.output-content table { width: 100% !important; border-collapse: collapse !important; margin: 1rem 0 !important; font-family: 'DM Mono', monospace !important; font-size: 0.8rem !important; }
.output-content th { background: rgba(167,139,250,0.1) !important; color: #a78bfa !important; padding: 0.6rem 1rem !important; text-align: left !important; border: 1px solid rgba(167,139,250,0.2) !important; }
.output-content td { padding: 0.6rem 1rem !important; border: 1px solid rgba(255,255,255,0.06) !important; color: #b8b5c8 !important; }
.output-content code { background: rgba(167,139,250,0.1) !important; color: #c4b5fd !important; padding: 0.2rem 0.5rem !important; border-radius: 4px !important; font-family: 'DM Mono', monospace !important; }
.output-content hr { border: none !important; border-top: 1px solid rgba(255,255,255,0.06) !important; margin: 2rem 0 !important; }
.section-divider { height: 1px; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.06), transparent); margin: 2rem 0; }
</style>
""", unsafe_allow_html=True)


# ─── PDF Generator ─────────────────────────────────────────────────────────────
def markdown_to_pdf(markdown_text: str, idea: str) -> bytes:
    try:
        from fpdf import FPDF

        class PDF(FPDF):
            def header(self):
                self.set_fill_color(15, 10, 30)
                self.rect(0, 0, 210, 20, 'F')
                self.set_font('Helvetica', 'B', 10)
                self.set_text_color(167, 139, 250)
                self.set_y(6)
                self.cell(0, 8, 'AI Product Manager Agent', align='C')
                self.set_text_color(80, 75, 100)
                self.ln(20)

            def footer(self):
                self.set_y(-15)
                self.set_font('Helvetica', '', 8)
                self.set_text_color(80, 75, 100)
                self.cell(0, 10, f'Page {self.page_no()} | AI Product Manager Agent', align='C')

        pdf = PDF()
        pdf.set_auto_page_break(auto=True, margin=20)
        pdf.add_page()
        pdf.set_margins(20, 25, 20)

        for line in markdown_text.split('\n'):
            line = line.rstrip()
            if line.startswith('# '):
                pdf.ln(4)
                pdf.set_font('Helvetica', 'B', 18)
                pdf.set_text_color(255, 255, 255)
                text = re.sub(r'[^\x00-\x7F]+', '', line[2:].strip())
                pdf.multi_cell(0, 10, text)
                pdf.set_draw_color(124, 58, 237)
                pdf.set_line_width(0.5)
                pdf.line(20, pdf.get_y(), 190, pdf.get_y())
                pdf.ln(4)
            elif line.startswith('## '):
                pdf.ln(5)
                pdf.set_font('Helvetica', 'B', 13)
                pdf.set_text_color(167, 139, 250)
                text = re.sub(r'[^\x00-\x7F]+', '', line[3:].strip())
                pdf.multi_cell(0, 8, text)
                pdf.ln(2)
            elif line.startswith('### '):
                pdf.ln(3)
                pdf.set_font('Helvetica', 'B', 11)
                pdf.set_text_color(196, 181, 253)
                text = re.sub(r'[^\x00-\x7F]+', '', line[4:].strip())
                pdf.multi_cell(0, 7, text)
                pdf.ln(1)
            elif line.strip() in ['---', '***', '___']:
                pdf.ln(2)
                pdf.set_draw_color(50, 45, 70)
                pdf.set_line_width(0.3)
                pdf.line(20, pdf.get_y(), 190, pdf.get_y())
                pdf.ln(4)
            elif line.strip().startswith('|') and line.strip().endswith('|'):
                cells = [c.strip() for c in line.strip().strip('|').split('|')]
                if all(re.match(r'^:?-+:?$', c.strip()) for c in cells if c.strip()):
                    continue
                col_width = 170 / max(len(cells), 1)
                is_header = any(c.startswith('**') for c in cells)
                pdf.set_font('Helvetica', 'B' if is_header else '', 8)
                pdf.set_text_color(167, 139, 250) if is_header else pdf.set_text_color(184, 181, 200)
                pdf.set_fill_color(30, 20, 50) if is_header else pdf.set_fill_color(18, 15, 30)
                for cell in cells:
                    cell = re.sub(r'\*\*(.+?)\*\*', r'\1', cell)
                    cell = re.sub(r'[^\x00-\x7F]+', '', cell)
                    pdf.cell(col_width, 7, cell[:30], border=1, fill=True)
                pdf.ln()
            elif line.strip().startswith('- ') or line.strip().startswith('* '):
                pdf.set_font('Helvetica', '', 10)
                pdf.set_text_color(184, 181, 200)
                text = re.sub(r'\*\*(.+?)\*\*', r'\1', line.strip()[2:].strip())
                text = re.sub(r'[^\x00-\x7F]+', '', text)
                pdf.set_x(25)
                pdf.cell(5, 6, chr(149))
                pdf.multi_cell(160, 6, text)
            elif re.match(r'^\d+\.\s', line.strip()):
                pdf.set_font('Helvetica', '', 10)
                pdf.set_text_color(184, 181, 200)
                text = re.sub(r'^\d+\.\s', '', line.strip())
                text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
                text = re.sub(r'[^\x00-\x7F]+', '', text)
                num = re.match(r'^(\d+)\.', line.strip()).group(1)
                pdf.set_x(25)
                pdf.cell(8, 6, f"{num}.")
                pdf.multi_cell(157, 6, text)
            elif line.strip() == '':
                pdf.ln(2)
            else:
                pdf.set_font('Helvetica', '', 10)
                pdf.set_text_color(184, 181, 200)
                text = re.sub(r'\*\*(.+?)\*\*', r'\1', line.strip())
                text = re.sub(r'\*(.+?)\*', r'\1', text)
                text = re.sub(r'[^\x00-\x7F]+', '', text)
                if text:
                    pdf.multi_cell(0, 6, text)

        output = pdf.output()
        return bytes(bytearray(output))

    except Exception as e:
        return markdown_text.encode('utf-8')


# ─── Sidebar: API Key ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 0.5rem 0 1.5rem'>
        <div style='font-family: Syne, sans-serif; font-size: 1.1rem; font-weight: 700; color: #e8e6f0; margin-bottom: 0.3rem'>
            🔑 API Key
        </div>
        <div style='font-family: DM Mono, monospace; font-size: 0.65rem; color: #5a5768; letter-spacing: 0.05em'>
            Required to use this app
        </div>
    </div>
    """, unsafe_allow_html=True)

    gemini_key = st.text_input(
    "Gemini API Key", type="password",
    placeholder="AIza...", label_visibility="collapsed",
    key="gemini_api_key_input"
)

    if gemini_key and gemini_key.startswith("AIza"):
        st.markdown("""<div style='background: rgba(52,211,153,0.08); border: 1px solid rgba(52,211,153,0.25);
        border-radius: 8px; padding: 0.6rem 0.9rem; margin-top: 0.5rem;
        font-family: DM Mono, monospace; font-size: 0.7rem; color: #6ee7b7'>✓ Key looks valid</div>""",
        unsafe_allow_html=True)
    elif gemini_key:
        st.markdown("""<div style='background: rgba(248,113,113,0.08); border: 1px solid rgba(248,113,113,0.25);
        border-radius: 8px; padding: 0.6rem 0.9rem; margin-top: 0.5rem;
        font-family: DM Mono, monospace; font-size: 0.7rem; color: #fca5a5'>✗ Key should start with AIza</div>""",
        unsafe_allow_html=True)

    st.markdown("""
    <div style='margin-top: 1rem; padding: 1rem; background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06); border-radius: 10px'>
        <div style='font-family: DM Mono, monospace; font-size: 0.65rem; color: #5a5768; line-height: 1.8'>
            🔒 Your key is never stored<br>📡 Used only for this session<br>🆓 Free tier: 15 req/min
        </div>
    </div>
    <div style='margin-top: 1rem'>
        <a href='https://aistudio.google.com/app/apikey' target='_blank'
        style='display: block; text-align: center; background: linear-gradient(135deg, #7c3aed, #4f46e5);
        color: white; text-decoration: none; padding: 0.6rem; border-radius: 8px;
        font-family: Syne, sans-serif; font-size: 0.8rem; font-weight: 600'>Get Free API Key →</a>
    </div>
    """, unsafe_allow_html=True)

# ─── Lock Screen ───────────────────────────────────────────────────────────────
if not gemini_key or not gemini_key.strip():
    st.markdown("""
    <div class="hero">
        <div class="hero-badge">⚡ Powered by Multi-Tool AI Agent</div>
        <h1 class="hero-title">AI Product Manager</h1>
        <p class="hero-sub">Transform any idea into a complete product plan with market research, PRD, RICE scoring, and expert critique.</p>
    </div>
    <div class="lock-screen">
        <div class="lock-icon">🔐</div>
        <div class="lock-title">Enter your API Key to begin</div>
        <div class="lock-sub">Enter your free Gemini API key in the sidebar to get started.</div>
        <a class="lock-link" href="https://aistudio.google.com/app/apikey" target="_blank">Get your free key →</a>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ─── Main App ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">⚡ Powered by Multi-Tool AI Agent</div>
    <h1 class="hero-title">AI Product Manager</h1>
    <p class="hero-sub">Transform any idea into a complete product plan in minutes.</p>
</div>
<div class="pipeline">
    <span class="pipe-step">🔍 search_tool</span><span class="pipe-arrow">→</span>
    <span class="pipe-step">📄 rag_tool</span><span class="pipe-arrow">→</span>
    <span class="pipe-step">🧠 research_tool</span><span class="pipe-arrow">→</span>
    <span class="pipe-step">📋 prd_tool</span><span class="pipe-arrow">→</span>
    <span class="pipe-step">📊 planning_tool</span><span class="pipe-arrow">→</span>
    <span class="pipe-step">🧪 critic_tool</span>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])
with col1:
    idea = st.text_input(
    "Your Product Idea", 
    placeholder="e.g. AI fitness app for college students in India...",
    key="product_idea_input"
)
with col2:
    st.markdown("<div style='height: 28px'></div>", unsafe_allow_html=True)
    generate_clicked = st.button("🚀 Generate Plan", use_container_width=True)

with st.expander("📎 Attach a research PDF (optional)"):
    uploaded_file = st.file_uploader("Upload PDF for additional context", type=["pdf"], label_visibility="visible")
    if uploaded_file is not None:
        try:
            # Save PDF to temp location for RAG
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.getvalue())
                tmp_path = tmp.name
            from app.rag.pdf_loader import load_pdf
            load_pdf(tmp_path)
            st.success("✅ PDF uploaded and indexed successfully!")
        except Exception as e:
            st.error(f"Error uploading PDF: {str(e)}")

st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

# ─── Generate ──────────────────────────────────────────────────────────────────
if generate_clicked:
    if not idea.strip():
        st.warning("⚠️ Please enter a product idea first.")
    else:
        with st.spinner("🤖 Agent is working... This may take 2-3 minutes"):
            try:
                start_time = time.time()

                # ── Set API keys from user input + streamlit secrets ──
                os.environ["GEMINI_API_KEY"] = gemini_key.strip()

                # Tavily key from Streamlit secrets (set in deployment)
                try:
                    os.environ["TAVILY_API_KEY"] = st.secrets["TAVILY_API_KEY"]
                except Exception:
                    pass  # Will use existing env var if set

                # ── Direct function call (no HTTP request needed) ──
                from app.agents.pm_agent import run_agent
                result = run_agent(idea)

                elapsed = round(time.time() - start_time, 1)
                output = result.get("output", "No output generated.")
                tools_used = result.get("tools_used", [])
                num_steps = result.get("num_steps", 0)
                steps = result.get("steps", [])

                st.success(f"✅ Generated successfully in {elapsed}s")

                # Tools banner
                if tools_used:
                    tools_html = '<div class="tools-banner"><span class="tools-label">Tools used</span>'
                    for t in tools_used:
                        tools_html += f'<span class="tool-tag">{t}</span>'
                    tools_html += f'<span style="margin-left:auto;font-family:DM Mono,monospace;font-size:0.7rem;color:#5a5768">{num_steps} steps · {elapsed}s</span>'
                    tools_html += '</div>'
                    st.markdown(tools_html, unsafe_allow_html=True)

                # Output
                st.markdown('<div class="output-card"><div class="output-content">', unsafe_allow_html=True)
                st.markdown(output)
                st.markdown('</div></div>', unsafe_allow_html=True)

                # Download buttons
                st.markdown("<div style='height: 1rem'></div>", unsafe_allow_html=True)
                dl_col1, dl_col2 = st.columns(2)
                with dl_col1:
                    st.download_button(
                        label="⬇️ Download as Markdown",
                        data=output,
                        file_name=f"product_plan_{idea[:25].replace(' ','_')}.md",
                        mime="text/markdown",
                        use_container_width=True
                    )
                with dl_col2:
                    pdf_bytes = markdown_to_pdf(output, idea)
                    st.download_button(
                        label="📄 Download as PDF",
                        data=pdf_bytes,
                        file_name=f"product_plan_{idea[:25].replace(' ','_')}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )

                # Intermediate steps
                if steps:
                    with st.expander(f"🔍 View intermediate steps ({len(steps)} tool calls)"):
                        for i, step in enumerate(steps):
                            st.markdown(f"**Step {i+1}: `{step.get('tool', 'unknown')}`**")
                            inp = step.get('input', '')
                            if isinstance(inp, dict):
                                inp = json.dumps(inp, indent=2)
                            st.code(str(inp)[:500], language="text")
                            st.caption(step.get('output_preview', '')[:400])
                            st.markdown("---")

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("💡 Check your Gemini API key and try again.")