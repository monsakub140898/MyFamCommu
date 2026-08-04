import streamlit as st
from supabase import create_client, Client
import uuid
from datetime import datetime

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
# 3. Custom Minimalist CSS
# ---------------------------------------------------------
st.markdown("""
<style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Sarabun:wght@300;400;500;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', 'Sarabun', -apple-system, BlinkMacSystemFont, sans-serif;
        background-color: #FBFBFA;
        color: #242423;
    }

    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 4rem;
        max-width: 500px;
        margin: 0 auto;
    }

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

    .section-title {
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #8C8A85;
        margin: 1.5rem 0 0.8rem 0;
    }

    .gen-header {
        font-size: 0.85rem;
        font-weight: 600;
        color: #D97757;
        margin-top: 1.2rem;
        margin-bottom: 0.6rem;
    }

    /* CSS Visual Family Tree Styles */
    .tree-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 16px;
        padding: 20px 10px;
        background: #FFFFFF;
        border: 1px solid #EAEAE6;
        border-radius: 16px;
        margin-bottom: 20px;
    }

    .tree-level {
        display: flex;
        justify-content: center;
        gap: 16px;
        flex-wrap: wrap;
        width: 100%;
    }

    .tree-node {
        display: flex;
        flex-direction: column;
        align-items: center;
        background: #FAFAFA;
        border: 1px solid #EFEFEA;
        border-radius: 12px;
        padding: 10px 14px;
        min-width: 85px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }

    .tree-avatar-img {
        width: 52px;
        height: 52px;
        border-radius: 50%;
        object-fit: cover;
        border: 2px solid #D97757;
        margin-bottom: 6px;
    }

    .tree-avatar-placeholder {
        width: 52px;
        height: 52px;
        border-radius: 50%;
        background-color: #EFEFEA;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.4rem;
        margin-bottom: 6px;
        border: 2px solid #D97757;
    }

    .tree-node-name {
        font-size: 0.85rem;
        font-weight: 600;
        color: #1A1A18;
        text-align: center;
    }

    .tree-node-sub {
        font-size: 0.7rem;
        color: #8C8A85;
    }

    .tree-connector {
        width: 2px;
        height: 14px;
        background-color: #D97757;
    }

    /* Tabs Style */
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
# 4. App Header & Data Fetching
# ---------------------------------------------------------
st.markdown("<div class='app-title'>My Fam Commu</div>", unsafe_allow_html=True)
st.markdown("<div class='app-subtitle'>Family Tree & Pet Records</div>", unsafe_allow_html=True)

def fetch_members():
    try:
        response = supabase.table("members").select("*").order("gen_level", desc=False).execute()
        return response.data
    except Exception as e:
        st.error(f"ไม่สามารถเชื่อมต่อฐานข้อมูลได้: {e}")
        return []

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
        st.markdown("""
        <div style="text-align: center; padding: 36px 16px; background-color: #FFFFFF; border: 1px solid #EAEAE6; border-radius: 12px; margin-top: 12px;">
            <p style="font-size: 2rem; margin-bottom: 8px;">🐾</p>
            <p style="color: #1A1A18; font-weight: 600; font-size: 0.95rem; margin-bottom: 4px;">ยังไม่มีข้อมูลสมาชิก</p>
            <p style="color: #8C8A85; font-size: 0.8rem; margin: 0;">เริ่มต้นเพิ่มสมาชิกคนแรกได้ที่แท็บ <b>"➕ เพิ่มสมาชิก"</b></p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # 1. แสดงแผนผังแบบ Visual CSS Tree
        st.markdown("<div class='section-title'>แผนผัง (FAMILY TREE)</div>", unsafe_allow_html=True)
        
        unique_gens = sorted(list(set(m.get('gen_level', 0) for m in data)))
        
        tree_blocks = ["<div class='tree-container'>"]
        for idx, gen in enumerate(unique_gens):
            gen_members = [m for m in data if m.get('gen_level', 0) == gen]
            
            if idx > 0:
                tree_blocks.append("<div class='tree-connector'></div>")
                
            tree_blocks.append("<div class='tree-level'>")
            for m in gen_members:
                if m.get('image_url'):
                    avatar_html = f"<img src='{m['image_url']}' class='tree-avatar-img'>"
                else:
                    icon = '🐱' if m.get('type') == 'สัตว์เลี้ยง' else '👤'
                    avatar_html = f"<div class='tree-avatar-placeholder'>{icon}</div>"
                
                tree_blocks.append(f"<div class='tree-node'>{avatar_html}<div class='tree-node-name'>{m['name']}</div><div class='tree-node-sub'>Gen {m.get('gen_level', 0)}</div></div>")
            
            tree_blocks.append("</div>")
        tree_blocks.append("</div>")
        
        full_tree_html = "".join(tree_blocks)
        st.markdown(full_tree_html, unsafe_allow_html=True)
        
        st.divider()

        # 2. รายชื่อสมาชิกทั้งหมด (คลิกแถบชื่อเพื่อดูข้อมูล/ลบข้อมูล)
        st.markdown("<div class='section-title'>รายชื่อสมาชิกทั้งหมด</div>", unsafe_allow_html=True)
        
        for gen in unique_gens:
            st.markdown(f"<div class='gen-header'>📌 Generation {gen}</div>", unsafe_allow_html=True)
            gen_members = [m for m in data if m.get('gen_level', 0) == gen]
            
            for m in gen_members:
                icon = '🐱' if m.get('type') == 'สัตว์เลี้ยง' else '👤'
                
                with st.expander(f"{icon} {m['name']} ({m['species']})"):
                    if m.get('image_url'):
                        st.image(m['image_url'], use_container_width=True)
                    st.write(f"**ชื่อ:** {m['name']}")
                    st.write(f"**ประเภท:** {m['type']} ({m['species']})")
                    st.write(f"**เพศ:** {m['gender']} | **รุ่น:** Gen {m['gen_level']}")
                    if m.get('birth_date'):
                        st.write(f"**วันเกิด:** {m['birth_date']}")
                    if m.get('father') or m.get('mother'):
                        st.write(f"**พ่อ-แม่:** {m.get('father', '-')} / {m.get('mother', '-')}")
                    if m.get('notes'):
                        st.write(f"**บันทึก:** {m['notes']}")
                    
                    st.divider()
                    
                    if st.button(f"🗑️ ลบ {m['name']}", key=f"del_{m['id']}", use_container_width=True):
                        try:
                            if m.get('image_url'):
                                try:
                                    file_name = m['image_url'].split('/')[-1]
                                    supabase.storage.from_("fam-photos").remove([file_name])
                                except Exception as img_err:
                                    st.warning(f"ลบรูปภาพไม่สำเร็จ: {img_err}")
                            
                            supabase.table("members").delete().eq("id", m["id"]).execute()
                            st.success(f"ลบ {m['name']} และรูปภาพเรียบร้อยแล้ว")
                            st.rerun()
                        except Exception as e:
                            st.error(f"เกิดข้อผิดพลาดในการลบ: {e}")

# ---------------------------------------------------------
# Tab 2: เพิ่มสมาชิกใหม่
# ---------------------------------------------------------
with tab2:
    st.markdown("<p style='font-size: 0.9rem; color: #706F6C; margin-bottom: 1rem;'>กรอกรายละเอียดเพื่อบันทึกสมาชิกเข้าสู่ระบบ</p>", unsafe_allow_html=True)
    
    member_type = st.radio("ประเภทสมาชิก", ["คน", "สัตว์เลี้ยง"], horizontal=True, label_visibility="collapsed")
    gen_level = st.number_input("Generation (0=รุ่นแรกสุด, 1=รุ่นลูก, 2=รุ่นหลาน)", min_value=0, max_value=10, value=0)
    
    existing_members = fetch_members()
    
    # 🎯 ตัวกรองพ่อ-แม่: จะดึงเฉพาะสมาชิกที่อยู่ใน Gen ก่อนหน้าตรงๆ 1 รุ่น เท่านั้น
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
            father = st.selectbox(f"เลือกพ่อ {parent_target_gen}" if gen_level > 0 else "เลือกพ่อ", father_options)
        with col_m:
            mother = st.selectbox(f"เลือกแม่ {parent_target_gen}" if gen_level > 0 else "เลือกแม่", mother_options)
            
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
                        "birth_date": birth_date.strftime("%Y-%m-%d") if birth_date else None,
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