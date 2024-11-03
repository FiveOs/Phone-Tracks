
import tkinter
import tkintermapview
import phonenumbers
import opencage
import os

from key import key
from phonenumbers import geocoder
from phonenumbers import carrier

from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *

from opencage.geocoder import OpenCageGeocode

# tkinter dimensions
root = tkinter.Tk()
root.geometry("500x500")

# app label
label1 = Label(text="Phone Number Tracker")
label1.pack()

# Function to validate and format phone numbers
def validate_and_parse_number(num_str):
    try:
        # Ensure the number is in the correct format for Malaysia
        num = phonenumbers.parse(num_str, "MY")
        if not phonenumbers.is_valid_number(num):
            raise phonenumbers.NumberParseException(0, "Invalid number format")
        return num
    except phonenumbers.NumberParseException as e:
        messagebox.showerror("Error", f"Invalid phone number format: {str(e)}")
        return None

# Function to retrieve location details
def get_location_details(num):
    try:
        location = geocoder.description_for_number(num, "en")
        service_provider = carrier.name_for_number(num, "en")
        
        ocg = OpenCageGeocode(key)
        query = str(location)
        results = ocg.geocode(query)

        if not results:
            messagebox.showerror("Error", "Could not retrieve location details")
            return None, None, None, None

        lat = results[0]['geometry']['lat']
        lng = results[0]['geometry']['lng']
        return location, service_provider, lat, lng
    except Exception as e:
        messagebox.showerror("Error", f"Error while fetching location details: {str(e)}")
        return None, None, None, None

# Main function to display results
def getResult():
    num_str = number.get("1.0", END).strip()
    num = validate_and_parse_number(num_str)

    if num:
        location, service_provider, lat, lng = get_location_details(num)
        
        if location and service_provider:
            # Display results on the map
            my_label = LabelFrame(root)
            my_label.pack(pady=20)

            map_widget = tkintermapview.TkinterMapView(my_label, width=450, height=450, corner_radius=0)
            map_widget.set_position(lat, lng)
            map_widget.set_marker(lat, lng, text="Phone Location")
            map_widget.set_zoom(10)
            map_widget.pack()

            # Convert coordinates to address
            adr = tkintermapview.convert_coordinates_to_address(lat, lng)

            # Parse data to screen
            result.delete(1.0, END)  # Clear previous results
            result.insert(END, f"The country of this number is: {location}\n")
            result.insert(END, f"The sim card of this number is: {service_provider}\n")
            result.insert(END, f"Latitude is: {lat}\n")
            result.insert(END, f"Longitude is: {lng}\n")
            result.insert(END, f"Street Address is: {adr.street}\n")
            result.insert(END, f"City Address is: {adr.city}\n")
            result.insert(END, f"Postal Code is: {adr.postal}\n")

number = Text(height=1)
number.pack()

# Define a style for the button
style = Style()
style.configure("TButton", font=('calibri', 20, 'bold'), borderwidth='4')
style.map('TButton', foreground=[('active', '!disabled', 'green')],
                     background=[('active', 'black')])

button = Button(text="Search", command=getResult)
button.pack(pady=10, padx=100)

result = Text(height=7)
result.pack()

root.mainloop()
