import streamlit as st
from supabase import create_client, Client
import uuid

# ---------------------------------------------------------
# 1. ตั้งค่าหน้าเพจแบบ Mobile-First Responsive
# ---------------------------------------------------------
st.set_page_config(
    page_title="My Fam Commu",
    page_icon="🐾",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# 2. เชื่อมต่อ Supabase Cloud
# ---------------------------------------------------------
SUPABASE_URL = "https://zqeiswjafwwzemygmjcl.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpxZWlzd2phZnd3emVteWdtamNsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODU4MTcyMzYsImV4cCI6MjEwMTM5MzIzNn0.9yV7BAYCiwUyk3NQmtZ5bLfUrPmirWGnY7rgga2BA64"

@st.cache_resource
def init_supabase() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_supabase()

# ---------------------------------------------------------
# 3. Custom CSS ตกแต่ง UI สไตล์แอปมือถือ (Pastel Tone)
# ---------------------------------------------------------
st.markdown("""
<style>
    /* ซ่อน Header / Footer เดิมของ Streamlit */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    
    /* บังคับกรอบหน้าจอให้พอดีกับมือถือทุกรุ่น (รวมถึง iPhone 13 บน Safari) */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 480px;
        margin: 0 auto;
    }
    
    /* ดีไซน์การ์ดสมาชิก */
    .member-card {
        border-radius: 20px;
        padding: 16px;
        margin-bottom: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.03);
        border: 2px solid #FFF;
        display: flex;
        align-items: center;
        gap: 15px;
    }
    .gen-0 { background-color: #E6FFFA; border-color: #B2F5EA; } /* ฟ้าพาสเทล */
    .gen-1 { background-color: #FFFAF0; border-color: #FEEBC8; } /* ส้มพาสเทล */
    .gen-2 { background-color: #FFF5F7; border-color: #FED7E2; } /* ชมพูพาสเทล */
    .gen-3 { background-color: #F0FFF4; border-color: #C6F6D5; } /* เขียวพาสเทล */

    .avatar-img {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        object-fit: cover;
        border: 2px solid white;
    }
    .avatar-placeholder {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background-color: #EDF2F7;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.8rem;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. ส่วนหัวแอปพลิเคชัน (App Header)
# ---------------------------------------------------------
st.markdown("<h2 style='text-align: center; color: #4A5568; margin-bottom: 0;'>🐾 My Fam Commu</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #A0AEC0; font-size: 0.85rem;'>ผังครอบครัว & สมุดบันทึกสัตว์เลี้ยง</p>", unsafe_allow_html=True)

menu = st.radio("Navigation", ["🌳 ผังครอบครัว", "➕ เพิ่มสมาชิกใหม่"], horizontal=True, label_visibility="collapsed")
st.divider()

# ฟังก์ชันดึงข้อมูลจาก Cloud
def fetch_members():
    try:
        response = supabase.table("members").select("*").order("gen_level", desc=False).execute()
        return response.data
    except Exception:
        return []

# ---------------------------------------------------------
# หน้าที่ 1: ผังครอบครัว (Mobile Visual Family Tree)
# ---------------------------------------------------------
if menu == "🌳 ผังครอบครัว":
    data = fetch_members()
    
    # ถ้ายังไม่มีข้อมูลในระบบเลย (ครั้งแรกสุด) ให้แสดงหน้าว่างสวยๆ
    if not data:
        st.markdown("""
        <div style="text-align: center; padding: 40px 20px; background-color: #FFF5F5; border-radius: 20px; border: 2px dashed #FEB2B2; margin-top: 10px;">
            <p style="font-size: 3rem; margin-bottom: 10px;">🐾</p>
            <h4 style="color: #4A5568; margin-bottom: 8px;">ยังไม่มีสมาชิกในครอบครัว</h4>
            <p style="color: #718096; font-size: 0.85rem; margin: 0;">เริ่มต้นเพิ่มสมาชิกคนแรกได้ที่เมนูด้านบน<br><b>"➕ เพิ่มสมาชิกใหม่"</b></p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # แสดงผลตาม Generation แนวดิ่ง
        for gen in range(6):
            members_in_gen = [m for m in data if m.get("gen_level") == gen]
            if members_in_gen:
                st.markdown(f"<p style='color:#A0AEC0; font-weight:bold; font-size:0.8rem; letter-spacing:1px; margin-bottom:8px;'>GENERATION {gen}</p>", unsafe_allow_html=True)
                
                for m in members_in_gen:
                    # เตรียมรูปโปรไฟล์
                    if m.get('image_url'):
                        img_html = f"<img src='{m['image_url']}' class='avatar-img'>"
                    else:
                        icon = '🐱' if m['type'] == 'สัตว์เลี้ยง' else '👤'
                        img_html = f"<div class='avatar-placeholder'>{icon}</div>"
                    
                    card_html = f"""
                    <div class="member-card gen-{gen % 4}">
                        {img_html}
                        <div style="flex-grow: 1;">
                            <h4 style="margin:0; color:#2D3748; font-size:1.05rem;">{m['name']}</h4>
                            <p style="margin:2px 0 0 0; font-size:0.8rem; color:#718096;">
                                {m['species']} | เพศ: {m['gender']}
                            </p>
                        </div>
                    </div>
                    """
                    st.markdown(card_html, unsafe_allow_html=True)
                    
                    # คลิกเพื่อดูรายละเอียดโปรไฟล์ (Profile Detail Sheet)
                    with st.expander(f"📖 ดูโปรไฟล์ของ {m['name']}"):
                        if m.get('image_url'):
                            st.image(m['image_url'], use_container_width=True)
                        st.write(f"**ประเภท:** {m['type']} ({m['species']})")
                        st.write(f"**เพศ:** {m['gender']}")
                        st.write(f"**รุ่น:** Gen {m['gen_level']}")
                        if m.get('father') or m.get('mother'):
                            st.write(f"**พ่อ-แม่:** {m.get('father', '-')} & {m.get('mother', '-')}")
                        st.write(f"**บันทึกพัฒนาการ / โน้ต:** {m.get('notes') if m.get('notes') else '-'}")

# ---------------------------------------------------------
# หน้าที่ 2: ฟอร์มเพิ่มสมาชิกใหม่ (Dynamic Add Member Form)
# ---------------------------------------------------------
elif menu == "➕ เพิ่มสมาชิกใหม่":
    st.subheader("เพิ่มสมาชิกใหม่")
    
    # Conditional Logic เลือกประเภท
    member_type = st.radio("ประเภทสมาชิก", ["คน", "สัตว์เลี้ยง"], horizontal=True)
    
    existing_members = fetch_members()
    member_names = ["- ไม่ระบุ -"] + [m["name"] for m in existing_members]
    
    with st.form("add_member_form", clear_on_submit=True):
        name = st.text_input("ชื่อสมาชิก (Name)*")
        
        if member_type == "คน":
            species = "คน"
            gender = st.selectbox("เพศ", ["ชาย", "หญิง", "อื่นๆ"])
        else:
            species = st.selectbox("ชนิดสัตว์เลี้ยง", ["แมว", "หมา", "นก", "กระต่าย", "อื่นๆ"])
            gender = st.selectbox("เพศ", ["ผู้", "เมีย"])
            
        gen_level = st.number_input("Generation (ลำดับรุ่น 0, 1, 2...)", min_value=0, max_value=10, value=0)
        
        st.markdown("**เชื่อมสายเลือด (Parents):**")
        col_f, col_m = st.columns(2)
        with col_f:
            father = st.selectbox("เลือกพ่อ", member_names)
        with col_m:
            mother = st.selectbox("เลือกแม่", member_names)
            
        notes = st.text_area("บันทึกพัฒนาการ / ลักษณะเด่น / โน้ตเพิ่มเติม")
        uploaded_file = st.file_uploader("📸 อัปโหลดรูปถ่าย", type=["jpg", "png", "jpeg"])
        
        submitted = st.form_submit_button("☁️ บันทึกข้อมูลขึ้น Cloud", use_container_width=True)
        
        if submitted:
            if not name:
                st.error("กรุณากรอกชื่อสมาชิกด้วยครับ")
            else:
                image_url = None
                
                # ถ้ามีรูปภาพ ให้อัปโหลดขึ้น Storage Bucket 'fam-photos'
                if uploaded_file is not None:
                    file_ext = uploaded_file.name.split(".")[-1]
                    file_path = f"{uuid.uuid4()}.{file_ext}"
                    
                    supabase.storage.from_("fam-photos").upload(
                        path=file_path,
                        file=uploaded_file.getvalue(),
                        file_options={"content-type": uploaded_file.type}
                    )
                    image_url = supabase.storage.from_("fam-photos").get_public_url(file_path)
                
                # บันทึกลง Supabase Database
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
                st.success(f"บันทึกข้อมูล {name} เข้าสู่ระบบเรียบร้อยแล้ว!")
                st.balloons()