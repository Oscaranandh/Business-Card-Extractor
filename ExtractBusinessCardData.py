import time
import numpy as np
import pandas as pd
import pytesseract
import streamlit as st
from PIL import Image
import pytesseract
import argparse
import streamlit as st
import easyocr
import cv2
import numpy as np
import re
import sqlite3
from PIL import Image
from sqlite3 import Error

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('C:/Users/3arav/OneDrive/Desktop/oscar/mydatabases.db')
        return conn
    except Error as e:
        print(e)

    return conn

conn = create_connection()
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS BCD (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL,
designation TEXT,
email TEXT,
phone INTEGER,
address TEXT,
state TEXT,
city TEXT,
pincode INTEGER,
website TEXT,
company TEXT)''')

conn.commit()
conn.close()



def add_business_card(name, designation, email, phone, address, state, city, pincode, website, company):

    try:
        conn = create_connection()
        c = conn.cursor()
        # Insert the business card details into the business_cards table
        c.execute('''INSERT INTO BCD (name, designation, email, phone, address,city, state, pincode, website, company) 
                     VALUES (?, ?, ?, ?, ?,?, ?, ?, ?,?)''', (name, designation, email, phone, address, city, state, pincode, website, company))
        business_card_id = c.lastrowid

        # Insert the business card image into the business_card_images table
        #c.execute('''INSERT INTO BusinessCards(image, business_card_id)
         #            VALUES (?, ?)''', (image, business_card_id))
        conn.commit()
        conn.close()

        st.success("Business card details added successfully!")
        st.markdown('<h4 style="color: blue;">Viewing Details </h4>', unsafe_allow_html=True)
        vbutton = st.checkbox("View Business Card ")
        if vbutton is True:
            view_business_cards()
    except Exception as e:
        st.error("Error occurred while adding business card details: {}".format(str(e)))



def view_business_cards():
    conn = create_connection()
    c = conn.cursor()
    name_id = st.sidebar.text_input('Enter your name')
    c.execute(f'SELECT * FROM BCD WHERE name =?', (name_id,))
    rows = c.fetchall()
    count=0
    if rows:
        st.write("**Business Card Entries:**")
        for row in rows:
            st.write(" ID: {}".format(row[0]))
            st.write("  Name: {}".format(row[1]))
            st.write("  Title: {}".format(row[2]))
            st.write("  Email: {}".format(row[3]))
            st.write("  Phone: {}".format(row[4]))
            st.write("  Address: {}".format(row[5]))
            st.write("  City: {}".format(row[6]))
            st.write("  State: {}".format(row[7]))
            st.write("  Pincode: {}".format(row[8]))
            st.write("  Website: {}".format(row[9]))
            st.write("  Company: {}".format(row[10]))
            count+=1
            if count == 1:
                break
        conn.close()
        st.markdown('<h4 style="color: blue;">To update your details</h4>', unsafe_allow_html=True)
        ubutton = st.checkbox('Update Business Card')
        if ubutton is True:
            update_business_card(id,name,designation, email, phone, address,state,city,pincode,website, company)
        else:
            st.markdown('<h4 style="color: blue;">To delete your details</h4>', unsafe_allow_html=True)
            dbutton = st.checkbox('Delete Business Card')
            if dbutton is True:
               delete_business_card()

    else:
        st.warning("No business card entries found.")


def update_business_card(id,name,designation, email, phone, address,state,city,pincode,website, company):
    try:
        conn = create_connection()
        c = conn.cursor()
        call_id = st.sidebar.text_input('Enter ID')
        c.execute(f'SELECT * FROM BCD WHERE id =?', (call_id,))
        res = c.fetchone()
        if res:
            name = st.text_input('Name', res[1])
            designation = st.text_input('Designation', res[2])
            email = st.text_input('Email', res[3])
            phone = st.text_input('Phone', res[4])
            address = st.text_input('Address', res[5])
            state = st.text_input('State', res[6])
            city = st.text_input('City', res[7])
            pincode = st.text_input('Pincode', res[8])
            website = st.text_input('Website', res[9])
            company = st.text_input('Company', res[10])
        values = (name, designation, email, phone, address,state,city,pincode ,website,company,res[0])
        c.execute('''UPDATE BCD SET  name = ? ,designation = ?, email = ?, phone = ?, address = ? ,state =?,city =?,pincode =?,website =?,company =?
                     WHERE id = ?''', values)
        fini = st.checkbox("Finish")
        if fini is True:
            conn.commit()
            conn.close()
            st.success("Business card details updated successfully!")
            check = st.checkbox("View details after update")
            if check is True:
                conn = create_connection()
                c = conn.cursor()
                c.execute(f'SELECT * FROM BCD WHERE id =?', (call_id,))
                rows = c.fetchall()
                count = 0
                if rows:
                    st.write("**Business Card Entries:**")
                    for row in rows:
                        st.write(" ID: {}".format(row[0]))
                        st.write("  Name: {}".format(row[1]))
                        st.write("  Title: {}".format(row[2]))
                        st.write("  Email: {}".format(row[3]))
                        st.write("  Phone: {}".format(row[4]))
                        st.write("  Address: {}".format(row[5]))
                        st.write("  City: {}".format(row[7]))
                        st.write("  State: {}".format(row[6]))
                        st.write("  Pincode: {}".format(row[8]))
                        st.write("  Website: {}".format(row[9]))
                        st.write("  Company: {}".format(row[10]))
                        count += 1
                        if count == 1:
                            break

    except Exception as e:
        conn.rollback()
        conn.close()
        st.error("Error occurred while updating business card details: {}".format(str(e)))

