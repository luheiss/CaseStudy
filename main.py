import streamlit as st
from devices import Device
from users import User
from reservation import Reservation
import queries as qr

st.title("Geräteverwaltung MCI")

tab1, tab2, tab3, tab4 = st.tabs(["Reservierungen", "Geräte", "Nutzer", "Wartungen"])
#device_list=["Test1","Gerät_2"]

with tab1:
    st.header("Reservierungssystem")
    devices_in_db = qr.find_devices()
    user_in_db = qr.find_users()
    st.subheader("Gerät auswählen")
    selected_device = st.selectbox("Wählen Sie ein Gerät:", devices_in_db)
    selected_user = st.selectbox("Wähle Benutzer", user_in_db)
    with st.form("Reservierung anlegen"):
        reservation_start = st.date_input("Startdatum der Reservierung:")
        reservation_end = st.date_input("Enddatum der Reservierung:")
        submitted = st.form_submit_button("Reservierung anlegen")
        if submitted:
             if reservation_start <= reservation_end:
                # Hier könnten Daten in die Datenbank gespeichert werden
                Reservation(selected_user,selected_device,reservation_start,reservation_end)
                Reservation.store_data()
                st.success(f"Reservierung für **{selected_device}** angelegt: \n\n"
                    f"Reservierender Nutzer: {selected_user}\n"
                    f"Startdatum: {reservation_start}\n"
                    f"Enddatum: {reservation_end}")

    # # 1. Gerät auswählen
    # if devices_in_db:
    #     selected_device = st.selectbox("Wählen Sie ein Gerät:", devices_in_db)
    #     if selected_device:
    #         device = Device.find_by_attribute("device_name", selected_device)
    #         st.write(f"Ausgewähltes Gerät: **{device.device_name}**")
    #     else:
    #         st.error("Kein Gerät ausgewählt.")
    # else:
    #     st.warning("Keine Geräte verfügbar.")

    # # 2. Reservierungsdaten eingeben
    # st.subheader("Reservierungsdaten eingeben")
    # if selected_device:
    #     with st.form("Reservierung anlegen"):
    #         reserving_user = st.text_input("Reservierender Nutzer (E-Mail):")
    #         reservation_start = st.date_input("Startdatum der Reservierung:")
    #         reservation_end = st.date_input("Enddatum der Reservierung:")


    #         if reservation_end < reservation_start:
    #             st.error("Das Enddatum muss nach dem Startdatum liegen.")

    #         submitted = st.form_submit_button("Reservierung anlegen")
    #         if submitted:
    #             if reservation_start <= reservation_end:
    #                 # Hier könnten Daten in die Datenbank gespeichert werden
    #                 st.success(f"Reservierung für **{selected_device}** angelegt: \n\n"
    #                            f"Reservierender Nutzer: {reserving_user}\n"
    #                            f"Startdatum: {reservation_start}\n"
    #                            f"Enddatum: {reservation_end}")
    #             else:
    #                 st.error("Bitte korrigieren Sie die Reservierungsdaten.")

    #     # Möglichkeit, Reservierungen zu löschen
    #     st.subheader("Reservierungen verwalten")
    #     if st.button("Reservierung entfernen"):
    #         st.warning("Reservierung wird entfernt (Datenbank-Integration erforderlich).")
    # else:
    #     st.warning("Bitte wählen Sie ein Gerät, um fortzufahren.")


with tab2:
    # Überschrift
    st.write("# Gerätemanagement")

    # Alle Geräte und Benutzer aus der Datenbank laden
    devices_in_db = qr.find_devices()
    user_in_db = qr.find_users()
    tab5, tab6 = st.tabs(["Neues Gerät anlegen","Geräte Einstellungen ändern"])


    with tab5:
        new_device= st.text_input("Neues Gerät anlegen", key="add_new_device")
        #user_id= st.text_input("User", key="add_user")
        user_id= st.selectbox('User auswählen', user_in_db)
        if st.button("Gerät anlegen"):
            if not new_device or not user_id:
                st.error("Bitte Name eingeben!")

            elif new_device == Device.find_by_attribute("device_name", new_device):
                 st.error("Dieses Gerät ist schon in der Datenbank hinterlegt!")
            else:
                new = Device(device_name=new_device, managed_by_user_id=user_id)
                new.store_data()
                st.success(f"Gerät *{new_device}* wurde erfolgreich angelegt!")

    with tab6:
        if devices_in_db:
            current_device_name = st.selectbox('Gerät auswählen',options=devices_in_db, key="sbDevice")
            if current_device_name in devices_in_db:
                loaded_device = Device.find_by_attribute("device_name", current_device_name)

                if loaded_device:
                    st.write(f"Ausgewähltes Gerät: **{loaded_device.device_name}**")

                with st.form("Geräte-Einstellungen"):
                                    new_manager= st.selectbox('User ändern', user_in_db)
                                    submitted = st.form_submit_button("Speichern")
                                    if submitted:
                                        loaded_device.set_managed_by_user_id(new_manager)
                                        loaded_device.store_data()
                                        st.success(f"Änderungen für **{loaded_device.device_name}** wurden gespeichert!")
                                        st.rerun()

with tab3:
    #devices_in_db = qr.find_devices()
    user_in_db = qr.find_users()
    st.header("Nutzer- Verwaltung")
    tab7,tab8= st.tabs(["Neuen Nutzer anlegen", "Nutzer bearbeiten"])
    with tab7:
        new_user_name= st.text_input("Name")
        new_user_email= st.text_input("Email")
        if st.button("Benutzer anlegen"):
            if not new_user_name or not new_user_email:
                st.error("Bitte gültige Namen eingeben!")
            elif new_user_email == user_in_db:
                st.error(f"Ein Benutzer mit der email: *{new_user_email}* existiert bereits!")

            else:
                newUser=User(new_user_email,new_user_name)
                newUser.store_data()
                st.success(f"Benutzer *{new_user_name}* wurde erfolgreich angelegt!")
    with tab8:
        st.write("Edit user")
        current_user= st.selectbox("User",user_in_db)
        if current_user in user_in_db:
                loaded_user = User.find_by_attribute("id", current_user)
    
        with st.form("User-Einstellungen"):
            new_name= st.text_input(f"Name: {loaded_user.name}", key="new_user")
            submitted = st.form_submit_button("Speichern")
            if submitted:
                loaded_user.set_user_name(new_name)
                loaded_user.store_data()
                st.success(f"Änderungen für **{current_user}** wurden gespeichert!")
                st.rerun()
with tab4:
    st.header("Wartungsmanagement")
  