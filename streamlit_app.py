import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
import urllib.parse
import re

# --- 1. CONFIGURATION & DIRECT DB LINK ---
DB_URL = "https://docs.google.com/spreadsheets/d/1XByjOff262bUNx8i1bzCOQrzjXxw3JlU93paosDdpbE/edit?usp=sharing"
DRIVE_URL = "https://drive.google.com/drive/folders/1XIwkqlSv8Kesf2abM0vwFeI8IX63qzEt?usp=drive_link"

icon_url = "https://cdn-icons-png.flaticon.com/512/814/814513.png" 
st.set_page_config(page_title="GeoSense by Sahan", page_icon=icon_url, layout="centered")

# --- 2. IMAGES (FB COVER & IMGBB GALLERY) ---
FB_COVER_IMAGE_URL = "https://i.ibb.co/pv1MBwZH/645857513-122124476361086173-5353523332435350460-n.png" 

img_gallery_1 = "https://i.ibb.co/HLRrxp3n/TIF00958.jpg"
img_gallery_2 = "https://i.ibb.co/SX4KBHF4/TIF00946.jpg"
img_gallery_3 = "https://i.ibb.co/XxjWgkvy/TIF00721.jpg"

# --- 3. CONSTANTS & UTILITIES ---
BATCHES = ["2026 A/L", "2027 A/L", "2028 A/L"]

DISTRICT_DATA = {
    "Colombo": {"lat": 6.9271, "lon": 79.8612}, "Kandy": {"lat": 7.2906, "lon": 80.6337},
    "Galle": {"lat": 6.0535, "lon": 80.2210}, "Matara": {"lat": 5.9549, "lon": 80.5550},
    "Kurunegala": {"lat": 7.4863, "lon": 80.3647}, "Anuradhapura": {"lat": 8.3114, "lon": 80.4037},
    "Ratnapura": {"lat": 6.7056, "lon": 80.3847}, "Kalutara": {"lat": 6.5854, "lon": 79.9607},
    "Badulla": {"lat": 6.9934, "lon": 81.0550}, "Nuwara Eliya": {"lat": 6.9497, "lon": 80.7891},
    "Hambantota": {"lat": 6.1246, "lon": 81.1185}, "Puttalam": {"lat": 8.0330, "lon": 79.8250},
    "Kegalle": {"lat": 7.2513, "lon": 80.3464}, "Matale": {"lat": 7.4675, "lon": 80.6234},
    "Polonnaruwa": {"lat": 7.9397, "lon": 81.0036}, "Monaragala": {"lat": 6.8724, "lon": 81.3507},
    "Ampara": {"lat": 7.2842, "lon": 81.6747}, "Trincomalee": {"lat": 8.5711, "lon": 81.2335},
    "Batticaloa": {"lat": 7.7302, "lon": 81.6747}, "Vavuniya": {"lat": 8.7542, "lon": 80.4982},
    "Mannar": {"lat": 8.9810, "lon": 79.9044}, "Mullaitivu": {"lat": 9.2671, "lon": 80.8142},
    "Kilinochchi": {"lat": 9.3803, "lon": 80.4037}, "Jaffna": {"lat": 9.6615, "lon": 80.0255}
}

MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

# --- Smart WhatsApp Link Generation with Pre-filled Message ---
# --- 4. GOOGLE SHEET CONNECTION (DIRECT CREDENTIALS INJECTION) ---
# Secrets වලින් කෙලින්ම credentials dict එක හදාගන්නවා
credentials_dict = {
    "type": st.secrets["connections"]["gsheets"]["type"],
    "project_id": st.secrets["connections"]["gsheets"]["project_id"],
    "private_key_id": st.secrets["connections"]["gsheets"]["private_key_id"],
    "private_key": st.secrets["connections"]["gsheets"]["private_key"].replace("\\n", "\n"),
    "client_email": st.secrets["connections"]["gsheets"]["client_email"],
    "client_id": st.secrets["connections"]["gsheets"]["client_id"],
    "auth_uri": st.secrets["connections"]["gsheets"]["auth_uri"],
    "token_uri": st.secrets["connections"]["gsheets"]["token_uri"],
    "auth_provider_x509_cert_url": st.secrets["connections"]["gsheets"]["auth_provider_x509_cert_url"],
    "client_x509_cert_url": st.secrets["connections"]["gsheets"]["client_x509_cert_url"]
}

