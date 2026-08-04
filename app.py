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

# ---------------------------------------------------------
# 3. Custom Pastel World & Smooth Font CSS
# ---------------------------------------------------------
st.markdown("""
<style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    
    @import url('https://fonts.googleapis.com/css2?family=Mitr:wght@300;400;500;600&family=Outfit:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', 'Mitr', -apple-system, BlinkMacSystemFont, sans-serif;
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

    /* =========================================================
       1. แท็บเมนู (Tabs Navigation)
       ========================================================= */
    div[data-testid="stTabs"] {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        width: 100% !important;
    }

    div[data-testid="stTabs"] div[data-baseweb="tab-list"] {
        display: flex !important;
        justify-content: center !important;
        gap: 8px !important;
        background-color: #F5EFE6 !important;
        padding: 6px 8px !important;
        border-radius: 20px !important;
        border: 1px solid #EADBCE !important;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.03) !important;
        margin-left: auto !important;
        margin-right: auto !important;
        width: fit-content !important;
    }

    div[data-testid="stTabs"] button[data-baseweb="tab"] {
        border-radius: 14px !important;
        padding: 6px 14px !important;
        font-size: 0.88rem !important;
        font-weight: 600 !important;
        color: #7A6F64 !important;
        border: none !important;
        background: transparent !important;
        transition: all 0.28s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
    }

    div[data-testid="stTabs"] button[data-baseweb="tab"]:hover {
        color: #E11D48 !important;
        background: rgba(255, 255, 255, 0.7) !important;
        transform: translateY(-1px) scale(1.01) !important;
    }

    div[data-testid="stTabs"] button[aria-selected="true"] {
        background: linear-gradient(135deg, #FFB7B2 0%, #FFDAC1 100%) !important;
        color: #8D2B44 !important;
        box-shadow: 0 3px 10px rgba(255, 154, 162, 0.35) !important;
        transform: translateY(0px) !important;
    }

    div[data-testid="stTabs"] [data-baseweb="tab-highlight-title"],
    div[data-testid="stTabs"] [data-baseweb="tab-border"] {
        display: none !important;
    }

    /* =========================================================
       2. Radio Segmented Control
       ========================================================= */
    div[data-testid="stRadio"] > div[role="radiogroup"] {
        display: flex !important;
        flex-direction: row !important;
        width: 100% !important;
        gap: 4px !important;
        background-color: #FFF0F3 !important;
        padding: 4px !important;
        border-radius: 14px !important;
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
        padding: 4px 10px !important;
        border-radius: 10px !important;
        transition: all 0.25s ease !important;
        cursor: pointer !important;
        border: none !important;
        margin: 0 !important;
    }

    div[data-testid="stRadio"] label [data-testid="stMarkdownContainer"] p {
        white-space: nowrap !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        color: #A08C82 !important;
    }

    div[data-testid="stRadio"] label[data-checked="true"] {
        background: #FFFFFF !important;
        box-shadow: 0 2px 6px rgba(255, 154, 162, 0.25) !important;
    }

    div[data-testid="stRadio"] label[data-checked="true"] [data-testid="stMarkdownContainer"] p {
        color: #FF5E7E !important;
        font-weight: 700 !important;
    }

    /* =========================================================
       3. Button Styling (Custom Secondary & Primary Buttons)
       ========================================================= */
    div.stButton {
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
    }

    /* ปุ่มรองทั่วไป (Secondary) -> สีเขียวพาสเทลละมุน */
    div.stButton > button:not([kind="primary"]) {
        background: linear-gradient(135deg, #E2ECE9 0%, #D4E2DE) !important;
        color: #3D5A5B !important;
        border: 1.5px solid #C4D6D2 !important;
        border-radius: 14px !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        padding: 0.5rem 0.8rem !important;
        min-height: 44px !important;
        width: 100% !important;
        transition: all 0.25s ease !important;
    }

    div.stButton > button:not([kind="primary"]):hover {
        background: linear-gradient(135deg, #D4E2DE 0%, #C4D6D2) !important;
        color: #2C4243 !important;
        border-color: #B2C8C3 !important;
    }

    /* ปุ่มแก้ไขข้อมูล -> สีฟ้าอ่อนพาสเทลที่ชัดเจนและขนาดเท่ากันเป๊ะ */
    .pastel-blue-btn button {
        background: linear-gradient(135deg, #E0F2FE 0%, #BAE6FD 100%) !important;
        color: #0284C7 !important;
        border: 1.5px solid #7DD3FC !important;
        border-radius: 14px !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        padding: 0.5rem 0.8rem !important;
        min-height: 44px !important;
        width: 100% !important;
        box-shadow: 0 4px 12px rgba(186, 230, 253, 0.4) !important;
        transition: all 0.25s ease !important;
    }

    .pastel-blue-btn button:hover {
        background: linear-gradient(135deg, #BAE6FD 0%, #38BDF8 100%) !important;
        color: #0369A1 !important;
        border-color: #0284C7 !important;
        transform: translateY(-1px) !important;
    }

    /* ปุ่มหลัก / ลบข้อมูล (Primary) -> สีชมพูพีช-แดงละมุน และขนาดเท่ากัน */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #FF5E7E 0%, #FF3366 100%) !important;
        color: #FFFFFF !important;
        border: 1.5px solid #FF3366 !important;
        border-radius: 14px !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        padding: 0.5rem 0.8rem !important;
        min-height: 44px !important;
        width: 100% !important;
        box-shadow: 0 4px 12px rgba(255, 94, 126, 0.3) !important;
        transition: all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
    }

    div.stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #FF3366 0%, #E11D48 100%) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 16px rgba(225, 29, 72, 0.4) !important;
    }

    div[data-testid="stFormSubmitButton"] {
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
    }

    div[data-testid="stFormSubmitButton"] > button {
        background: linear-gradient(135deg, #FF5E7E 0%, #FF3366 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 14px !important;
        font-weight: 700 !important;
        font-size: 0.92rem !important;
        padding: 0.6rem 1rem !important;
        min-height: 44px !important;
        width: 80% !important;
        margin: 0 auto !important;
        box-shadow: 0 6px 16px rgba(255, 94, 126, 0.3) !important;
        transition: all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
        cursor: pointer !important;
    }

    div[data-testid="stFormSubmitButton"] > button:hover {
        background: linear-gradient(135deg, #FF3366 0%, #E11D48 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(225, 29, 72, 0.4) !important;
    }

    /* =========================================================
       4. CSS Pastel Tree Container
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

    div[data-testid="stDialog"] div[data-testid="stVerticalBlock"] {
        gap: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Pastel Color Palette System
# ---------------------------------------------------------
PASTEL_PALETTE = [
    {"bg": "#FFF0F2", "color": "#E11D48", "border": "#FFCCE1", "badge_bg": "#FFE4E6"}, # Gen 1
    {"bg": "#FEFCE8", "color": "#D97706", "border": "#FEF08A", "badge_bg": "#FEF3C7"}, # Gen 2
    {"bg": "#F0FDF4", "color": "#16A34A", "border": "#BBF7D0", "badge_bg": "#DCFCE7"}, # Gen 3
    {"bg": "#F0F9FF", "color": "#0284C7", "border": "#BAE6FD", "badge_bg": "#E0F2FE"}, # Gen 4
    {"bg": "#FAF5FF", "color": "#9333EA", "border": "#E9D5FF", "badge_bg": "#F3E8FF"}, # Gen 5
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
        st.error(f"ไม่สามารถเชื่อมต่อฐานข้อมูลได้ : {e}")
        return []

# ---------------------------------------------------------
# 5. Dialog Function for Member Details Modal with Edit, Edit Confirmation & Delete
# ---------------------------------------------------------
def render_member_dialog(m):
    @st.dialog("รายละเอียดสมาชิก")
    def show_modal():
        del_key = f"confirm_del_{m['id']}"
        edit_key = f"is_editing_{m['id']}"
        edit_confirm_key = f"show_edit_confirm_{m['id']}"
        pending_edit_key = f"pending_edit_data_{m['id']}"
        
        if del_key not in st.session_state:
            st.session_state[del_key] = False
        if edit_key not in st.session_state:
            st.session_state[edit_key] = False
        if edit_confirm_key not in st.session_state:
            st.session_state[edit_confirm_key] = False
        if pending_edit_key not in st.session_state:
            st.session_state[pending_edit_key] = None

        # 1. หน้าจอตรวจสอบและยืนยันการแก้ไขข้อมูล
        if st.session_state[edit_confirm_key] and st.session_state[pending_edit_key]:
            pem = st.session_state[pending_edit_key]
            st.markdown("<div class='section-title'>✨ ตรวจสอบข้อมูลก่อนยืนยันการแก้ไข</div>", unsafe_allow_html=True)
            st.markdown(
                f"""
                <div style='background: #FFFFFF; border: 2px solid #BAE6FD; padding: 18px; border-radius: 20px; margin-bottom: 16px; box-shadow: 0 8px 20px rgba(186, 230, 253, 0.25);'>
                    <div style='font-size: 1.05rem; font-weight: 700; color: #0369A1; margin-bottom: 10px; text-align: center; border-bottom: 1px solid #E0F2FE; padding-bottom: 8px;'>📋 ข้อมูลที่แก้ไขใหม่</div>
                    <div style='font-size: 0.9rem; color: #4A443F; display: flex; flex-direction: column; gap: 6px;'>
                        <div><b>ชื่อ :</b> {pem['name']}</div>
                        <div><b>ประเภท :</b> {pem['type']} ({pem['species']})</div>
                        <div><b>เพศ :</b> {pem['gender']} &nbsp;|&nbsp; <b>รุ่น:</b> Gen {pem['gen_level']}</div>
                        <div><b>วันเกิด :</b> {pem['birth_date'] if pem['birth_date'] else '-'}</div>
                        <div><b>พ่อ / แม่ :</b> {pem['father'] if pem['father'] else '-'} / {pem['mother'] if pem['mother'] else '-'}</div>
                        <div><b>บันทึกเพิ่มเติม :</b> {pem['notes'] if pem['notes'] else '-'}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            col_edit_yes, col_edit_no = st.columns(2)
            with col_edit_yes:
                if st.button("✓ ยืนยันการแก้ไข", key=f"confirm_edit_yes_{m['id']}", use_container_width=True, type="primary"):
                    try:
                        image_url = m.get('image_url')
                        if pem['file_bytes'] is not None:
                            file_ext = pem['file_name'].split(".")[-1]
                            file_path = f"{uuid.uuid4()}.{file_ext}"
                            supabase.storage.from_("fam-photos").upload(
                                path=file_path,
                                file=pem['file_bytes'],
                                file_options={"content-type": pem['file_type']}
                            )
                            image_url = supabase.storage.from_("fam-photos").get_public_url(file_path)
                            
                            if m.get('image_url'):
                                try:
                                    old_filename = m['image_url'].split('/')[-1].split('?')[0]
                                    supabase.storage.from_("fam-photos").remove([old_filename])
                                except:
                                    pass

                        updated_data = {
                            "name": pem['name'],
                            "type": pem['type'],
                            "species": pem['species'],
                            "gender": pem['gender'],
                            "gen_level": int(pem['gen_level']),
                            "birth_date": pem['birth_date'],
                            "father": pem['father'],
                            "mother": pem['mother'],
                            "notes": pem['notes'],
                            "image_url": image_url
                        }
                        
                        supabase.table("members").update(updated_data).eq("id", m["id"]).execute()
                        st.success(f"แก้ไขข้อมูล {pem['name']} เรียบร้อยแล้ว")
                        st.session_state[edit_confirm_key] = False
                        st.session_state[edit_key] = False
                        st.session_state[pending_edit_key] = None
                        st.query_params.clear()
                        st.rerun()
                    except Exception as e:
                        st.error(f"เกิดข้อผิดพลาดในการแก้ไขข้อมูล: {e}")
            with col_edit_no:
                if st.button("✕ ยกเลิก", key=f"confirm_edit_no_{m['id']}", use_container_width=True):
                    st.session_state[edit_confirm_key] = False
                    st.rerun()

        # 2. หน้าจอฟอร์มแก้ไขข้อมูล
        elif st.session_state[edit_key]:
            st.markdown("<div class='section-title'>✨ แก้ไขข้อมูลสมาชิก</div>", unsafe_allow_html=True)
            
            with st.form(f"edit_form_{m['id']}"):
                edit_name = st.text_input("ชื่อสมาชิก*", value=m['name'])
                
                edit_type = st.selectbox("ประเภทสมาชิก", ["คน", "สัตว์เลี้ยง"], index=0 if m.get('type') == 'คน' else 1)
                
                if edit_type == "คน":
                    edit_species = "คน"
                    gender_options = ["ชาย", "หญิง", "อื่นๆ"]
                    curr_gender = m.get('gender', 'ชาย')
                    edit_gender = st.selectbox("เพศ", gender_options, index=gender_options.index(curr_gender) if curr_gender in gender_options else 0)
                else:
                    species_options = ["แมว", "หมา", "นก", "กระต่าย", "อื่นๆ"]
                    curr_species = m.get('species', 'แมว')
                    edit_species = st.selectbox("ชนิดสัตว์เลี้ยง", species_options, index=species_options.index(curr_species) if curr_species in species_options else 0)
                    gender_options = ["ผู้", "เมีย"]
                    curr_gender = m.get('gender', 'ผู้')
                    edit_gender = st.selectbox("เพศ", gender_options, index=gender_options.index(curr_gender) if curr_gender in gender_options else 0)
                
                edit_gen = st.number_input("Generation", min_value=1, max_value=10, value=int(m.get('gen_level', 1)), step=1)
                
                try:
                    default_date = datetime.strptime(m['birth_date'], "%Y-%m-%d") if m.get('birth_date') else None
                except:
                    default_date = None
                    
                edit_birth_date = st.date_input("วัน/เดือน/ปี เกิด", value=default_date, min_value=datetime(1900, 1, 1), max_value=datetime.now(), format="DD/MM/YYYY")
                
                existing_members = fetch_members()
                parent_target_gen = edit_gen - 1
                if edit_gen > 1:
                    father_options = ["- ไม่ระบุ -"] + [item["name"] for item in existing_members if item.get("gender") in ["ชาย", "ผู้"] and item.get("gen_level", 1) == parent_target_gen and item["id"] != m["id"]]
                    mother_options = ["- ไม่ระบุ -"] + [item["name"] for item in existing_members if item.get("gender") in ["หญิง", "เมีย"] and item.get("gen_level", 1) == parent_target_gen and item["id"] != m["id"]]
                else:
                    father_options = ["- ไม่ระบุ -"]
                    mother_options = ["- ไม่ระบุ -"]
                    
                f_default = m.get('father') if m.get('father') in father_options else "- ไม่ระบุ -"
                m_default = m.get('mother') if m.get('mother') in mother_options else "- ไม่ระบุ -"
                f_idx = father_options.index(f_default) if f_default in father_options else 0
                m_idx = mother_options.index(m_default) if m_default in mother_options else 0
                
                col_f, col_m = st.columns(2)
                with col_f:
                    edit_father = st.selectbox("เลือกพ่อ", father_options, index=f_idx)
                with col_m:
                    edit_mother = st.selectbox("เลือกแม่", mother_options, index=m_idx)
                    
                edit_notes = st.text_area("บันทึกเพิ่มเติม", value=m.get('notes', ''))
                edit_uploaded_file = st.file_uploader("📸 เปลี่ยนรูปถ่าย (ถ้าต้องการ)", type=["jpg", "png", "jpeg"])
                
                submitted_edit = st.form_submit_button("✨ ตรวจสอบข้อมูลก่อนแก้ไข", use_container_width=True)
                
                if submitted_edit:
                    if not edit_name:
                        st.error("กรุณากรอกชื่อสมาชิก")
                    else:
                        file_bytes = edit_uploaded_file.getvalue() if edit_uploaded_file is not None else None
                        file_name_val = edit_uploaded_file.name if edit_uploaded_file is not None else None
                        file_type_val = edit_uploaded_file.type if edit_uploaded_file is not None else None

                        st.session_state[pending_edit_key] = {
                            "name": edit_name,
                            "type": edit_type,
                            "species": edit_species,
                            "gender": edit_gender,
                            "gen_level": int(edit_gen),
                            "birth_date": edit_birth_date.strftime("%Y-%m-%d") if edit_birth_date else None,
                            "father": edit_father if edit_father != "- ไม่ระบุ -" else None,
                            "mother": edit_mother if edit_mother != "- ไม่ระบุ -" else None,
                            "notes": edit_notes,
                            "file_bytes": file_bytes,
                            "file_name": file_name_val,
                            "file_type": file_type_val
                        }
                        st.session_state[edit_confirm_key] = True
                        st.rerun()

            if st.button("✕ ยกเลิกการแก้ไข", key=f"cancel_edit_{m['id']}", use_container_width=True):
                st.session_state[edit_key] = False
                st.rerun()

        # 3. หน้าจอยืนยันการลบข้อมูล
        elif st.session_state[del_key]:
            st.markdown(
                f"<div style='background: #FFF5F5; border: 1.5px solid #FEB2B2; padding: 12px; border-radius: 14px; text-align: center; margin-bottom: 10px; color: #9B2C2C; font-size: 0.88rem; font-weight: 600;'>"
                f"⚠️ คุณต้องการลบข้อมูลของ <b>{m['name']}</b> ใช่หรือไม่?<br><span style='font-size:0.78rem; font-weight:normal; color:#C53030;'>การกระทำนี้ไม่สามารถย้อนกลับได้</span>"
                f"</div>",
                unsafe_allow_html=True
            )
            col_confirm_del, col_cancel_del = st.columns(2)
            with col_confirm_del:
                if st.button("✓ ยืนยันการลบ", key=f"confirm_yes_{m['id']}", use_container_width=True, type="primary"):
                    try:
                        if m.get('image_url'):
                            try:
                                raw_filename = m['image_url'].split('/')[-1]
                                file_name = raw_filename.split('?')[0]
                                supabase.storage.from_("fam-photos").remove([file_name])
                            except Exception as img_err:
                                st.error(f"ไม่สามารถลบรูปภาพจาก Storage ได้: {img_err}")
                        
                        supabase.table("members").delete().eq("id", m["id"]).execute()
                        st.success(f"ลบ {m['name']} เรียบร้อยแล้ว")
                        st.session_state[del_key] = False
                        st.query_params.clear()
                        st.rerun()
                    except Exception as e:
                        st.error(f"เกิดข้อผิดพลาดในการลบข้อมูล : {e}")
            with col_cancel_del:
                if st.button("✕ ยกเลิก", key=f"confirm_no_{m['id']}", use_container_width=True):
                    st.session_state[del_key] = False
                    st.rerun()
        
        # 4. หน้าแสดงรายละเอียดปกติ
        else:
            if m.get('image_url'):
                st.markdown(
                    f'<div style="display: flex; justify-content: center; background: #FAF7F2; border-radius: 18px; overflow: hidden; margin-bottom: 12px; border: 1px solid #EADBCE;">'
                    f'<img src="{m["image_url"]}" style="width: 100%; height: auto; display: block; object-fit: contain;">'
                    f'</div>',
                    unsafe_allow_html=True
                )
            
            if m.get('type') == 'คน':
                type_display = 'คน'
            else:
                type_display = f"{m.get('type')} ({m.get('species', '-')})"
                
            birth_date_html = f"<div><b>วันเกิด :</b> {m['birth_date']}</div>" if m.get('birth_date') else ""
            parents_html = f"<div><b>พ่อ / แม่ :</b> {m.get('father', '-')} / {m.get('mother', '-')}</div>" if (m.get('father') or m.get('mother')) else ""
            notes_html = f"<div><b>บันทึกย่อ :</b> {m['notes']}</div>" if m.get('notes') else ""

            st.markdown(
                f"""
                <div style='background: #FFFFFF; border: 1.5px solid #EADBCE; padding: 16px; border-radius: 16px; font-size: 0.9rem; color: #4A443F; display: flex; flex-direction: column; gap: 8px; margin-bottom: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.02);'>
                    <div style='font-size: 1.2rem; font-weight: 700; color: #4A443F; margin-bottom: 4px; border-bottom: 1px solid #F3ECE1; padding-bottom: 8px;'>{m['name']}</div>
                    <div><b>ประเภท :</b> {type_display}</div>
                    <div><b>เพศ :</b> {m['gender']} &nbsp;|&nbsp; <b>รุ่น:</b> Gen {m.get('gen_level', 1)}</div>
                    {birth_date_html}
                    {parents_html}
                    {notes_html}
                </div>
                """,
                unsafe_allow_html=True
            )
            
            col_edit, col_del = st.columns(2)
            with col_edit:
                st.markdown('<div class="pastel-blue-btn">', unsafe_allow_html=True)
                if st.button("✏️ แก้ไขข้อมูล", key=f"btn_edit_{m['id']}", use_container_width=True):
                    st.session_state[edit_key] = True
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            with col_del:
                if st.button("🗑️ ลบข้อมูล", key=f"btn_del_{m['id']}", use_container_width=True, type="primary"):
                    st.session_state[del_key] = True
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
            '<p style="color: #5C5248; font-weight: 600; font-size: 1.05rem; margin-bottom: 4px;">ยังไม่มีข้อมูลสมาชิก</p>'
            '<p style="color: #A09385; font-size: 0.85rem; margin: 0;">กดที่แท็บ <b>"➕ เพิ่มสมาชิก"</b> เพื่อเพิ่มข้อมูลสมาชิก</p>'
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
        
        unique_gens = sorted(list(set(m.get('gen_level', 1) for m in data)))
        
        tree_blocks = ["<div class='tree-container'>"]
        for idx, gen in enumerate(unique_gens):
            gen_members = [m for m in data if m.get('gen_level', 1) == gen]
            theme = PASTEL_PALETTE[(gen - 1) % len(PASTEL_PALETTE)]
            
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
                
                node_html = f'<a href="?selected_id={m["id"]}" target="_self" class="tree-node-link"><div class="tree-node" style="{card_style}">{avatar_html}<div class="tree-node-name">{m["name"]}</div><div style="{badge_style}">Gen {m.get("gen_level", 1)}</div></div></a>'
                tree_blocks.append(node_html)
            
            tree_blocks.append("</div>")
        tree_blocks.append("</div>")
        
        full_tree_html = "".join(tree_blocks)
        st.markdown(full_tree_html, unsafe_allow_html=True)

# ---------------------------------------------------------
# Tab 2: เพิ่มสมาชิกใหม่ (พร้อมหน้าจอตรวจสอบและยืนยันการบันทึก)
# ---------------------------------------------------------
with tab2:
    if "show_save_confirm" not in st.session_state:
        st.session_state.show_save_confirm = False
    if "pending_member_data" not in st.session_state:
        st.session_state.pending_member_data = None

    if st.session_state.show_save_confirm and st.session_state.pending_member_data:
        pm = st.session_state.pending_member_data
        st.markdown("<div class='section-title'>✨ ตรวจสอบข้อมูลก่อนยืนยันการบันทึก</div>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div style='background: #FFFFFF; border: 2px solid #FFB7B2; padding: 18px; border-radius: 20px; margin-bottom: 16px; box-shadow: 0 8px 20px rgba(255, 183, 178, 0.25);'>
                <div style='font-size: 1.05rem; font-weight: 700; color: #8D2B44; margin-bottom: 10px; text-align: center; border-bottom: 1px solid #FFE4E6; padding-bottom: 8px;'>📋 ข้อมูลสมาชิกใหม่</div>
                <div style='font-size: 0.9rem; color: #4A443F; display: flex; flex-direction: column; gap: 6px;'>
                    <div><b>ชื่อ :</b> {pm['name']}</div>
                    <div><b>ประเภท :</b> {pm['type']} ({pm['species']})</div>
                    <div><b>เพศ :</b> {pm['gender']} &nbsp;|&nbsp; <b>รุ่น:</b> Gen {pm['gen_level']}</div>
                    <div><b>วันเกิด :</b> {pm['birth_date'] if pm['birth_date'] else '-'}</div>
                    <div><b>พ่อ / แม่ :</b> {pm['father'] if pm['father'] else '-'} / {pm['mother'] if pm['mother'] else '-'}</div>
                    <div><b>บันทึกเพิ่มเติม :</b> {pm['notes'] if pm['notes'] else '-'}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        col_save_yes, col_save_no = st.columns(2)
        with col_save_yes:
            if st.button("✓ ยืนยันการบันทึก", key="save_confirm_yes", use_container_width=True, type="primary"):
                try:
                    image_url = None
                    if pm['file_bytes'] is not None:
                        file_ext = pm['file_name'].split(".")[-1]
                        file_path = f"{uuid.uuid4()}.{file_ext}"
                        supabase.storage.from_("fam-photos").upload(
                            path=file_path,
                            file=pm['file_bytes'],
                            file_options={"content-type": pm['file_type']}
                        )
                        image_url = supabase.storage.from_("fam-photos").get_public_url(file_path)
                    
                    new_member = {
                        "name": pm['name'],
                        "type": pm['type'],
                        "species": pm['species'],
                        "gender": pm['gender'],
                        "gen_level": pm['gen_level'],
                        "birth_date": pm['birth_date'],
                        "father": pm['father'],
                        "mother": pm['mother'],
                        "notes": pm['notes'],
                        "image_url": image_url
                    }
                    
                    supabase.table("members").insert(new_member).execute()
                    st.success(f"บันทึก {pm['name']} เรียบร้อยแล้ว")
                    st.session_state.show_save_confirm = False
                    st.session_state.pending_member_data = None
                    st.rerun()
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
        with col_save_no:
            if st.button("✕ ยกเลิก", key="save_confirm_no", use_container_width=True):
                st.session_state.show_save_confirm = False
                st.session_state.pending_member_data = None
                st.rerun()
    else:
        st.markdown("<p style='font-size: 0.85rem; color: #A09385; margin-bottom: 0.8rem; text-align: center;'>กรอกรายละเอียดเพื่อบันทึกสมาชิกหรือสัตว์เลี้ยง</p>", unsafe_allow_html=True)
        
        col_type, col_gen = st.columns([1.0, 1.0])
        
        with col_type:
            member_type = st.radio("ประเภทสมาชิก", ["คน", "สัตว์เลี้ยง"], horizontal=True, label_visibility="collapsed")
            
        with col_gen:
            gen_level = st.number_input(
                "Generation", 
                min_value=1, 
                max_value=10, 
                value=1,
                step=1
            )
        
        existing_members = fetch_members()
        parent_target_gen = gen_level - 1
        
        if gen_level > 1:
            father_options = ["- ไม่ระบุ -"] + [
                m["name"] for m in existing_members 
                if m.get("gender") in ["ชาย", "ผู้"] and m.get("gen_level", 1) == parent_target_gen
            ]
            mother_options = ["- ไม่ระบุ -"] + [
                m["name"] for m in existing_members 
                if m.get("gender") in ["หญิง", "เมีย"] and m.get("gen_level", 1) == parent_target_gen
            ]
        else:
            father_options = ["- ไม่ระบุ -"]
            mother_options = ["- ไม่ระบุ -"]
        
        st.write("")
        
        with st.form("add_member_form", clear_on_submit=False):
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
                father = st.selectbox(f"เลือกพ่อ (จาก Gen {parent_target_gen})" if gen_level > 1 else "เลือกพ่อ", father_options)
            with col_m:
                mother = st.selectbox(f"เลือกแม่ (จาก Gen {parent_target_gen})" if gen_level > 1 else "เลือกแม่", mother_options)
                
            notes = st.text_area("บันทึกเพิ่มเติม", placeholder="ใส่บันทึกย่อ นิสัย หรือลักษณะเด่น...")
            uploaded_file = st.file_uploader("📸 รูปถ่ายสมาชิก", type=["jpg", "png", "jpeg"])
            
            submitted = st.form_submit_button("✨ ตรวจสอบข้อมูลก่อนบันทึก", use_container_width=True)
            
            if submitted:
                if not name:
                    st.error("กรุณากรอกชื่อสมาชิก")
                else:
                    file_bytes = uploaded_file.getvalue() if uploaded_file is not None else None
                    file_name_val = uploaded_file.name if uploaded_file is not None else None
                    file_type_val = uploaded_file.type if uploaded_file is not None else None

                    st.session_state.pending_member_data = {
                        "name": name,
                        "type": member_type,
                        "species": species,
                        "gender": gender,
                        "gen_level": int(gen_level),
                        "birth_date": birth_date.strftime("%Y-%m-%d") if birth_date else None,
                        "father": father if father != "- ไม่ระบุ -" else None,
                        "mother": mother if mother != "- ไม่ระบุ -" else None,
                        "notes": notes,
                        "file_bytes": file_bytes,
                        "file_name": file_name_val,
                        "file_type": file_type_val
                    }
                    st.session_state.show_save_confirm = True
                    st.rerun()