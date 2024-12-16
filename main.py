import streamlit as st
#
#
## Initialisiere `authentication_status` im Session State
#if "authentication_status" not in st.session_state:
#    st.session_state["authentication_status"] = None
#if "name" not in st.session_state:
#    st.session_state["name"] = None
#
## Admin-Login-Bereich oben links
#with st.sidebar:
#    st.header("Login")
#    username = st.text_input("Benutzername")
#    password = st.text_input("Passwort", type="password")
#    if st.button("Login"):
#        if username == "admin" and password == "1234":  # Beispiel-Benutzername und Passwort
#            st.success("Login erfolgreich!")
#            st.session_state["authentication_status"] = True
#            st.session_state["name"] = username
#        else:
#            st.error("Falscher Benutzername oder Passwort")
#            st.session_state["authentication_status"] = False
#
#tab0 ,tab1, tab2, tab3, tab4 = st.tabs(["🏠Home", "Reservierungen", "Geräte", "Nutzer", "Wartungen"])
#
#with tab0:
#    st.header("Home")
#    if st.session_state["authentication_status"]:
#        st.write(f'Welcome *{st.session_state["name"]}*')
#        st.title('Some content')
#        if st.button('Logout'):
#            st.session_state["authentication_status"] = False
#    else:
#        st.write("Hallo Gast. Als Gast kannst du nur Geräte reservieren!")
#with tab1:
#    st.header("Reserviernungssystem")
#    #st.write("# Reserviernungssystem")
#with tab2:
#    st.header("Geräte- Verwaltung")
#with tab3:
#    st.header("Nutzer- Verwaltung")
#with tab4:
#    st.header("Wartungsmanagement")
#
col1, col2 = st.columns(2)


with col1:
    if st.button("Baloons"):
        st.balloons()
with col2:
   st.write("Test")


#if st.session_state["authentication_status"]:
#    authenticator.logout('Logout', 'main')
#    st.write(f'Welcome *{st.session_state["name"]}*')
#    st.title('Some content')
#elif st.session_state["authentication_status"] == False:
#    st.error('Username/password is incorrect')
#elif st.session_state["authentication_status"] == None:
#    st.warning('Please enter your username and password')



#if "sb_current_device" not in st.session_state:
 #   st.session_state.sb_current_device = ""

# Eine Überschrift der ersten Ebene
#st.write("# Gerätemanagement")

# Eine Überschrift der zweiten Ebene
#st.write("## Geräteauswahl")

# Eine Auswahlbox mit hard-gecoded Optionen, das Ergebnis

#st.session_state.sb_current_device = st.selectbox(label='Gerät auswählen',
 #       options = ["Gerät_A", "Gerät_B"])

#st.write(F"Das ausgewählte Gerät ist {st.session_state.sb_current_device}")
