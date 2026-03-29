import streamlit as st
from PIL import Image
import base64
import sqlite3

st.set_page_config(page_title="Prayogam Foundation", layout="wide")

st.markdown("""
<style>
.stApp{
    background: linear-gradient(135deg,#1a1a2e,#16213e,#0f3460);
    color:white;
}
.title{
    font-size:48px;
    font-weight:700;
    text-align:center;
    margin-bottom:40px;
    background: linear-gradient(90deg,#ff9a9e,#fad0c4,#fbc2eb);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}
.desc{
    text-align:justify;
    font-size:20px;
    line-height:1.8;
    margin-bottom:40px;
    color:#e6e6e6;
}
[data-testid="column"]{
    display:flex;
    flex-direction:column;
    justify-content:center;
}
.click-img img{
    border-radius:20px;
    transition:0.35s;
    cursor:pointer;
    box-shadow:0 15px 40px rgba(0,0,0,0.4);
}
.click-img img:hover{
    transform:scale(1.05) rotate(1deg);
}
button{
    background: linear-gradient(90deg,#ff758c,#ff7eb3);
    color:white !important;
    border:none;
    border-radius:12px;
    font-size:18px;
    padding:10px 20px;
}
button:hover{
    transform:scale(1.05);
}
label{
    color:white !important;
    font-weight:500;
}

/* Radio button styles: make radio control and labels white */
/* Broad and specific selectors to override Streamlit's styles */
.stRadio label, .stRadio, .stRadio * { color: white !important; }
div[role="radiogroup"] label { color: white !important; }
input[type="radio"] { accent-color: white !important; }

</style>
""", unsafe_allow_html=True)

conn = sqlite3.connect("artists.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS artist_users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
Name TEXT,
Phone_Number TEXT UNIQUE
)
""")
conn.commit()

if "page" not in st.session_state:
    st.session_state.page = "home"

def img_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def home_page():
    st.markdown('<div class="title">Prayogam Foundation – Where Art Meets Opportunity</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1.2,1])

    with col1:
        st.markdown("<br><br>", unsafe_allow_html=True)

        st.markdown("""
        <div class="desc">
        Prayogam Foundation provides a digital platform designed to connect creative artists with audiences and event organizers.
        Artists from diverse fields can register on the website to showcase their talent and artistic journey, while users can
        explore, select, and invite artists for shows, events, and performances. Through this initiative, we aim to revive art,
        empower artists, and create meaningful opportunities that celebrate both the art and the artist.
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns([1,2,1])
        with c2:
            if st.button("Begin the Journey"):
                st.session_state.page = "options"
                st.rerun()

    with col2:
        img = Image.open("Logo.png")
        st.image(img, width=600)

def options_page():

    b1, b2, b3 = st.columns([1,8,1])

    st.markdown("<h2 style='text-align:center;'>Choose Registration Type</h2>", unsafe_allow_html=True)

    artist64 = img_to_base64("Artist.png")
    user64 = img_to_base64("User.png")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            f"""
            <div class="click-img">
            <a href="?nav=artist">
            <div style="text-align:center;">
            <img src="data:image/png;base64,{artist64}" width="75%">
            </div>
            </a>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class="click-img">
            <a href="?nav=user">
            <div style="text-align:center;">
            <img src="data:image/png;base64,{user64}" width="75%">
            </div>
            </a>
            </div>
            """,
            unsafe_allow_html=True,
        )

