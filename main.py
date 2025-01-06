import streamlit as st
from streamlit_echarts import st_echarts



tab1, tab2, tab3, tab4 = st.tabs(["Reservierungen", "Geräte", "Nutzer", "Wartungen"])


with tab1:
    st.header("Reservierungssystem")
    st.text_input("Datum", key="ti_tab1_name")
with tab2:
    st.header("Geräte- Verwaltung")
    st.text_input("Gerät", key="tt")
with tab3:
    st.header("Nutzer- Verwaltung")
with tab4:
    st.header("Wartungsmanagement")
    option = {
        "xAxis": {
            "type": "category",
            "data": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        },
        "yAxis": {"type": "value"},
        "series": [{"data": [820, 932, 901, 934, 1290, 1330, 1320], "type": "line"}],
    }
    st_echarts(options=option, height="400px")
#col1, col2 = st.columns(2)
#
#
#with col1:
#    if st.button("Baloons"):
#        st.balloons()
#with col2:
#   st.write("Test")
#

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
