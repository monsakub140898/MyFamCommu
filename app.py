import streamlit as st
from supabase import create_client, Client
import uuid
from datetime import datetime

# ---------------------------------------------------------
# 1. Page Configuration (Mobile-First)
# ---------------------------------------------------------
st.set_page_config(
    page_title="MyFamCommu",
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

# Initialize Session State for Generation
if "gen_level" not in st.session_state:
    st.session_state.gen_level = 0

def dec_gen():
    if st.session_state.gen_level > 0:
        st.session_state.gen_level -= 1

def inc_gen():
    if st.session_state.gen_level < 10:
        st.session_state.gen_level += 1

# ---------------------------------------------------------
# 3. Custom Pastel World & Fancy UI CSS
# ---------------------------------------------------------
st.markdown("""
<style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;500;600;700&family=Sarabun:wght@300;400;500;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Fredoka', 'Sarabun', -apple-system, BlinkMacSystemFont, sans-serif;
        background-color: #FAF7F2;
        color: #4A443F;
    }

    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 4rem;
        max-width: 480px;
        margin: 0 auto;
    }

    /* Header Styling */
    .app-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #5C5248;
        letter-spacing: -0.01em;
        text-align: center;
        margin-bottom: 2px;
    }
    
    .app-subtitle {
        font-size: 0.88rem;
        color: #A09385;
        text-align: center;
        margin-bottom: 1.5rem;
        font-weight: 500;
    }

    .section-title {
        font-size: 0.82rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        color: #8C8275;
        margin: 0.5rem 0 0.8rem 0;
        text-align: center;
    }

    .input-label {
        font-size: 0.82rem;
        font-weight: 600;
        color: #7A6F64;
        margin-bottom: 4px;
    }

    /* =========================================================
       1. แท็บเมนู (Tabs Navigation)
       ========================================================= */
    div[data-testid="stTabs"] [data-baseweb="tab-list"] {
        gap: 8px !important;
        background-color: #F5EFE6 !important;
        padding: 6px 8px !important;
        border-radius: 20px !important;
        border: 1px solid #EADBCE !important;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.03) !important;
    }

    div[data-testid="stTabs"] button[data-baseweb="tab"] {
        border-radius: 14px !important;
        padding: 8px 18px !important;
        font-size: 0.92rem !important;
        font-weight: 600 !important;
        color: #7A6F64 !important;
        border: none !important;
        background: transparent !important;
        transition: all 0.28s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
    }

    div[data-testid="stTabs"] button[data-baseweb="tab"]:hover {
        color: #E11D48 !important;
        background: rgba(255, 255, 255, 0.7) !important;
        transform: translateY(-2px) scale(1.02) !important;
    }

    div[data-testid="stTabs"] button[aria-selected="true"] {
        background: linear-gradient(135deg, #FFB7B2 0%, #FFDAC1 100%) !important;
        color: #8D2B44 !important;
        box-shadow: 0 4px 14px rgba(255, 154, 162, 0.45) !important;
        transform: translateY(-1px) !important;
    }

    div[data-testid="stTabs"] [data-baseweb="tab-highlight-title"],
    div[data-testid="stTabs"] [data-baseweb="tab-border"] {
        display: none !important;
    }

    /* =========================================================
       2. Radio Segmented Control (พาสเทลน่ารัก + ซ่อนจุดสนิท)
       ========================================================= */
    div[data-testid="stRadio"] > div[role="radiogroup"] {
        display: flex !important;
        flex-direction: row !important;
        width: 100% !important;
        gap: 4px !important;
        background-color: #FFF0F3 !important;
        padding: 4px !important;
        border-radius: 16px !important;
        border: 1px solid #FFE2E7 !important;
    }

    div[data-testid="stRadio"] [role="radiogroup"] label > div:first-child,
    div[data-testid="stRadio"] [role="radiogroup"] label input[type="radio"] {
        display: none !important;
    }

    div[data-testid="stRadio"] label {
        flex: 1 !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        background: transparent !important;
        padding: 6px 12px !important;
        border-radius: 12px !important;
        transition: all 0.25s ease !important;
        cursor: pointer !important;
        border: none !important;
        margin: 0 !important;
    }

    div[data-testid="stRadio"] label [data-testid="stMarkdownContainer"] p {
        white-space: nowrap !important;
        font-size: 0.88rem !important;
        font-weight: 600 !important;
        color: #A08C82 !important;
    }

    div[data-testid="stRadio"] label[data-checked="true"] {
        background: #FFFFFF !important;
        box-shadow: 0 3px 10px rgba(255, 154, 162, 0.35) !important;
    }

    div[data-testid="stRadio"] label[data-checked="true"] [data-testid="stMarkdownContainer"] p {
        color: #FF5E7E !important;
        font-weight: 700 !important;
    }

    /* =========================================================
       3. Generation Stepper (แยกปุ่ม + / - ออกมาอยู่นอกกรอบข้อความ)
       ========================================================= */
    /* ซ่อนปุ่ม +/- ดั้งเดิมที่ซ้อนอยู่ข้างใน number_input */
    div[data-testid="stNumberInput"] button {
        display: none !important;
    }

    /* ตกแต่งกรอบตัวเลขตรงกลางให้อยู่สัดส่วนสวยงาม */
    div[data-testid="stNumberInput"] input {
        text-align: center !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        color: #4A443F !important;
        background-color: #F8F6F0 !important;
        border-radius: 14px !important;
        border: 1px solid #EADBCE !important;
    }

    /* ตกแต่งปุ่ม + และ - นอกกรอบให้แยกเป็นปุ่มทรงแคปซูล/สี่เหลี่ยมมน */
    div[data-testid="stColumn"] button[kind="secondary"] {
        background-color: #FFF0F3 !important;
        color: #FF5E7E !important;
        border: 1px solid #FFE2E7 !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        box-shadow: 0 2px 6px rgba(255, 154, 162, 0.15) !important;
        transition: all 0.2s ease !important;
    }

    div[data-testid="stColumn"] button[kind="secondary"]:hover {
        background-color: #FFDDE2 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 10px rgba(255, 154, 162, 0.25) !important;
    }

    /* =========================================================
       4. Main Submit Form Button
       ========================================================= */
    div[data-testid="stFormSubmitButton"] > button {
        background: linear-gradient(135deg, #FFB7B2 0%, #FF9AA2 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 16px !important;
        font-weight: 700 !important;
        font-size: 0.98rem !important;
        padding: 0.75rem 1.2rem !important;
        box-shadow: 0 6px 18px rgba(255, 154, 162, 0.4) !important;
        transition: all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
        cursor: pointer !important;
    }

    div[data-testid="stFormSubmitButton"] > button:hover {
        background: linear-gradient(135deg, #FF9AA2 0%, #FF8B94 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 22px rgba(255, 139, 148, 0.5) !important;
    }

    /* =========================================================
       5. CSS Pastel Tree Container
       ========================================================= */
    .tree-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 16px;
        padding: 24px 14px;
        background: #FFFFFF;
        border: 2px solid #F3ECE1;
        border-radius: 24px;
        box-shadow: 0 10px 25px rgba(235, 222, 208, 0.4);
        margin-bottom: 20px;
    }

    .tree-level {
        display: flex;
        justify-content: center;
        gap: 14px;
        flex-wrap: wrap;
        width: 100%;
    }

    .tree-node-link {
        text-decoration: none !important;
        color: inherit !important;
        display: inline-block;
    }

    .tree-node {
        display: flex;
        flex-direction: column;
        align-items: center;
        background: #FFFFFF;
        border-radius: 18px;
        padding: 12px 14px;
        min-width: 92px;
        transition: all 0.25s ease;
        cursor: pointer;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
    }

    .tree-node:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
    }

    .tree-avatar-img {
        width: 58px;
        height: 58px;
        border-radius: 50%;
        object-fit: cover;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.06);
        margin-bottom: 8px;
    }

    .tree-avatar-placeholder {
        width: 58px;
        height: 58px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.6rem;
        margin-bottom: 8px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
    }

    .tree-node-name {
        font-size: 0.88rem;
        font-weight: 600;
        color: #4A443F;
        text-align: center;
    }

    .tree-connector {
        width: 3px;
        height: 18px;
        background: linear-gradient(180deg, #FDE68A 0%, #BAE6FD 100%);
        border-radius: 3px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Pastel Color Palette System
# ---------------------------------------------------------
PASTEL_PALETTE = [
    {"bg": "#FFF0F2", "color": "#E11D48", "border": "#FFCCE1", "badge_bg": "#FFE4E6"}, # Gen 0
    {"bg": "#FEFCE8", "color": "#D97706", "border": "#FEF08A", "badge_bg": "#FEF3C7"}, # Gen 1
    {"bg": "#F0FDF4", "color": "#16A34A", "border": "#BBF7D0", "badge_bg": "#DCFCE7"}, # Gen 2
    {"bg": "#F0F9FF", "color": "#0284C7", "border": "#BAE6FD", "badge_bg": "#E0F2FE"}, # Gen 3
    {"bg": "#FAF5FF", "color": "#9333EA", "border": "#E9D5FF", "badge_bg": "#F3E8FF"}, # Gen 4
]

# ---------------------------------------------------------
# 4. App Header & Data Fetching
# ---------------------------------------------------------
st.markdown("<div class='app-title'>MyFamCommu 🐾</div>", unsafe_allow_html=True)
st.markdown("<div class='app-subtitle'>แผนผังครอบครัว 🌸🌼🩵</div>", unsafe_allow_html=True)

def fetch_members():
    try:
        response = supabase.table("members").select("*").order("gen_level", desc=False).execute()
        return response.data
    except Exception as e:
        st.error(f"ไม่สามารถเชื่อมต่อฐานข้อมูลได้: {e}")
        return []

# ---------------------------------------------------------
# 5. Dialog Function for Member Details Modal
# ---------------------------------------------------------
def render_member_dialog(m):
    @st.dialog("📄 รายละเอียดสมาชิก")
    def show_modal():
        if m.get('image_url'):
            st.image(m['image_url'], use_container_width=True)
        
        st.markdown(f"### {m['name']}")
        st.markdown(f"**ประเภท:** `{m['type']} ({m['species']})`")
        st.markdown(f"**เพศ:** {m['gender']} | **รุ่น:** Gen {m.get('gen_level', 0)}")
        
        if m.get('birth_date'):
            st.markdown(f"**วันเกิด:** {m['birth_date']}")
        if m.get('father') or m.get('mother'):
            st.markdown(f"**พ่อ / แม่:** {m.get('father', '-')} / {m.get('mother', '-')}")
        if m.get('notes'):
            st.markdown(f"**บันทึกย่อ:** {m['notes']}")
            
        st.divider()
        
        col_del, col_close = st.columns(2)
        with col_del:
            if st.button("🗑️ ลบข้อมูล", key=f"modal_del_{m['id']}", use_container_width=True, type="primary"):
                try:
                    if m.get('image_url'):
                        try:
                            raw_filename = m['image_url'].split('/')[-1]
                            file_name = raw_filename.split('?')[0]
                            supabase.storage.from_("fam-photos").remove([file_name])
                        except Exception as img_err:
                            st.error(f"ไม่สามารถลบรูปภาพจาก Storage ได้: {img_err}")
                    
                    supabase.table("members").delete().eq("id", m["id"]).execute()
                    st.success(f"ลบ {m['name']} เรียบร้อยแล้วครับ")
                    st.query_params.clear()
                    st.rerun()
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาดในการลบข้อมูล: {e}")
                    
        with col_close:
            if st.button("ปิด", key="modal_close", use_container_width=True):
                st.query_params.clear()
                st.rerun()
                
    show_modal()

# ---------------------------------------------------------
# Tabs Navigation
# ---------------------------------------------------------
tab1, tab2 = st.tabs(["🌳 ผังครอบครัว", "➕ เพิ่มสมาชิก"])

# ---------------------------------------------------------
# Tab 1: ผังครอบครัว
# ---------------------------------------------------------
with tab1:
    data = fetch_members()
    
    if not data:
        st.markdown(
            '<div style="text-align: center; padding: 40px 20px; background-color: #FFFFFF; border: 2px solid #F3ECE1; border-radius: 24px; margin-top: 12px; box-shadow: 0 6px 16px rgba(0,0,0,0.02);">'
            '<p style="font-size: 2.5rem; margin-bottom: 8px;">🐱🌸🐶</p>'
            '<p style="color: #5C5248; font-weight: 600; font-size: 1.05rem; margin-bottom: 4px;">ยังไม่มีข้อมูลสมาชิกในบ้าน</p>'
            '<p style="color: #A09385; font-size: 0.85rem; margin: 0;">กดที่แท็บ <b>"➕ เพิ่มสมาชิก"</b> เพื่อเพิ่มสมาชิก</p>'
            '</div>', 
            unsafe_allow_html=True
        )
    else:
        st.markdown("<div class='section-title'>🏡 แผนผังครอบครัว (คลิกที่รูปเพื่อดูรายละเอียด)</div>", unsafe_allow_html=True)
        
        if "selected_id" in st.query_params:
            sel_id = st.query_params["selected_id"]
            selected_m = next((m for m in data if str(m["id"]) == str(sel_id)), None)
            if selected_m:
                render_member_dialog(selected_m)
        
        unique_gens = sorted(list(set(m.get('gen_level', 0) for m in data)))
        
        tree_blocks = ["<div class='tree-container'>"]
        for idx, gen in enumerate(unique_gens):
            gen_members = [m for m in data if m.get('gen_level', 0) == gen]
            theme = PASTEL_PALETTE[gen % len(PASTEL_PALETTE)]
            
            if idx > 0:
                tree_blocks.append("<div class='tree-connector'></div>")
                
            tree_blocks.append("<div class='tree-level'>")
            for m in gen_members:
                card_style = f"background: {theme['bg']}; border: 1.5px solid {theme['border']};"
                badge_style = f"background: {theme['badge_bg']}; color: {theme['color']}; font-size: 0.68rem; font-weight: 600; padding: 2px 8px; border-radius: 10px; margin-top: 4px;"
                img_border_style = f"border: 3px solid {theme['border']};"
                
                if m.get('image_url'):
                    avatar_html = f'<img src="{m["image_url"]}" class="tree-avatar-img" style="{img_border_style}">'
                else:
                    icon = '🐱' if m.get('type') == 'สัตว์เลี้ยง' else '👤'
                    avatar_html = f'<div class="tree-avatar-placeholder" style="background-color: {theme["badge_bg"]}; {img_border_style}">{icon}</div>'
                
                node_html = f'<a href="?selected_id={m["id"]}" target="_self" class="tree-node-link"><div class="tree-node" style="{card_style}">{avatar_html}<div class="tree-node-name">{m["name"]}</div><div style="{badge_style}">Gen {m.get("gen_level", 0)}</div></div></a>'
                tree_blocks.append(node_html)
            
            tree_blocks.append("</div>")
        tree_blocks.append("</div>")
        
        full_tree_html = "".join(tree_blocks)
        st.markdown(full_tree_html, unsafe_allow_html=True)

# ---------------------------------------------------------
# Tab 2: เพิ่มสมาชิกใหม่
# ---------------------------------------------------------
with tab2:
    st.markdown("<p style='font-size: 0.85rem; color: #A09385; margin-bottom: 0.8rem; text-align: center;'>กรอกรายละเอียดเพื่อบันทึกสมาชิกหรือสัตว์เลี้ยง</p>", unsafe_allow_html=True)
    
    col_type, col_gen = st.columns([1.0, 1.0])
    
    with col_type:
        st.markdown("<div class='input-label'>ประเภทสมาชิก</div>", unsafe_allow_html=True)
        member_type = st.radio(["คน", "สัตว์เลี้ยง"], horizontal=True, label_visibility="collapsed")
        
    with col_gen:
        st.markdown("<div class='input-label'>Generation</div>", unsafe_allow_html=True)
        
        # เลย์เอาต์แยก 3 ช่อง: [ - ] [ 0 ] [ + ]
        g_dec, g_val, g_inc = st.columns([0.8, 1.4, 0.8])
        with g_dec:
            st.button("➖", key="btn_dec_gen", on_click=dec_gen, use_container_width=True)
        with g_val:
            gen_level = st.number_input(
                "Generation", 
                min_value=0, 
                max_value=10, 
                key="gen_level", 
                label_visibility="collapsed"
            )
        with g_inc:
            st.button("➕", key="btn_inc_gen", on_click=inc_gen, use_container_width=True)
    
    existing_members = fetch_members()
    parent_target_gen = gen_level - 1
    
    if gen_level > 0:
        father_options = ["- ไม่ระบุ -"] + [
            m["name"] for m in existing_members 
            if m.get("gender") in ["ชาย", "ผู้"] and m.get("gen_level", 0) == parent_target_gen
        ]
        mother_options = ["- ไม่ระบุ -"] + [
            m["name"] for m in existing_members 
            if m.get("gender") in ["หญิง", "เมีย"] and m.get("gen_level", 0) == parent_target_gen
        ]
    else:
        father_options = ["- ไม่ระบุ -"]
        mother_options = ["- ไม่ระบุ -"]
    
    st.write("")
    
    with st.form("add_member_form", clear_on_submit=True):
        name = st.text_input("ชื่อสมาชิก*")
        
        if member_type == "คน":
            species = "คน"
            gender = st.selectbox("เพศ", ["ชาย", "หญิง", "อื่นๆ"])
        else:
            species = st.selectbox("ชนิดสัตว์เลี้ยง", ["แมว", "หมา", "นก", "กระต่าย", "อื่นๆ"])
            gender = st.selectbox("เพศ", ["ผู้", "เมีย"])
            
        birth_date = st.date_input(
            "วัน/เดือน/ปี เกิด", 
            value=None, 
            min_value=datetime(1900, 1, 1), 
            max_value=datetime.now(),
            format="DD/MM/YYYY"
        )
        
        col_f, col_m = st.columns(2)
        with col_f:
            father = st.selectbox(f"เลือกพ่อ (จาก Gen {parent_target_gen})" if gen_level > 0 else "เลือกพ่อ", father_options)
        with col_m:
            mother = st.selectbox(f"เลือกแม่ (จาก Gen {parent_target_gen})" if gen_level > 0 else "เลือกแม่", mother_options)
            
        notes = st.text_area("บันทึกเพิ่มเติม", placeholder="ใส่บันทึกย่อ นิสัย หรือลักษณะเด่น...")
        uploaded_file = st.file_uploader("📸 รูปถ่ายสมาชิก", type=["jpg", "png", "jpeg"])
        
        submitted = st.form_submit_button("✨ บันทึกข้อมูลสมาชิก", use_container_width=True)
        
        if submitted:
            if not name:
                st.error("กรุณากรอกชื่อสมาชิก")
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
                        "birth_date": birth_date.strftime("%Y-%m-%d") if birth_date else None,
                        "father": father if father != "- ไม่ระบุ -" else None,
                        "mother": mother if mother != "- ไม่ระบุ -" else None,
                        "notes": notes,
                        "image_url": image_url
                    }
                    
                    supabase.table("members").insert(new_member).execute()
                    st.success(f"บันทึก {name} เรียบร้อยแล้ว")
                    st.rerun()
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")