def artist_page():


    if "artist_logged" not in st.session_state:
        st.session_state.artist_logged = False

    if "artist_phone" not in st.session_state:
        st.session_state.artist_phone = None

    if "edit_mode" not in st.session_state:
        st.session_state.edit_mode = False

    st.markdown("<h1 style='text-align:center;'>Artist Portal</h1>", unsafe_allow_html=True)

    left, center, right = st.columns([1,2,1])

    with center:

        if not st.session_state.artist_logged:

            option = st.radio("Choose Option", ["Register", "Login"], horizontal=True)

            if option == "Register":

                Name = st.text_input("Name")
                Phone_Number = st.text_input("Phone Number", max_chars=10)

                if st.button("Register", use_container_width=True):

                    if not Phone_Number.isdigit() or len(Phone_Number) != 10:
                        st.error("Enter valid 10 digit mobile number")

                    elif Name and Phone_Number:

                        c.execute("SELECT * FROM artist_users WHERE Phone_Number=?", (Phone_Number,))
                        user = c.fetchone()

                        if user:
                            st.warning("User already registered. Please login.")
                        else:
                            c.execute(
                                "INSERT INTO artist_users(Name,Phone_Number) VALUES(?,?)",
                                (Name, Phone_Number)
                            )
                            conn.commit()
                            st.success("Registration successful. Now login.")

                    else:
                        st.warning("Enter all details")

            elif option == "Login":

                Phone_Number = st.text_input("Enter Registered Phone Number", max_chars=10)

                if st.button("Login", use_container_width=True):

                    if not Phone_Number.isdigit() or len(Phone_Number) != 10:
                        st.error("Enter valid 10 digit mobile number")

                    else:
                        c.execute("SELECT * FROM artist_users WHERE Phone_Number=?", (Phone_Number,))
                        user = c.fetchone()

                        if user:
                            st.session_state.artist_logged = True
                            st.session_state.artist_phone = Phone_Number
                            st.rerun()
                        else:
                            st.error("User not found. Please register.")

        else:

            st.markdown("### Your Profile Details")

            c.execute(
                "SELECT full_name, art, description, area, drive FROM artist_profile WHERE phone=?",
                (st.session_state.artist_phone,)
            )
            profile = c.fetchone()

            if profile and not st.session_state.edit_mode:

                st.write("**Full Name:**", profile[0])
                st.write("**Art Category:**", profile[1])
                st.write("**Description:**", profile[2])
                st.write("**Region:**", profile[3])
                st.write("**Google Drive Link:**", profile[4])

                col1, col2 = st.columns(2)

                with col1:
                    if st.button("Edit Profile"):
                        st.session_state.edit_mode = True
                        st.rerun()

                with col2:
                    if st.button("Logout"):
                        st.session_state.artist_logged = False
                        st.session_state.artist_phone = None
                        st.session_state.edit_mode = False
                        st.rerun()

            elif profile and st.session_state.edit_mode:

                full_name = st.text_input("Full Name", value=profile[0])
                art = st.text_input("Art Category", value=profile[1])
                desc = st.text_area("Art Description", value=profile[2])
                area = st.text_input("Region / Area", value=profile[3])
                drive = st.text_input("Google Drive Link", value=profile[4])

                if st.button("Update Profile", use_container_width=True):

                    c.execute("""
                        UPDATE artist_profile
                        SET full_name=?, art=?, description=?, area=?, drive=?
                        WHERE phone=?
                    """, (full_name, art, desc, area, drive, st.session_state.artist_phone))

                    conn.commit()
                    st.session_state.edit_mode = False
                    st.success("Profile Updated Successfully")
                    st.rerun()

            else:

                st.info("No profile found. Please create your profile.")

                full_name = st.text_input("Full Name")
                art = st.text_input("Art Category")
                desc = st.text_area("Art Description")
                area = st.text_input("Region / Area")
                drive = st.text_input("Google Drive Link")

                if st.button("Submit Profile", use_container_width=True):

                    c.execute(
                        "INSERT INTO artist_profile(phone,full_name,art,description,area,drive) VALUES(?,?,?,?,?,?)",
                        (st.session_state.artist_phone, full_name, art, desc, area, drive)
                    )
                    conn.commit()

                    st.success("Profile saved")
                    st.rerun()
                
def user_page():
    st.markdown(
        """
        <style>
        .card{
            background:white;
            color:black;
            padding:20px;
            border-radius:15px;
            box-shadow:0 10px 25px rgba(0,0,0,0.2);
            margin-bottom:20px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.title("Available Artists")

    conn = sqlite3.connect("artists.db", check_same_thread=False)
    c = conn.cursor()

    c.execute("SELECT full_name, art, description, area, drive FROM artist_profile")
    artists = c.fetchall()

    if artists:
        cols = st.columns(2)
        for i, artist in enumerate(artists):
            with cols[i % 2]:
                st.markdown(
                    f"""
                    <div class="card">
                    <b>Name:</b> {artist[0]}<br><br>
                    <b>Art:</b> {artist[1]}<br><br>
                    <b>Description:</b> {artist[2]}<br><br>
                    <b>Region:</b> {artist[3]}<br><br>
                    <b>Portfolio:</b> {artist[4]}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    else:
        st.info("No artists registered yet")

query = st.query_params

if "nav" in query:
    if query["nav"] == "artist":
        st.session_state.page = "artist"
    elif query["nav"] == "user":
        st.session_state.page = "user"

if st.session_state.page == "home":
    home_page()
elif st.session_state.page == "options":
    options_page()
elif st.session_state.page == "artist":
    artist_page()
else:
    user_page()
