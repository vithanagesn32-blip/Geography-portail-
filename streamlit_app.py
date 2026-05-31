import streamlit as st
import pandas as pd
from datetime import datetime
import streamlit_folium as st_folium
import folium

# ==========================================
# 🛠️ 3 පියවර: කෝඩ් එක ඇතුළේ වෙනස් කළ යුතු තැන් (Code Customization)
# ==========================================

# 1. පින්තූර ලින්ක්ස් (ImgBB Direct Links)
BANNER_HOME = "https://i.ibb.co/your-home-banner-link.jpg"
BANNER_REG = "https://i.ibb.co/your-reg-banner-link.jpg"
BANNER_MAP = "https://i.ibb.co/your-map-banner-link.jpg"
BANNER_CLASS = "https://i.ibb.co/your-class-banner-link.jpg"

# 2. Page Title & Class Details
PAGE_TITLE = "Geo-Scholar - Geography Portal"
CLASS_NAME = "භූගෝල විද්‍යාව (Geography)"
TEACHER_NAME = "සහන් විතානගේ"  # මෙතනට යාලුවගේ නම දාන්න

# 3. WhatsApp සහ Zoom විස්තර
WHATSAPP_2026 = "https://chat.whatsapp.com/example2026"
WHATSAPP_2027 = "https://chat.whatsapp.com/example2027"
WHATSAPP_2028 = "https://chat.whatsapp.com/example2028"

ZOOM_ID = "123 456 7890"
ZOOM_PASSCODE = "Geo2028"
ZOOM_LINK = "https://zoom.us/j/example"

# 4. දුරකථන අංකය (WhatsApp Format: 947xxxxxxxx)
SUPPORT_PHONE = "94771234567" 

# 5. Google Drive (Tutes) සහ Calendar ලින්ක්ස්
DRIVE_LINK = "https://drive.google.com/drive/folders/example"
CALENDAR_EMBED = "https://calendar.google.com/calendar/embed?src=en.lk%23holiday%40group.v.calendar.google.com" # දැනට ලංකාවේ නිවාඩු දින දින දර්ශනය

# 6. Admin Password
ADMIN_PASSWORD = "GeoAdmin@2028"

# ==========================================
# ⚙️ පද්ධතියේ ක්‍රියාකාරී කෝඩ් එක (Logic) - මේවා වෙනස් කරන්න එපා
# ==========================================

st.set_page_config(page_title=PAGE_TITLE, page_icon="🗺️", layout="wide")

# Google Sheet එක සම්බන්ධ කිරීම (Secrets මඟින්)
try:
    gsheet_url = st.secrets["connections"]["gsheets"]["spreadsheet"]
    # Sheet IDs (Tab names අනුව)
    sheet_url_students = gsheet_url.replace("/edit?usp=sharing", "/gviz/tq?tqx=out:csv&sheet=Student_DB")
    sheet_url_payments = gsheet_url.replace("/edit?usp=sharing", "/gviz/tq?tqx=out:csv&sheet=Payments")
except Exception as e:
    st.error("Error: Google Sheet Secrets සෙට් කර නැත! කරුණාකර 4 වන පියවර බලන්න.")
    st.stop()

# Sidebar Navigation
st.sidebar.title(f"📌 {TEACHER_NAME} සර්ගේ පන්තිය")
page = st.sidebar.radio("යන්න මෙතනින්:", ["ඇතුළත් වීම (Home)", "නව ලියාපදිංචිය (Register)", "පන්ති කාමරය (Classroom)", "ගෙවීම් තොරතුරු (Payments)", "සිසුන්ගේ සිතියම (Student Map)", "පරිපාලන පැනලය (Admin)"])

# ----------------- HOME PAGE -----------------
if page == "ඇතුළත් වීම (Home)":
    st.image(BANNER_HOME, use_container_width=True)
    st.title(f"👋 සාදරයෙන් පිළිගන්නවා! {CLASS_NAME}")
    st.subheader(f"මෙහෙයවීම: {TEACHER_NAME} (Lecturer)")
    
    st.markdown(f"""
    ඔබේ භූගෝල විද්‍යා අධ්‍යාපන ගමන වඩාත් තාක්ෂණික සහ පහසු එකක් කිරීමට මෙම ඩිජිටල් පද්ධතිය නිර්මාණය කර ඇත. 
    පහත සේවාවන් ලබා ගැනීමට වම්පස ඇති **Navigation Menu** එක භාවිතා කරන්න:
    * **Register:** පන්තියට අලුතින්ම එකතු වන සිසුන් සඳහා.
    * **Classroom:** Zoom ලින්ක්, Tutes සහ WhatsApp ගෲප් වලට සම්බන්ධ වීමට.
    * **Payments:** මාසික පන්ති ගාස්තු ගෙවීම් වාර්තා ඇතුළත් කිරීමට.
    
    📞 ඕනෑම ගැටලුවකදී සම්බන්ධ කරගන්න: [WhatsApp හරහා මැසේජ් කරන්න](https://wa.me/{SUPPORT_PHONE})
    """)

