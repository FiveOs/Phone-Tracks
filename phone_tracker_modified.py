import tkinter
import tkintermapview
import phonenumbers
import opencage

import os
key = os.getenv("OPENCAGE_API_KEY")
if not key:
    messagebox.showerror("Error", "API key not found. Please set the OPENCAGE_API_KEY environment variable.")

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

# main function
def getResult():
    num = number.get("1.0", END).strip().replace("-", "").replace(" ", "")
    # check if the number textbox is completed correctly
    try:
        num1 = phonenumbers.parse(num)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        messagebox.showerror("Error", "Number box is empty or the input is not numeric !!")

    # use geocoder to retrive the location
        try:
            location = geocoder.description_for_number(num1, "en")
    # use carrier to retrive the service provider
            service_provider = carrier.name_for_number(num1, "en")

    # OpenCageGeocode is used to retrive location details like longitude, latitude
    ocg = OpenCageGeocode(key)
    query = str(location)
    results = ocg.geocode(query)

    lat = results[0]['geometry']['lat']
    lng = results[0]['geometry']['lng']

    print(lat)

    # Define LabelFrame to show the map on my app
    my_label = LabelFrame(root)
    my_label.pack(pady=20)

    # tkintermapview to fullfield my label with exact location of phone using lat and lng
    map_widget = tkintermapview.TkinterMapView(my_label, width=450, height=450, corner_radius=0)
    map_widget.set_position(lat, lng)
    # set_marker to set the marker on my map to see the location
    map_widget.set_marker(lat, lng, text = "Phone Location")
    # set_zoom to set the zoom on my map to actually see something
    map_widget.set_zoom(10)
    map_widget.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
    map_widget.pack()

    # convert the coordinates to address info to be able to analyse the informations
    adr = tkintermapview.convert_coordinates_to_address(lat, lng)

    # parse the data to screen
    result.insert(END, "The country of this number is: " + location)
    result.insert(END, "\nThe sim card of this number is: " + service_provider)

    result.insert(END, "\nLatitude is: " + str(lat))
    result.insert(END, "\nLongitude is: " + str(lng))

    result.insert(END,"\nStreet Address is: " + adr.street)
    result.insert(END,"\nCity Address is: " + adr.city)
    result.insert(END,"\nPostal Code is: " + adr.postal)

number = Text(height=1)
number.pack()

# define a style for my button
style = Style()
style.configure("TButton", font= ('calibri', 20, 'bold'), borderwidth='4')
style.map('TButton', foreground = [('active', '!disabled', 'green')],
                     background = [('active', 'black')])

button = Button(text="Search", command=getResult)
button.pack(pady = 10, padx=100)

result = Text(height=7)
result.pack()

root.mainloop()