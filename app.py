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
# 3. Custom Warm Minimalist & Interactive Tree CSS
# ---------------------------------------------------------
st.markdown("""
<style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;500;600;700&family=Sarabun:wght@300;400;500;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Fredoka', 'Sarabun', -apple-system, BlinkMacSystemFont, sans-serif;
        background-color: #FAF8F5;
        color: #33322E;
    }

    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 4rem;
        max-width: 480px;
        margin: 0 auto;
    }

    /* Header Styling */
    .app-title {
        font-size: 1.7rem;
        font-weight: 700;
        color: #2D2B28;
        letter-spacing: -0.01em;
        text-align: center;
        margin-bottom: 2px;
    }
    
    .app-subtitle {
        font-size: 0.85rem;
        color: #9C968E;
        text-align: center;
        margin-bottom: 1.5rem;
        font-weight: 400;
    }

    .section-title {
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: #A39B91;
        margin: 1rem 0 0.8rem 0;
        text-align: center;
    }

    /* CSS Visual Family Tree Styles */
    .tree-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 16px;
        padding: 22px 12px;
        background: #FFFFFF;
        border: 1.5px solid #F0EAE1;
        border-radius: 20px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.02);
        margin-bottom: 20px;
    }

    .tree-level {
        display: flex;
        justify-content: center;
        gap: 16px;
        flex-wrap: wrap;
        width: 100%;
    }

    /* Interactive Clickable Node Wrapper */
    .tree-node-link {
        text-decoration: none !important;
        color: inherit !important;
        display: inline-block;
    }

    .tree-node {
        display: flex;
        flex-direction: column;
        align-items: center;
        background: #FAF8F5;
        border: 1.5px solid #EFEAE1;
        border-radius: 16px;
        padding: 12px 14px;
        min-width: 90px;
        transition: all 0.2s ease;
        cursor: pointer;
    }

    .tree-node:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 16px rgba(224, 122, 95, 0.18);
        border-color: #E07A5F;
        background: #FFFFFF;
    }

    .tree-avatar-img {
        width: 56px;
        height: 56px;
        border-radius: 50%;
        object-fit: cover;
        border: 3px solid #FFFFFF;
        box-shadow: 0 4px 10px rgba(224, 122, 95, 0.25);
        margin-bottom: 8px;
    }

    .tree-avatar-placeholder {
        width: 56px;
        height: 56px;
        border-radius: 50%;
        background-color: #FDF0ED;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        margin-bottom: 8px;
        border: 3px solid #FFFFFF;
        box-shadow: 0 4px 10px rgba(224, 122, 95, 0.15);
    }

    .tree-node-name {
        font-size: 0.88rem;
        font-weight: 600;
        color: #2D2B28;
        text-align: center;
    }

    .tree-node-badge {
        font-size: 0.68rem;
        font-weight: 600;
        color: #E07A5F;
        background: #FDF0ED;
        padding: 2px 8px;
        border-radius: 10px;
        margin-top: 4px;
    }

    .tree-connector {
        width: 2px;
        height: 16px;
        background-color: #F2CC8F;
        border-radius: 2px;
    }

    /* Tabs Style */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #F2ECE1;
        padding: 5px;
        border-radius: 14px;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 8px 18px;
        font-size: 0.85rem;
        font-weight: 600;
        color: #827B73;
        border: none;
    }

    .stTabs [aria-selected="true"] {
        background-color: #FFFFFF !important;
        color: #2D2B28 !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
    }

    /* Button Customization */
    div[data-testid="stFormSubmitButton"] > button {
        background-color: #E07A5F !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        padding: 0.6rem 1rem !important;
        box-shadow: 0 4px 12px rgba(224, 122, 95, 0.25) !important;
        transition: all 0.2s ease;
    }
    div[data-testid="stFormSubmitButton"] > button:hover {
        background-color: #D0694E !important;
        transform: translateY(-1px);
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. App Header & Data Fetching
# ---------------------------------------------------------
st.markdown("<div class='app-title'>My Fam Commu 🐾</div>", unsafe_allow_html=True)
st.markdown("<div class='app-subtitle'>บันทึกผังครอบครัว</div>", unsafe_allow_html=True)

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
                            file_name = m['image_url'].split('/')[-1]
                            supabase.storage.from_("fam-photos").remove([file_name])
                        except Exception as img_err:
                            st.warning(f"ลบรูปภาพไม่สำเร็จ: {img_err}")
                    
                    supabase.table("members").delete().eq("id", m["id"]).execute()
                    st.success(f"ลบ {m['name']} เรียบร้อยแล้ว")
                    st.query_params.clear()
                    st.rerun()
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาดในการลบ: {e}")
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
# Tab 1: ผังครอบครัว (แสดงเฉพาะแผนผัง + กดดูรายละเอียดได้)
# ---------------------------------------------------------
with tab1:
    data = fetch_members()
    
    if not data:
        st.markdown("""
        <div style="text-align: center; padding: 40px 20px; background-color: #FFFFFF; border: 1.5px solid #F0EAE1; border-radius: 20px; margin-top: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.02);">
            <p style="font-size: 2.2rem; margin-bottom: 8px;">🐶🐱</p>
            <p style="color: #2D2B28; font-weight: 600; font-size: 1rem; margin-bottom: 4px;">ยังไม่มีข้อมูลสมาชิกในบ้าน</p>
            <p style="color: #9C968E; font-size: 0.82rem; margin: 0;">กดที่แท็บ <b>"➕ เพิ่มสมาชิก"</b> ด้านบนเพื่อเริ่มเพิ่มข้อมูลคนแรกได้เลยครับ</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("<div class='section-title'>🏡 แผนผัง (คลิกที่รูปเพื่อดูรายละเอียด)</div>", unsafe_allow_html=True)
        
        # ตรวจสอบว่าผู้ใช้คลิกเลือกสมาชิกคนไหนในแผนผังหรือไม่
        if "selected_id" in st.query_params:
            sel_id = st.query_params["selected_id"]
            selected_m = next((m for m in data if str(m["id"]) == str(sel_id)), None)
            if selected_m:
                render_member_dialog(selected_m)
        
        # วาดแผนผังแบบ Clickable Tree Node
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
                
                # ใส่แท็ก <a> เพื่อให้ครอบการ์ดทั้งหมด คลิกแล้วเปิด Pop-up รายละเอียดทันที
                node_html = f"<a href='?selected_id={m['id']}' target='_self' class='tree-node-link'><div class='tree-node'>{avatar_html}<div class='tree-node-name'>{m['name']}</div><div class='tree-node-badge'>Gen {m.get('gen_level', 0)}</div></div></a>"
                tree_blocks.append(node_html)
            
            tree_blocks.append("</div>")
        tree_blocks.append("</div>")
        
        full_tree_html = "".join(tree_blocks)
        st.markdown(full_tree_html, unsafe_allow_html=True)

# ---------------------------------------------------------
# Tab 2: เพิ่มสมาชิกใหม่
# ---------------------------------------------------------
with tab2:
    st.markdown("<p style='font-size: 0.85rem; color: #9C968E; margin-bottom: 1rem;'>กรอกรายละเอียดเพื่อบันทึกสมาชิกคนใหม่หรือสัตว์เลี้ยงเข้าบ้านครับ</p>", unsafe_allow_html=True)
    
    member_type = st.radio("ประเภทสมาชิก", ["คน", "สัตว์เลี้ยง"], horizontal=True, label_visibility="collapsed")
    gen_level = st.number_input("Generation (0=รุ่นแรกสุด, 1=รุ่นลูก, 2=รุ่นหลาน)", min_value=0, max_value=10, value=0)
    
    existing_members = fetch_members()
    
    # ตัวกรองพ่อ-แม่: ดึงเฉพาะสมาชิกจาก Gen ก่อนหน้าตรงๆ 1 รุ่น
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
            father = st.selectbox(f"เลือกพ่อ (จาก Gen {parent_target_gen})" if gen_level > 0 else "เลือกพ่อ", father_options)
        with col_m:
            mother = st.selectbox(f"เลือกแม่ (จาก Gen {parent_target_gen})" if gen_level > 0 else "เลือกแม่", mother_options)
            
        notes = st.text_area("บันทึกเพิ่มเติม", placeholder="ใส่บันทึกย่อ นิสัย หรือลักษณะเด่น...")
        uploaded_file = st.file_uploader("📸 รูปถ่ายสมาชิก", type=["jpg", "png", "jpeg"])
        
        submitted = st.form_submit_button("✨ บันทึกข้อมูลสมาชิก", use_container_width=True)
        
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
                    st.success(f"บันทึก {name} เรียบร้อยแล้วครับ!")
                    st.rerun()
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")