# ----------------- REGISTRATION PAGE -----------------
elif page == "නව ලියාපදිංචිය (Register)":
    st.image(BANNER_REG, use_container_width=True)
    st.title("📝 සිසුවා ලියාපදිංචි කිරීම")
    st.write("පහත පෝරමය නිවැරදිව පුරවා පද්ධතියට ඇතුළත් වන්න.")
    
    with st.form("reg_form", clear_on_submit=True):
        name = st.text_input("සම්පූර්ණ නම (Name in Full):")
        phone = st.text_input("දුරකථන අංකය (WhatsApp Number):")
        batch = st.selectbox("කණ්ඩායම (Batch):", ["2026 A/L", "2027 A/L", "2028 A/L"])
        district = st.text_input("දිස්ත්‍රික්කය (District):")
        
        st.write("📍 සිතියමේ ඔබව පෙන්වීමට ආසන්න ලක්ෂ්‍යය (Latitude & Longitude) ඇතුළත් කරන්න:")
        lat = st.number_input("Latitude (උදා: 7.2906)", format="%.4f", value=7.2906)
        lon = st.number_input("Longitude (උදා: 80.6337)", format="%.4f", value=80.6337)
        
        submitted = st.form_submit_button("ලියාපදිංචි වන්න")
        if submitted:
            if name and phone and district:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # මෙතනදී කෙලින්ම ගූගල් ශීට් එකට ලියන්න නම් Google Forms/Apps Script එකක් ඕන වෙනවා. 
                # දැනට Streamlit එකෙන් පෙන්වනවා. (Apps script එක පසුව සෙට් කරමු)
                st.success(f"🎉 ස්තූතියි {name}! ඔබ සාර්ථකව ලියාපදිංචි වුණා. (කරුණාකර මෙම දත්ත පරිපාලක වෙත යවන්න)")
                st.info(f"දත්ත: {timestamp}, {name}, {phone}, {batch}, {district}, {lat}, {lon}, Pending")
            else:
                st.warning("කරුණාකර සියලුම විස්තර ඇතුළත් කරන්න!")

# ----------------- CLASSROOM PAGE -----------------
elif page == "පන්ති කාමරය (Classroom)":
    st.image(BANNER_CLASS, use_container_width=True)
    st.title("📚 මගේ පන්ති කාමරය")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎥 සජීවී Zoom පන්තිය")
        st.write(f"**Meeting ID:** {ZOOM_ID}")
        st.write(f"**Passcode:** {ZOOM_PASSCODE}")
        st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ") # නිකන් Demo එකක්, ඕන නම් අයින් කරන්න
        st.markdown(f'<a href="{ZOOM_LINK}" target="_blank"><button style="background-color:#2D8CFF;color:white;padding:10px;border:none;border-radius:5px;width:100%;">Zoom පන්තියට සම්බන්ධ වන්න</button></a>', unsafe_allow_text=True)
        
        st.subheader("📁 නිබන්ධන (Tutes & Notes)")
        st.markdown(f'<a href="{DRIVE_LINK}" target="_blank"><button style="background-color:#198754;color:white;padding:10px;border:none;border-radius:5px;width:100%;">Google Drive එකට යන්න</button></a>', unsafe_allow_text=True)

    with col2:
        st.subheader("💬 WhatsApp සමූහයන් (Groups)")
        st.markdown(f"[🟢 2026 Batch WhatsApp Group]({WHATSAPP_2026})")
        st.markdown(f"[🟢 2027 Batch WhatsApp Group]({WHATSAPP_2027})")
        st.markdown(f"[🟢 2028 Batch WhatsApp Group]({WHATSAPP_2028})")
        
        st.subheader("📅 පන්ති කාලසටහන (Calendar)")
        st.markdown(f'<iframe src="{CALENDAR_EMBED}" style="border: 0" width="100%" height="250" frameborder="0" scrolling="no"></iframe>', unsafe_allow_text=True)