# Credentials dict එක කෙලින්ම connection එකට pass කරනවා
conn = st.connection("gsheets", type=GSheetsConnection, credentials=credentials_dict)

try:
    df_global_students = conn.read(spreadsheet=DB_URL, worksheet="Student_DB", ttl=0)
except Exception as e:
    st.error(f"⚠️ Unable to sync with database. Error Details: {e}")
    df_global_students = pd.DataFrame()
    if len(cleaned) == 9 and cleaned.startswith('7'): return "0" + cleaned
    return cleaned

# --- 4. GOOGLE SHEET CONNECTION ---
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    df_global_students = conn.read(spreadsheet=DB_URL, worksheet="Student_DB", ttl=0)
except Exception as e:
    st.error("⚠️ Unable to sync with database. Please verify configuration.")
    df_global_students = pd.DataFrame()

# --- 5. PREMIUM UI CUSTOMIZATION (THEMING) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght=300;400;500;600;700&display=swap');
    
    .stApp { 
        background: linear-gradient(rgba(244, 248, 249, 0.92), rgba(244, 248, 249, 0.92)), 
        url("https://www.transparenttextures.com/patterns/gplay.png");
        background-size: cover; background-attachment: fixed;
    }
    
    .main-title { font-family: 'Poppins', sans-serif; color: #0f4c5c; text-align: center; font-size: clamp(34px, 6vw, 55px); font-weight: 700; margin-top: 10px; }
    .sub-title { font-family: 'Poppins', sans-serif; color: #e36414; text-align: center; font-size: clamp(13px, 3vw, 17px); font-weight: 600; margin-bottom: 30px; text-transform: uppercase; letter-spacing: 1.5px; }
    .stMarkdown, p, label, .stSelectbox, .stTextInput { font-family: 'Poppins', sans-serif !important; font-weight: 400 !important; color: #2b2d42 !important; }
    
    .stTabs [data-baseweb="tab-list"] { justify-content: center; gap: 10px; }
    .stTabs [data-baseweb="tab"] { 
        background-color: rgba(215, 228, 230, 0.7); border-radius: 8px 8px 0px 0px; padding: 10px 18px; 
        font-family: 'Poppins', sans-serif; font-weight: 600; color: #0f4c5c;
    }
    
    .stButton>button { width: 100%; background: linear-gradient(90deg, #0f4c5c 0%, #118ab2 100%); color: white; border-radius: 12px; height: 50px; font-weight: 600; border: none; font-family: 'Poppins', sans-serif; transition: 0.3s; }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(15,76,92,0.3); }
    
    .bio-card { background: #ffffff; border-radius: 16px; padding: 25px; box-shadow: 0 8px 25px rgba(15, 76, 92, 0.06); border: 1px solid #e2eaeb; margin-bottom: 25px; }
    .profile-card { background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.04); margin-bottom: 20px; border-left: 5px solid #0f4c5c; }
    .paid-badge { background-color: #2ec4b6; color: white; padding: 15px; border-radius: 12px; text-align: center; font-weight: bold; margin: 15px 0; }
    
    .social-container { display: flex; justify-content: center; gap: 25px; margin: 20px 0; }
    .social-icon { width: 45px; height: 45px; transition: transform 0.3s ease, filter 0.3s ease; cursor: pointer; }
    .social-icon:hover { transform: scale(1.2); filter: drop-shadow(0px 5px 8px rgba(0,0,0,0.15)); }
    
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 6. BRANDING HEADER WITH FB COVER IMAGE ---
st.markdown(f"""
    <div style="display: flex; justify-content: center; margin-bottom: 15px;">
        <img src="{FB_COVER_IMAGE_URL}" style="width: 100%; border-radius: 16px; object-fit: cover; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
    </div>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">GeoSense <span style="color:#e36414; font-weight:400;">by Sahan</span></p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Guiding the next Generation of Geographers</p>', unsafe_allow_html=True)

# --- 7. APPS TABS NAVIGATION ---
menu = st.tabs(["🌍 Home", "📝 Registration", "💳 Fees & Payments", "📍 Student Map", "📅 Schedule", "📚 Resources"])

# --- TAB 1: HOME (ABOUT THE LECTURER & ACADEMIC HUB) ---
with menu[0]:
    col_img, col_det = st.columns([2, 3])
    with col_img:
        st.image(img_gallery_1, caption="Sahan Vitanage", width="stretch")
    with col_det:
        st.markdown("""
        <div class="bio-card" style="padding:15px; height:100%;">
            <h3 style="color: #0f4c5c; margin-top:0;">Meet Your Lecturer</h3>
            <p style="font-size: 15px; line-height: 1.6; margin-bottom:8px;">
                <b>Sahan Vitanage</b><br>
                <span style="color: #e36414; font-weight: 600;">GIS Expert & Educator</span><br>
                BSc. Honors in Geographical Information Science<br>
                <i>University of Peradeniya, Sri Lanka.</i>
            </p>
            <p style="font-size: 13.5px; color: #555; margin-top:0;">
                Bringing contemporary Geospatial Technology & GIS Expertise straight into Advanced Level Geography classrooms to engineer a smart learning landscape.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    st.write("")
    st.markdown("### 🎓 Academic & Convocation Gallery")
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.image(img_gallery_2, caption="Excellence in Geospatial Science", width="stretch")
    with col_g2:
        st.image(img_gallery_3, caption="University of Peradeniya Convocation", width="stretch")
        
    st.markdown("<hr style='border: 1px solid #e2eaeb;'>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align:center; color:#0f4c5c;'>Connect with GeoSense Community</h4>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="social-container">
        <a href="https://youtube.com/@geosensebysahan?si=8aCYZsTRqDo7bT0r" target="_blank">
            <img src="https://cdn-icons-png.flaticon.com/512/3670/3670147.png" class="social-icon" alt="YouTube">
        </a>
        <a href="https://www.facebook.com/share/1E3uyMWtYq/" target="_blank">
            <img src="https://cdn-icons-png.flaticon.com/512/5968/5968764.png" class="social-icon" alt="Facebook">
        </a>
        <a href="https://www.tiktok.com/@sahan.vithanage7?_r=1&_t=ZS-97dvOpvuysT" target="_blank">
            <img src="https://cdn-icons-png.flaticon.com/512/3046/3046124.png" class="social-icon" alt="TikTok">
        </a>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    st.link_button("📲 Chat Directly on WhatsApp Business", SAHAN_WHATSAPP_LINK)

# --- TAB 2: REGISTRATION FORM ---
with menu[1]:
    st.markdown("### 📝 Create Student Account")
    check_phone = st.text_input("Enter your WhatsApp Mobile Number", key="reg_check", max_chars=10, placeholder="e.g., 0711234567")
    
    if check_phone and is_valid_phone(check_phone):
        df_students = df_global_students.copy() if not df_global_students.empty else pd.DataFrame()
        existing_numbers = df_students['Phone_Number'].apply(format_sheet_phone).values if not df_students.empty and 'Phone_Number' in df_students.columns else []
        
        if str(check_phone).strip() in existing_numbers:
            st.warning("⚠️ Access Profile Alert: This phone number is already registered inside GeoSense!")
        else:
            with st.form("reg_form", clear_on_submit=True):
                name = st.text_input("Full Student Name")
                batch = st.selectbox("Academic Year (Batch)", BATCHES)
                dist = st.selectbox("Residential District", list(DISTRICT_DATA.keys()))
                
                if st.form_submit_button("Submit Registration Profile"):
                    if name:
                        new_student = pd.DataFrame([{
                            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                            "Name": name, "Phone_Number": check_phone, "Batch": batch, "District": dist, 
                            "lat": DISTRICT_DATA[dist]["lat"], "lon": DISTRICT_DATA[dist]["lon"], 
                            "Access": "Don't Allow", "Group_Status": "Joined"
                        }])
                        conn.update(spreadsheet=DB_URL, worksheet="Student_DB", data=pd.concat([df_students, new_student], ignore_index=True))
                        st.success("Successfully Registered Onto GeoSense Database Server! 🎉")
                        st.rerun()

# --- TAB 3: FEES & PAYMENTS SUBMISSION ---
with menu[2]:
    st.markdown("""
    <div class="bio-card" style="border: 1.5px dashed #e36414; text-align: center;">
        <h4 style="color: #0f4c5c; margin-top:0;">🏦 Class Fee Bank Details:</h4>
        <p style='color: #e36414; font-size: 16px; font-weight: bold; margin: 10px 0;'>Class Fee Bank Details Will Be Updated Soon! ⏳</p>
        <p style='font-size: 13.5px; color: #555;'>Please contact Sahan Sir via WhatsApp for immediate class fee payment inquiries.</p>
    </div>
    """, unsafe_allow_html=True)

    pay_phone = st.text_input("Enter Registered WhatsApp Number (07xxxxxxxx)", key="pay_check", max_chars=10, placeholder="e.g., 0711234567")
    if pay_phone and is_valid_phone(pay_phone):
        df_reg = df_global_students.copy() if not df_global_students.empty else pd.DataFrame()
        if not df_reg.empty and 'Phone_Number' in df_reg.columns:
            df_reg['formatted_phone'] = df_reg['Phone_Number'].apply(format_sheet_phone)
            user = df_reg[df_reg['formatted_phone'] == str(pay_phone).strip()]
            
            if not user.empty:
                s_name, s_batch = user.iloc[0]['Name'], user.iloc[0]['Batch']
                st.markdown(f'<div class="profile-card"><h4>{s_name}</h4><p>Batch Stream: {s_batch}</p></div>', unsafe_allow_html=True)
                
                with st.form("pay_form", clear_on_submit=True):
                    p_month = st.selectbox("Select Target Billing Month", MONTHS)
                    p_amount = st.text_input("Transacted Amount (LKR)")
                    
                    if st.form_submit_button("Upload and Log Payment"):
                        if p_amount:
                            pay_txt = urllib.parse.quote(f"*Class Fee Log Receipt - GeoSense*\n\n"
                                                         f"👤 Student: {s_name}\n"
                                                         f"🎓 Stream Batch: {s_batch}\n"
                                                         f"📅 Target Month: {p_month}\n"
                                                         f"💰 Logged Value: LKR {p_amount}")
                                            
                            new_pay = pd.DataFrame([{"Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Name": s_name, "Phone_Number": pay_phone, "Batch": s_batch, "Month": p_month, "Amount": p_amount, "Status": "Paid"}])
                            df_pays_hist = conn.read(spreadsheet=DB_URL, worksheet="Payments", ttl=0)
                            conn.update(spreadsheet=DB_URL, worksheet="Payments", data=pd.concat([df_pays_hist, new_pay], ignore_index=True))
                            
                            st.markdown(f'<div class="paid-badge">Transaction Logged Successfully! ✅</div>', unsafe_allow_html=True)
                            st.link_button("📲 Submit Deposit Slip to Sir", f"https://wa.me/94717123334?text={pay_txt}")
            else:
                st.error("❌ Authentication Error: This phone footprint does not exist on our servers.")

# --- TAB 4: GIS INTERACTIVE STUDENT MAP ---
with menu[3]:
    st.markdown("### 📍 Live Geospatial Student GIS Density Map")
    st.write("Leveraging built-in GIS properties to showcase the live island-wide registration footprint.")
    if not df_global_students.empty and 'lat' in df_global_students.columns and 'lon' in df_global_students.columns:
        st.map(df_global_students[['lat', 'lon']].dropna(), color="#0f4c5c")
    else:
        st.info("Awaiting live GIS node coordination inputs.")

# --- TAB 5: LECTURE TIMETABLE CALENDAR ---
with menu[4]:
    st.markdown("### 📅 Live Academic Operational Schedule")
    st.iframe("https://calendar.google.com/calendar/embed?src=buddhika1999b%40gmail.com", height=500)

# --- TAB 6: PREMIUM LEARNING RESOURCES ---
with menu[5]:
    st.markdown("### 📚 Strategic Geography Analytics, Notes & Mapping Frameworks")
    tute_phone = st.text_input("Enter WhatsApp Authentication ID to access Cloud Assets", key="tute_check", max_chars=10, placeholder="e.g., 0711234567")
    
    if tute_phone and is_valid_phone(tute_phone):
        df_reg = df_global_students.copy() if not df_global_students.empty else pd.DataFrame()
        if not df_reg.empty and 'Phone_Number' in df_reg.columns:
            df_reg['formatted_phone'] = df_reg['Phone_Number'].apply(format_sheet_phone)
            user = df_reg[df_reg['formatted_phone'] == str(tute_phone).strip()]
            
            if not user.empty:
                s_name, s_batch = user.iloc[0]['Name'], user.iloc[0]['Batch']
                
                if 'Access' in user.columns and str(user.iloc[0]['Access']).strip().lower() == 'allow':
                    st.success(f"🔓 Access Granted! Welcome {s_name}. Cloud sync active.")
                    st.link_button("📥 Open Cloud Vault (Notes & Resources)", DRIVE_URL)
                else:
                    st.error("⏳ Security Approval Pending: Your teacher needs to manually whitelist your access profile parameters.")
                    req_msg = urllib.parse.quote(f"*Resource Vault Whitelist Request - GeoSense*\n\n"
                                                 f"👤 Student Identity: {s_name}\n"
                                                 f"🎓 Target Batch Node: {s_batch}\n"
                                                 f"📱 Comms Link ID: {tute_phone}\n\n"
                                                 f"Sir, please run a verification check on my logs and authorize cloud vault access keys.")
                    st.link_button("📲 Query Teacher for Whitelist Access", f"https://wa.me/94717123334?text={req_msg}")
            else:
                st.error("❌ Identification ID not verified on database servers.")

# --- ⚙️ TEACHER ADMINISTRATION FRAMEWORK ---
st.divider()
with st.expander("⚙️ GeoSense Educational Matrix Control Panel (Staff Only)"):
    admin_pw = st.text_input("Provide Administrative Authorization Key", type="password", key="secret_admin_pw")
    if admin_pw == "admin123":
        st.success("Admin Node Authenticated!")
        df_admin = df_global_students.copy() if not df_global_students.empty else pd.DataFrame()
        if not df_admin.empty:
            if 'Access' not in df_admin.columns: df_admin['Access'] = "Don't Allow"
            else: df_admin['Access'] = df_admin['Access'].fillna("Don't Allow").astype(str).replace({'nan': "Don't Allow", '': "Don't Allow"})
            
            df_admin['formatted_phone'] = df_admin['Phone_Number'].apply(format_sheet_phone)
            
            st.markdown("### 📋 Student Resource Access Management")
            view_opt = st.radio("Pipeline Filters", ["All Node Registry Logs", "Awaiting Resource Approval Only"], horizontal=True)
            display_df = df_admin if view_opt == "All Node Registry Logs" else df_admin[df_admin['Access'] == "Don't Allow"]
            
            if display_df.empty:
                st.info("No matching identity data packets active on the workspace pipeline.")
            else:
                for idx, row in display_df.iterrows():
                    col_info, col_status, col_btn = st.columns([3, 1, 1])
                    current_access = row['Access']
                    
                    col_info.write(f"👤 **{row['Name']}** ({row['Batch']}) - {row['formatted_phone']}")
                    
                    if current_access.lower() == 'allow':
                        col_status.markdown("<span style='color:#2ec4b6;font-weight:bold;'>Allowed 🔓</span>", unsafe_allow_html=True)
                        if col_btn.button("Revoke Access", key=f"admin_r_{idx}"):
                            df_admin.at[idx, 'Access'] = "Don't Allow"
                            df_admin_clean = df_admin.drop(columns=['formatted_phone'], errors='ignore')
                            conn.update(spreadsheet=DB_URL, worksheet="Student_DB", data=df_admin_clean)
                            st.rerun()
                    else:
                        col_status.markdown("<span style='color:#e36414;font-weight:bold;'>Locked 🔒</span>", unsafe_allow_html=True)
                        if col_btn.button("Grant Access", key=f"admin_g_{idx}"):
                            df_admin.at[idx, 'Access'] = "Allow"
                            df_admin_clean = df_admin.drop(columns=['formatted_phone'], errors='ignore')
                            conn.update(spreadsheet=DB_URL, worksheet="Student_DB", data=df_admin_clean)
                            st.rerun()