def delete_business_card(id):
    try:
        conn = create_connection()
        c = conn.cursor()
        c.execute('''DELETE FROM BCD WHERE id = ?''', (id,))
        conn.commit()
        st.success("Business card details deleted successfully!")
    except Exception as e:
        st.error("Error occurred while deleting business card details: {}".format(str(e)))



st.set_page_config(page_title = 'BUSINESS CARD SCANNER')

reader = easyocr.Reader(['en'])


def prepro_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    return gray

st.markdown("""
            <div style='background-color: #9b59b6; padding: 10px; border-radius: 5px;'>
            <h1 style='color: #2ecc71; text-align: center;'>BUSINESS CARD SCANNER</h1>
            </div>
            """, unsafe_allow_html=True)

img = Image.open(r'D:\Oscar\Self Html\bceimage.jpg')
st.image(img)

st.markdown('<h2 style="color: blue;">Introduction</h2>', unsafe_allow_html=True)

st.write("Welcome to our Business Card Scanner app! Our app is designed to help you easily and efficiently manage your business card information. With just a few clicks, you can extract the relevant information from your business cards and store it in a database for later use.")

st.write("Our app uses state-of-the-art technology to extract information from business card images. Simply upload an image of your business card and let our app do the rest. Our app will extract the name, phone number, email address, and any other relevant information from the image and display it in a clean and organized manner.")
st.write("Once the information has been extracted, you can easily add it to a database with the click of a button. This will allow you to access and manage your business card information from anywhere, at any time.Whether you're a busy professional who wants to streamline their workflow, or a small business owner who needs to manage a large number of business cards, our app is the perfect solution. So why wait? Try our Business Card Scanner app today and start managing your business card information with ease!")

st.markdown('<h3 style="color: blue;">Steps for extracting</h3>', unsafe_allow_html=True)

st.markdown('<ul style="color:green;">'
            '<li> 1. Upload the image in given format</li>'
            '<li> 2. Select the button to Add details in SQL</li>'
            '<li> 3. Select option to View,Update and Delete for further process</li>'
            '</ul>', unsafe_allow_html=True)

st.markdown('<h4 style="color: blue;">Upload Your Image here</h4>', unsafe_allow_html=True)

# Create a file uploader to allow users to upload an image
uploaded_file = st.file_uploader("Only Images", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    st.image(uploaded_file, caption='Uploaded business card', use_column_width=True)
    st.success('Image added successfully ')
else:
    st.error('Select a mentioned file type')
if uploaded_file is not None:

    image = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8),1)
    gray = prepro_image(image)


    result = reader.readtext(gray)



    # Extract the fields from the text using regular expressions

    name_regex = r"^[A-Z]*(\s[A-Z][a-z]*)*$"
    designation_regex = r'([A-Z][a-z]+)( \b(?:MANAGER|CEO|FOUNDER|Executive|leader|Manager))'
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    phone_regex = r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]'
    address_regex = r'\d+ [\w-]+ [Avenue|Street|Road|Lane|Blvd|Dr|Pl|Ct|Trl|Pkwy|Way]+'
    city_regex = r'\b(?:Tirupur|HYDERABAD|Salem|Erode|Chennai)'
    state_regex = r"\b(?:Andhra Pradesh|Arunachal Pradesh|Assam|Bihar|Chhattisgarh|Goa|Gujarat|Haryana|Himachal Pradesh|Jharkhand|Karnataka|Kerala|Madhya Pradesh|Maharashtra|Manipur|Meghalaya|Mizoram|Nagaland|Odisha|Punjab|Rajasthan|Sikkim|TamilNadu|Telangana|Tripura|Uttar Pradesh|Uttarakhand|West Bengal)\b"
    pincode_regex = r'[1-9][0-9]{5}'
    website_regex = r'www\.(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
    company_regex = r'([A-Z][a-z]+)( \b(?:digitals|INSURANCE|AIRLINES|Restaurant|Electricals))'
    # Extract the fields from the text using regular expressions
    name = None
    designation = None
    email = None
    phone = None
    address = None
    city = None
    state = None
    pincode = None
    website = None
    company = None

    for r in result:
        if not name:
            match = re.search(name_regex, r[1])
            if match :
                name = match.group(0)

        if not designation :
            match = re.search(designation_regex, r[1])
            if match:
                designation = match.group(0)

        if not email:
            match = re.search(email_regex, r[1])
            if match:
                email = match.group(0)

        if not phone:
            match = re.search(phone_regex, r[1])
            if match:
                phone = match.group(0)

        if not address:
            match = re.search(address_regex, r[1])
            if match:
                address = match.group(0)

        if not city :
            match = re.search(city_regex, r[1])
            if match and match != designation:
                city = match.group(0)

        if not state:
            match = re.search(state_regex, r[1])
            if match :
                state = match.group(0)

        if not pincode:
            match = re.search(pincode_regex, r[1])
            if match:
                pincode = match.group(0)

        if not website:
            match = re.search(website_regex, r[1])
            if match:
                website = match.group(0)

        if not company:
            match = re.search(company_regex, r[1])
            if match:
                company = match.group(0)

    st.markdown('<h4 style="color: blue;">Select button to Add Details</h4>', unsafe_allow_html=True)
    ad = st.checkbox("Add business card Details")
    if ad is True:
        add_business_card(name,designation,email,phone,address,state,city,pincode,website,company)
    else:
        st.warning("To save details add click add")


sel = st.selectbox("Other options",("Save","Delete"))
if sel == 'Save':
    cb = st.button("Click submit to save the process")
    if cb is True:
        conn.close()
        st.success("Saved Successfully")

else:

    d1button = st.checkbox('Delete Business Card')
    if d1button is True:
        card_id = st.text_input('Enter the ID of the business card to delete')
        delete_business_card(card_id)

st.write("Copyright © 2023. All rights reserved.")