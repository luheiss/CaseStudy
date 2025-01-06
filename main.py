import streamlit as st
from devices import Device
from queries import find_devices

st.title("Geräteverwaltung MCI")

tab1, tab2, tab3, tab4 = st.tabs(["Reservierungen", "Geräte", "Nutzer", "Wartungen"])
device_list=["Test1","Gerät_2"]

with tab1:
    st.header("Reservierungssystem")

    # 1. Gerät auswählen
    st.subheader("Gerät auswählen")
    devices_in_db = find_devices()

    if devices_in_db:
        selected_device = st.selectbox("Wählen Sie ein Gerät:", devices_in_db)
        if selected_device:
            device = Device.find_by_attribute("device_name", selected_device)
            st.write(f"Ausgewähltes Gerät: **{device.device_name}**")
        else:
            st.error("Kein Gerät ausgewählt.")
    else:
        st.warning("Keine Geräte verfügbar.")

    # 2. Reservierungsdaten eingeben
    st.subheader("Reservierungsdaten eingeben")
    if selected_device:
        with st.form("Reservierung anlegen"):
            reserving_user = st.text_input("Reservierender Nutzer (E-Mail):")
            reservation_start = st.date_input("Startdatum der Reservierung:")
            reservation_end = st.date_input("Enddatum der Reservierung:")


            if reservation_end < reservation_start:
                st.error("Das Enddatum muss nach dem Startdatum liegen.")

            submitted = st.form_submit_button("Reservierung anlegen")
            if submitted:
                if reservation_start <= reservation_end:
                    # Hier könnten Daten in die Datenbank gespeichert werden
                    st.success(f"Reservierung für **{selected_device}** angelegt: \n\n"
                               f"Reservierender Nutzer: {reserving_user}\n"
                               f"Startdatum: {reservation_start}\n"
                               f"Enddatum: {reservation_end}")
                else:
                    st.error("Bitte korrigieren Sie die Reservierungsdaten.")

        # Möglichkeit, Reservierungen zu löschen
        st.subheader("Reservierungen verwalten")
        if st.button("Reservierung entfernen"):
            st.warning("Reservierung wird entfernt (Datenbank-Integration erforderlich).")
    else:
        st.warning("Bitte wählen Sie ein Gerät, um fortzufahren.")


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
  