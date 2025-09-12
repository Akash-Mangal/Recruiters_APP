import streamlit as st


if "role" not in st.session_state:
    st.session_state.role = "Candidate" 

ROLES = [None, "Candidate", "Recruiter", "Admin"]

def login():
    st.header("Log in")
    role = st.selectbox("Choose your role", ROLES)
    if st.button("Log in"):
        st.session_state.role = role
        st.rerun()

def logout():
    st.session_state.role = None
    st.rerun()

role = st.session_state.role

logout_page = st.Page(logout, title="Log out", icon=":material/logout:")
settings = st.Page("settings.py", title="Settings", icon=":material/settings:")

ats = st.Page(
    "candidate/ats.py",
    title="ATS",
    icon=":material/help:",
    default=(role == "Candidate"),
)
request_2 = st.Page(
    "candidate/request_2.py", title="Request 2", icon=":material/bug_report:"
)

respond_1 = st.Page(
    "respond/respond_1.py",
    title="Respond 1",
    icon=":material/healing:",
    default=(role == "Recruiter"),
)
respond_2 = st.Page(
    "respond/respond_2.py", title="Respond 2", icon=":material/handyman:"
)
admin_1 = st.Page(
    "admin/admin_1.py",
    title="Admin 1",
    icon=":material/person_add:",
    default=(role == "Admin"),
)
admin_2 = st.Page("admin/admin_2.py", title="Admin 2", icon=":material/security:")

account_pages = [logout_page, settings]
request_pages = [ats, request_2]
respond_pages = [respond_1, respond_2]
admin_pages = [admin_1, admin_2]

st.title("Recruiter APP")
# st.logo("images/photo-1548407260-da850faa41e3.avif", icon_image="images/icon_blue.png")

page_dict = {}

if st.session_state.role in ["Candidate", "Admin"]:
    page_dict["Candidate"] = request_pages
if st.session_state.role in ["Recruiter", "Admin"]:
    page_dict["Respond"] = respond_pages
if st.session_state.role == "Admin":
    page_dict["Admin"] = admin_pages

if len(page_dict) > 0:
    pg = st.navigation({"Account": account_pages} | page_dict)
else:
    pg = st.navigation([st.Page(login)])

pg.run()