# ----------------- PAYMENTS PAGE -----------------
elif page == "ගෙවීම් තොරතුරු (Payments)":
    st.title("💳 මාසික පන්ති ගාස්තු තොරතුරු")
    st.write("ඔබේ මාසික ගෙවීම් රිසිට්පත් විස්තර මෙතැනින් ඇතුළත් කරන්න.")
    
    with st.form("payment_form", clear_on_submit=True):
        p_name = st.text_input("සිසුවාගේ නම:")
        p_phone = st.text_input("දුරකථන අංකය:")
        p_batch = st.selectbox("කණ්ඩායම:", ["2026 A/L", "2027 A/L", "2028 A/L"])
        p_month = st.selectbox("ගෙවීම් කළ මාසය:", ["ජනවාරි", "පෙබරවාරි", "මාර්තු", "අප්‍රේල්", "මැයි", "ජූනි", "ජූලි", "අගෝස්තු", "සැප්තැම්බර්", "ඔක්තෝබර්", "නොවැම්බර්", "දෙසැම්බර්"])
        p_amount = st.text_input("මුදල (Rs.):", value="2000")
        
        st.info("💡 දැනට පද්ධතිය පරීක්ෂණ මට්ටමේ පවතින බැවින් ගෙවීම් තහවුරු කිරීමට රිසිට්පත සර්ගේ WhatsApp එකට දාන්න.")
        p_submitted = st.form_submit_button("ගෙවීම් විස්තර ඇතුළත් කරන්න")
        if p_submitted:
            st.success("👍 ඔබේ ගෙවීම් විස්තර ලැබුණා. පරිපාලක විසින් එය පරීක්ෂා කර සක්‍රීය කරනු ඇත.")

# ----------------- MAP PAGE -----------------
elif page == "සිසුන්ගේ සිතියම (Student Map)":
    st.image(BANNER_MAP, use_container_width=True)
    st.title("🗺️ අපේ පන්තියේ සිසුන් ලංකාව වටා")
    st.write("පන්තියේ සිසුන් විසිරී සිටින ආකාරය දැක්වෙන සිතියම (ලියාපදිංචි දත්ත අනුව).")
    
    # මැප් එක මැද ලංකාවට සෙට් කිරීම
    m = folium.Map(location=[7.8731, 80.7718], zoom_start=7)
    
    # නිදර්ශන ලක්ෂ්‍යයන් කිහිපයක් (Demo data)
    folium.Marker([7.2906, 80.6337], popup="Kandy Center", icon=folium.Icon(color="red", icon="info-sign")).add_to(m)
    folium.Marker([6.9271, 79.8612], popup="Colombo Student", icon=folium.Icon(color="blue")).add_to(m)
    
    st_folium.st_folium(m, width=1000, height=500)

# ----------------- ADMIN PANEL -----------------
elif page == "පරිපාලන පැනලය (Admin)":
    st.title("🔒 පරිපාලන පැනලය (Admin Panel)")
    
    pwd = st.text_input("මුරපදය ඇතුළත් කරන්න (Password):", type="password")
    if pwd == ADMIN_PASSWORD:
        st.success("Access Granted! සාදරයෙන් පිළිගන්නවා සර්.")
        
        tab1, tab2 = st.tabs(["සිසුන්ගේ දත්ත (Students)", "ගෙවීම් දත්ත (Payments)"])
        
        with tab1:
            st.subheader("👥 ලියාපදිංචි වී ඇති සිසුන්")
            try:
                df_students = pd.read_csv(sheet_url_students)
                st.dataframe(df_students)
            except:
                st.warning("Google Sheet එකේ 'Student_DB' කියන Tab එක සොයාගත නොහැක හෝ දත්ත නැත.")
                
        with tab2:
            st.subheader("💰 ලැබී ඇති ගෙවීම්")
            try:
                df_payments = pd.read_csv(sheet_url_payments)
                st.dataframe(df_payments)
            except:
                st.warning("Google Sheet එකේ 'Payments' කියන Tab එක සොයාගත නොහැක හෝ දත්ත නැත.")
    elif pwd != "":
        st.error("වැරදි මුරපදයක්! නැවත උත්සාහ කරන්න.")
