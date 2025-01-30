import streamlit as st
from devices import Device
from users import User
from reservation import Reservation
import queries as qr
from datetime import datetime
import time

st.title("Geräteverwaltung MCI")

tab1, tab2, tab3, tab4 = st.tabs(["Reservierungen", "Geräte", "Nutzer", "Wartungen"])
#device_list=["Test1","Gerät_2"]

with tab1:
    st.header("Reservierungssystem")
    resTab1, resTab2= st.tabs(["Reservierung anlegen", "Reservierungen anzeigen"])

    devices_in_db = qr.find_devices()
    user_in_db = qr.find_users()
    reservation_in_db = Reservation.find_all()
    with resTab1:
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
                    if new.store_data():
                        st.error("Reservierung schon vorhanden!")
                    else:
                        st.success(f"Reservierung für **{selected_device}** angelegt: \n\n"
                            f"Reservierender Nutzer: {selected_user}\n"
                            f"Startdatum: {reservation_start}\n"
                            f"Enddatum: {reservation_end}")
                else : 
                    st.write("Datum falsche angelegt!")
                    
    with resTab2:
        selected_reservation = st.selectbox("Wählen Sie ein Gerät:", devices_in_db, key= "Reservation")
        loaded_reservations = Reservation.find_by_attribute("device_id", selected_reservation, num_to_return=-1)
        if not loaded_reservations: 
            st.write("Reservation not found.")
        else:
            st.write(f"{loaded_reservations}")

with tab2:
    # Überschrift
    st.header("Gerätemanagement")

    # Alle Geräte und Benutzer aus der Datenbank laden
    devices_in_db = qr.find_devices()
    user_in_db = qr.find_users()
    tab5, tab6 = st.tabs(["Neues Gerät anlegen","Geräte Einstellungen ändern"])


    with tab5:
        new_device= st.text_input("Neues Gerät anlegen", key="add_new_device")
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

                #if loaded_device:
                 #   st.write(f"Ausgewähltes Gerät: **{loaded_device.device_name}**")

                with st.form("Geräte-Einstellungen"):
                    new_manager= st.selectbox('User ändern', user_in_db)
                    submitted = st.form_submit_button("Speichern")
                    if submitted:
                        loaded_device.set_managed_by_user_id(new_manager)
                        loaded_device.store_data()
                        st.success(f"Änderungen für **{loaded_device.device_name}** wurden gespeichert!")
                        st.rerun()
                delete = st.button("Löschen", key = "delete")
                if delete:
                    Device.delete(loaded_device)

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
        delete_user = st.button("Löschen", key = "delete_user")
        if delete_user:
             User.delete(loaded_user)

with tab4:
    st.header("Wartungsmanagement")
    tab9, tab10 = st.tabs(["Nächste Wartungstermine", "Wartung anlegen oder verändern"])

    with tab9:
        # Datenbankabfrage direkt im Tab durchführen
        devices_in_db = qr.find_devices()
        for device in devices_in_db:
            loaded_device = Device.find_by_attribute("device_name", device)
            if loaded_device and loaded_device.next_maintenance:
                next_maintenance = loaded_device.next_maintenance
                st.markdown(f"**{device}**, Nächste Wartung: {next_maintenance.date()}")

        # Wartungskosten pro Quartal berechnen und anzeigen
        st.subheader("Wartungskosten pro Quartal")
        current_year = datetime.now().year
        quarterly_costs = {1: 0, 2: 0, 3: 0, 4: 0}

        all_devices = Device.find_all()
        for device in all_devices:
            if device.next_maintenance and device.next_maintenance.year == current_year:
                quarter = (device.next_maintenance.month - 1) // 3 + 1
                quarterly_costs[quarter] += device.maintenance_cost

        for quarter, cost in quarterly_costs.items():
            st.write(f"Q{quarter} {current_year}: {cost} EUR")

    with tab10:
        selected_device = st.selectbox("Wählen Sie ein Gerät:", devices_in_db, key="device_selection_tab10")
        loaded_device = Device.find_by_attribute("device_name", selected_device)
    
        if loaded_device:
            # Anzeige der aktuellen Wartungsinformationen oder eine Nachricht, wenn keine Informationen vorhanden sind
            st.write("**Aktuelle Wartungsinformationen:**")
            if loaded_device.first_maintenance or loaded_device.maintenance_interval or loaded_device.maintenance_cost or loaded_device.next_maintenance:
                if loaded_device.first_maintenance:
                    st.write(f"Erstes Wartungsdatum: {loaded_device.first_maintenance}")
                if loaded_device.maintenance_interval:
                    st.write(f"Wartungsintervall (Tage): {loaded_device.maintenance_interval}")
                if loaded_device.maintenance_cost:
                    st.write(f"Wartungskosten (EUR): {loaded_device.maintenance_cost}")
                if loaded_device.next_maintenance:
                    st.write(f"Nächste Wartung: {loaded_device.next_maintenance.date()}")
            else:
                st.write("Keine Wartungsinformationen vorhanden.")
    
        with st.form("Wartung verwalten"):
            # Eingabefelder für die Wartungsinformationen
            first_maintenance = st.date_input(
                "Erstes Wartungsdatum:", 
                value=loaded_device.first_maintenance if loaded_device and loaded_device.first_maintenance else datetime.now()
            )
            maintenance_interval = st.number_input(
                "Wartungsintervall (Tage):", 
                min_value=1, 
                value=loaded_device.maintenance_interval if loaded_device and loaded_device.maintenance_interval else 1
            )
            maintenance_cost = st.number_input(
                "Wartungskosten (EUR):", 
                min_value=0.0, 
                value=loaded_device.maintenance_cost if loaded_device and loaded_device.maintenance_cost else 0.0
            )
    
            submitted = st.form_submit_button("Speichern")
            if submitted:
                device = Device.find_by_attribute("device_name", selected_device)
                device.first_maintenance = first_maintenance
                device.maintenance_interval = maintenance_interval
                device.maintenance_cost = maintenance_cost
                device.next_maintenance = device.calculate_next_maintenance()
                device.store_data()
                st.success(f"Wartung für **{selected_device}** wurde erfolgreich gespeichert!")