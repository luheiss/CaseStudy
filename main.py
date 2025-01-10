import streamlit as st
from devices import Device
from users import User
import queries as qr

st.title("Geräteverwaltung MCI")

tab1, tab2, tab3, tab4 = st.tabs(["Reservierungen", "Geräte", "Nutzer", "Wartungen"])
#device_list=["Test1","Gerät_2"]

with tab1:
    st.header("Reservierungssystem")

    # 1. Gerät auswählen
    st.subheader("Gerät auswählen")
    devices_in_db = qr.find_devices()

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
    # Eine Überschrift der ersten Ebene
    devices_in_db = qr.find_devices()
    user_in_db = qr.find_users()
    st.write("# Gerätemanagement")

    col1, col2 = st.columns(2)
    with col1:
        col_add_device = st.checkbox("Neues Gerät anlegen", True)
    with col2: 
        col_change_device = st.checkbox("Geräte Einstellungen ändern")

    if col_add_device:
        new_device= st.text_input("Neues Gerät anlegen", key="add_new_device")
        #user_id= st.text_input("User", key="add_user")
        user_id= st.selectbox('User auswählen', user_in_db)
        if st.button("Gerät anlegen"):
            if not new_device or not user_id:
                st.error("Bitte gültige Namen eingeben!")
            else:
                new=Device(device_name=new_device, managed_by_user_id=user_id)
                new.store_data()
                st.success(f"Gerät *{new_device}* wurde erfolgreich angelegt!")

        
    
    if col_change_device:
        if devices_in_db:
            current_device_name = st.selectbox('Gerät auswählen',options=devices_in_db, key="sbDevice")

            if current_device_name in devices_in_db:
                loaded_device = Device.find_by_attribute("device_name", current_device_name)
                if loaded_device:
                    st.write(f"Loaded Device: {loaded_device}")
                else:
                    st.error("Device not found in the database.")

                with st.form("Device"):
                    st.write(loaded_device.device_name)

                    text_input_val = st.text_input("Geräte-Verantwortlicher", value=loaded_device.managed_by_user_id)
                    loaded_device.set_managed_by_user_id(text_input_val)

                    # Every form must have a submit button.
                    submitted = st.form_submit_button("Submit")
                    if submitted:
                        loaded_device.store_data()
                        st.write("Data stored.")
                        st.rerun()
            else:
                st.error("Selected device is not in the database.")
        else:
            st.write("No devices found.")
            st.stop()

    st.write("Session State:")
    st.session_state

with tab3:
    user_in_db = qr.find_users()
    st.header("Nutzer- Verwaltung")
    new_user_name= st.text_input("Name")
    new_user_email= st.text_input("Email")
    if st.button("Benutzer anlegen"):
        if not new_user_name or not new_user_email:
            st.error("Bitte gültige Namen eingeben!")
        elif new_user_email == user_in_db:
            st.error(f"Ein Benutzer mit der email: *{new_user_email}* existiert bereits!")

        else:
            new=User(new_user_email, new_user_name)
            new.store_data()
            st.success(f"Benutzer *{new_user_name}* wurde erfolgreich angelegt!")


with tab4:
    st.header("Wartungsmanagement")
  