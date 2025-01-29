import streamlit as st
from devices import Device
from users import User
from reservation import Reservation
import queries as qr
from maintenance import Maintenance
from datetime import datetime

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
                new= Reservation(selected_user,selected_device,reservation_start,reservation_end)
                new.store_data()
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
    st.header("Gerätemanagement")

    # Alle Geräte und Benutzer aus der Datenbank laden
    devices_in_db = qr.find_devices()
    user_in_db = qr.find_users()
    #devices_in_db= Device.find_all()
    #user_in_db= User.find_all()
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
    #user_in_db = qr.find_users()
    st.header("Nutzer - Verwaltung")
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
        current_user= st.selectbox("User",user_in_db)
        if current_user in user_in_db:
            loaded_user = User.find_by_attribute("id", current_user)
    
        st.write("Geben Sie den neuen Username in das Feld ein:")
        with st.form("User-Einstellungen"):
            new_name= st.text_input(f"Aktueller Username: {loaded_user.name}", key="new_user")
            submitted = st.form_submit_button("Speichern")
            if submitted:
                loaded_user.set_user_name(new_name)
                loaded_user.store_data()
                st.success(f"Änderungen für **{current_user}** wurden gespeichert!")
                st.rerun()
with tab4:
    st.header("Wartungsmanagement")
    tab9, tab10, tab11 = st.tabs(["Nächste Wartungstermine", "Wartung anlegen", "Wartungsplan verändern"])
    devices_in_db = qr.find_devices()

    with tab9:
        for device in devices_in_db:
            loaded_maintenance = Maintenance.find_by_attribute("device_id", device, num_to_return=1)
            if loaded_maintenance:
                next_maintenance = loaded_maintenance[0].next_maintenance
                st.write(f"Gerät: {device}, Nächste Wartung: {next_maintenance.date()}")
            else:
                st.write(f"Gerät: {device}, Keine geplanten Wartungen")

        # Wartungskosten pro Quartal berechnen und anzeigen
        st.subheader("Wartungskosten pro Quartal")
        current_year = datetime.now().year
        quarterly_costs = {1: 0, 2: 0, 3: 0, 4: 0}

        all_maintenances = Maintenance.find_all()
        for maintenance in all_maintenances:
            next_maintenance_date = maintenance.next_maintenance
            if next_maintenance_date.year == current_year:
                quarter = (next_maintenance_date.month - 1) // 3 + 1
                quarterly_costs[quarter] += maintenance.__maintenance_cost

        for quarter, cost in quarterly_costs.items():
            st.write(f"Q{quarter} {current_year}: {cost} EUR")
  
    with tab10:
        with st.form("Wartung anlegen"):
            selected_device = st.selectbox("Wählen Sie ein Gerät:", devices_in_db)
            first_maintenance = st.date_input("Erstes Wartungsdatum:")
            maintenance_interval = st.number_input("Wartungsintervall (Tage):", min_value=1)
            maintenance_cost = st.number_input("Wartungskosten (EUR):", min_value=0.0)

            submitted = st.form_submit_button("Wartung anlegen")
            if submitted:
                new_maintenance = Maintenance(selected_device, first_maintenance, maintenance_interval, maintenance_cost)
                new_maintenance.store_data()
                st.success(f"Wartung für **{selected_device}** wurde erfolgreich angelegt!")

    with tab11:
        with st.form("Wartung aktualisieren"):
            selected_device = st.selectbox("Wählen Sie ein Gerät:", devices_in_db)
            loaded_maintenance = Maintenance.find_by_attribute("device_id", selected_device, num_to_return=1)
    
            if loaded_maintenance:
                maintenance = loaded_maintenance[0]
                st.write(f"Aktuelle nächste Wartung: {maintenance.next_maintenance.date()}")
    
                new_first_maintenance = st.date_input("Neues erstes Wartungsdatum:", value=maintenance.first_maintenance)
                new_maintenance_interval = st.number_input("Neues Wartungsintervall (Tage):", min_value=1, value=maintenance.__maintenance_interval)
                new_maintenance_cost = st.number_input("Neue Wartungskosten (EUR):", min_value=0.0, value=maintenance.__maintenance_cost)
    
                submitted = st.form_submit_button("Wartung aktualisieren")
                if submitted:
                    maintenance.first_maintenance = new_first_maintenance
                    maintenance.__maintenance_interval = new_maintenance_interval
                    maintenance.__maintenance_cost = new_maintenance_cost
                    maintenance.update_maintenance()
                    st.success(f"Wartung für **{selected_device}** wurde erfolgreich aktualisiert!")
            else:
                st.write("Keine geplanten Wartungen für das ausgewählte Gerät.")