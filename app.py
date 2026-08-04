import streamlit as st
from supabase import create_client, Client
import uuid

# ---------------------------------------------------------
# 1. Page Configuration (Mobile-First)
# ---------------------------------------------------------
st.set_page_config(
    page_title="My Fam Commu",
    page_icon="🐾",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# 2. Supabase Connection
# ---------------------------------------------------------
SUPABASE_URL = "https://zqeiswjafwwzemygmjcl.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpxZWlzd2phZnd3emVteWdtamNsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODU4MTcyMzYsImV4cCI6MjEwMTM5MzIzNn0.9yV7BAYCiwUyk3NQmtZ5bLfUrPmirWGnY7rgga2BA64"

@st.cache_resource
def init_supabase() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_supabase()

# ---------------------------------------------------------
# 3. Custom Minimalist CSS (Claude Aesthetic)
# ---------------------------------------------------------
st.markdown("""
<style>
    /* Hide Streamlit default headers/footers */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    
    /* Global Typography & Background */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Sarabun:wght@300;400;500;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', 'Sarabun', -apple-system, BlinkMacSystemFont, sans-serif;
        background-color: #FBFBFA;
        color: #242423;
    }

    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 4rem;
        max-width: 480px;
        margin: 0 auto;
    }

    /* Minimal Title Header */
    .app-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1A1A18;
        letter-spacing: -0.02em;
        text-align: center;
        margin-bottom: 2px;
    }
    
    .app-subtitle {
        font-size: 0.8rem;
        color: #8C8A85;
        text-align: center;
        margin-bottom: 1.2rem;
        font-weight: 400;
    }

    /* Minimal Gen Section Header */
    .gen-header {
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #8C8A85;
        margin: 1.5rem 0 0.6rem 0;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .gen-header::after {
        content: "";
        flex-grow: 1;
        height: 1px;
        background-color: #EFEFEA;
    }

    /* Card Styling */
    .member-card {
        background: #FFFFFF;
        border: 1px solid #EAEAE6;
        border-radius: 12px;
        padding: 12px 16px;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 14px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    }

    .avatar-img {
        width: 48px;
        height: 48px;
        border-radius: 50%;
        object-fit: cover;
        border: 1px solid #EFEFEA;
        flex-shrink: 0;
    }
    
    .avatar-placeholder {
        width: 48px;
        height: 48px;
        border-radius: 50%;
        background-color: #F4F4F0;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.3rem;
        flex-shrink: 0;
        border: 1px solid #EFEFEA;
    }

    .member-name {
        font-size: 0.95rem;
        font-weight: 600;
        color: #1A1A18;
        margin: 0;
    }

    .member-sub {
        font-size: 0.78rem;
        color: #706F6C;
        margin-top: 2px;
    }

    .badge-tag {
        display: inline-block;
        padding: 1px 7px;
        border-radius: 4px;
        font-size: 0.68rem;
        font-weight: 500;
        background-color: #F3F3EE;
        color: #575653;
        margin-left: 6px;
    }

    /* Streamlit Tab Customization */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #F4F4F0;
        padding: 4px;
        border-radius: 10px;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 6px 16px;
        font-size: 0.85rem;
        font-weight: 500;
        color: #706F6C;
        border: none;
    }

    .stTabs [aria-selected="true"] {
        background-color: #FFFFFF !important;
        color: #1A1A18 !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }

    /* Form Submit Button (Terracotta Accent) */
    div[data-testid="stFormSubmitButton"] > button {
        background-color: #D97757 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 0.5rem 1rem !important;
        transition: all 0.2s ease;
    }
    div[data-testid="stFormSubmitButton"] > button:hover {
        background-color: #C06142 !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. App Header
# ---------------------------------------------------------
st.markdown("<div class='app-title'>My Fam Commu</div>", unsafe_allow_html=True)
st.markdown("<div class='app-subtitle'>Family Tree & Pet Records</div>", unsafe_allow_html=True)

# Helper function
def fetch_members():
    try:
        response = supabase.table("members").select("*").order("gen_level", desc=False).execute()
        return response.data
    except Exception as e:
        st.error(f"ไม่สามารถเชื่อมต่อฐานข้อมูลได้: {e}")
        return []

# Navigation Tabs
tab1, tab2 = st.tabs(["🌳 ผังครอบครัว", "➕ เพิ่มสมาชิก"])

# ---------------------------------------------------------
# Tab 1: ผังครอบครัว (Minimal Family Tree)
# ---------------------------------------------------------
with tab1:
    data = fetch_members()
    
    if not data:
        st.markdown("""
        <div style="text-align: center; padding: 36px 16px; background-color: #FFFFFF; border: 1px solid #EAEAE6; border-radius: 12px; margin-top: 12px;">
            <p style="font-size: 2rem; margin-bottom: 8px;">🐾</p>
            <p style="color: #1A1A18; font-weight: 600; font-size: 0.95rem; margin-bottom: 4px;">ยังไม่มีข้อมูลสมาชิก</p>
            <p style="color: #8C8A85; font-size: 0.8rem; margin: 0;">เริ่มต้นเพิ่มสมาชิกคนแรกได้ที่แท็บ <b>"➕ เพิ่มสมาชิก"</b></p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for gen in range(6):
            members_in_gen = [m for m in data if m.get("gen_level") == gen]
            if members_in_gen:
                st.markdown(f"<div class='gen-header'>Generation {gen}</div>", unsafe_allow_html=True)
                
                for m in members_in_gen:
                    # Avatar
                    if m.get('image_url'):
                        img_html = f"<img src='{m['image_url']}' class='avatar-img'>"
                    else:
                        icon = '🐱' if m['type'] == 'สัตว์เลี้ยง' else '👤'
                        img_html = f"<div class='avatar-placeholder'>{icon}</div>"
                    
                    # Card
                    card_html = f"""
                    <div class="member-card">
                        {img_html}
                        <div style="flex-grow: 1;">
                            <div class="member-name">
                                {m['name']}
                                <span class="badge-tag">{m['species']}</span>
                            </div>
                            <div class="member-sub">เพศ: {m['gender']}</div>
                        </div>
                    </div>
                    """
                    st.markdown(card_html, unsafe_allow_html=True)
                    
                    # Profile Detail & Delete
                    with st.expander(f"ข้อมูลของ {m['name']}"):
                        if m.get('image_url'):
                            st.image(m['image_url'], use_container_width=True)
                        st.write(f"**ประเภท:** {m['type']} ({m['species']})")
                        st.write(f"**เพศ:** {m['gender']} | **รุ่น:** Gen {m['gen_level']}")
                        if m.get('father') or m.get('mother'):
                            st.write(f"**พ่อ-แม่:** {m.get('father', '-')} / {m.get('mother', '-')}")
                        if m.get('notes'):
                            st.write(f"**บันทึก:** {m['notes']}")
                        
                        st.divider()
                        if st.button(f"🗑️ ลบ {m['name']}", key=f"del_{m['id']}", use_container_width=True):
                            try:
                                supabase.table("members").delete().eq("id", m["id"]).execute()
                                st.success(f"ลบ {m['name']} เรียบร้อยแล้ว")
                                st.rerun()
                            except Exception as e:
                                st.error(f"เกิดข้อผิดพลาด: {e}")

# ---------------------------------------------------------
# Tab 2: เพิ่มสมาชิกใหม่ (Clean Form)
# ---------------------------------------------------------
with tab2:
    st.markdown("<p style='font-size: 0.9rem; color: #706F6C; margin-bottom: 1rem;'>กรอกรายละเอียดเพื่อบันทึกสมาชิกเข้าสู่ระบบ</p>", unsafe_allow_html=True)
    
    member_type = st.radio("ประเภทสมาชิก", ["คน", "สัตว์เลี้ยง"], horizontal=True, label_visibility="collapsed")
    
    existing_members = fetch_members()
    member_names = ["- ไม่ระบุ -"] + [m["name"] for m in existing_members]
    
    with st.form("add_member_form"):
        name = st.text_input("ชื่อสมาชิก*")
        
        if member_type == "คน":
            species = "คน"
            gender = st.selectbox("เพศ", ["ชาย", "หญิง", "อื่นๆ"])
        else:
            species = st.selectbox("ชนิดสัตว์เลี้ยง", ["แมว", "หมา", "นก", "กระต่าย", "อื่นๆ"])
            gender = st.selectbox("เพศ", ["ผู้", "เมีย"])
            
        gen_level = st.number_input("Generation (0, 1, 2...)", min_value=0, max_value=10, value=0)
        
        col_f, col_m = st.columns(2)
        with col_f:
            father = st.selectbox("เลือกพ่อ", member_names)
        with col_m:
            mother = st.selectbox("เลือกแม่", member_names)
            
        notes = st.text_area("บันทึกเพิ่มเติม / พัฒนาการ", placeholder="ใส่บันทึกย่อหรือลักษณะเด่น...")
        uploaded_file = st.file_uploader("📸 รูปถ่ายสมาชิก", type=["jpg", "png", "jpeg"])
        
        submitted = st.form_submit_button("บันทึกข้อมูล", use_container_width=True)
        
        if submitted:
            if not name:
                st.error("กรุณากรอกชื่อสมาชิกด้วยครับ")
            else:
                try:
                    image_url = None
                    if uploaded_file is not None:
                        file_ext = uploaded_file.name.split(".")[-1]
                        file_path = f"{uuid.uuid4()}.{file_ext}"
                        
                        supabase.storage.from_("fam-photos").upload(
                            path=file_path,
                            file=uploaded_file.getvalue(),
                            file_options={"content-type": uploaded_file.type}
                        )
                        image_url = supabase.storage.from_("fam-photos").get_public_url(file_path)
                    
                    new_member = {
                        "name": name,
                        "type": member_type,
                        "species": species,
                        "gender": gender,
                        "gen_level": int(gen_level),
                        "father": father if father != "- ไม่ระบุ -" else None,
                        "mother": mother if mother != "- ไม่ระบุ -" else None,
                        "notes": notes,
                        "image_url": image_url
                    }
                    
                    supabase.table("members").insert(new_member).execute()
                    st.success(f"บันทึก {name} สำเร็จ")
                    st.rerun()
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")