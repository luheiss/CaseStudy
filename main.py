import streamlit as st
from streamlit_echarts import st_echarts



tab1, tab2, tab3, tab4 = st.tabs(["Reservierungen", "Geräte", "Nutzer", "Wartungen"])
device_list=["Test1","Gerät_2"]

with tab1:
    st.header("Reservierungssystem")
    st.text_input("Datum", key="ti_tab1_name")

with tab2:
    st.header("Geräte- Verwaltung")
    new_device= st.text_input("Neues Gerät anlegen", key="add_new_device")
    if st.button("Gerät hinzufügen"):
       if new_device:  # Prüfe, ob das Eingabefeld nicht leer ist
           device_list.append(new_device)
           st.success(f"Gerät '{new_device}' hinzugefügt!")
       else:
           st.warning("Bitte einen gültigen Gerätenamen eingeben!")

    current_device = st.selectbox(label='Gerät auswählen', options = device_list)
    st.write(F"Das ausgewählte Gerät ist {current_device}")

with tab3:
    st.header("Nutzer- Verwaltung")

with tab4:
    st.header("Wartungsmanagement")
  