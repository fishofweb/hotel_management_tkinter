from tkinter import *
import tkinter.messagebox as tmsg
import sqlite3
import datetime
tk = Tk()

tk.title("Hotel Management")
tk.geometry("1000x1000")
table = datetime.datetime.now()
table_name=table.strftime("%x")

db_name= str(table_name)+".db"
conn = sqlite3.connect('hotel.db')
  

#
c = conn.cursor()
sql_query = "CREATE TABLE IF NOT EXISTS '{}' (name TEXT, nicard TEXT,checkin TEXT, checkout TEXT, stay TEXT, rooms_booked TEXT, allotted TEXT, discount TEXT, advance TEXT, people TEXT, roomtype TEXT, amenities TEXT, remaining TEXT)".format("checkin")
c.execute(sql_query)
sql_query = "CREATE TABLE IF NOT EXISTS '{}' (name TEXT, nicard TEXT,checkin TEXT, checkout TEXT, stay TEXT, rooms_booked TEXT, allotted TEXT, discount TEXT, advance TEXT, people TEXT, roomtype TEXT, amenities TEXT, remaining TEXT, notes TEXT)".format("checkout")
c.execute(sql_query)
conn.commit()
conn.close()

def info_():
    card = id_customer.get()
    print(card)
    if card:
        conn = sqlite3.connect('hotel.db')
        c = conn.cursor()
        c.execute("SELECT * from '{}' where nicard = '{}'".format("checkin", card))
        records = c.fetchall()
        print("Total rows are:  ", len(records))
        print(records[0][0])
        
        conn.commit()
        
        Label(f3, text="Name", bg= "black", fg = "white", padx=20).pack()
        Label(f3, text=records[0][0]).pack()

        Label(f3, text="ID CARD", bg= "black", fg = "white", padx=20).pack()
        Label(f3, text=records[0][1]).pack()
        Label(f3, text="checkin", bg= "black", fg = "white", padx=20).pack()
        Label(f3, text=records[0][2]).pack()
        Label(f3, text="checkout", bg= "black", fg = "white", padx=20).pack()
        Label(f3, text=records[0][3]).pack()
        Label(f3, text="discount", bg= "black", fg = "white", padx=20).pack()
        Label(f3, text=records[0][7]).pack()
        Label(f3, text="Room", bg= "black", fg = "white", padx=20).pack()
        Label(f3, text=records[0][6]).pack()
        Label(f3, text="Amenities", bg= "black", fg = "white", padx=20).pack()
        Label(f3, text=records[0][11]).pack()



def checkout():
    
    name_chkout = name_.get()
    id_chkout = id_.get()
    remaining_chkout = remaining.get()
    checkout_notes = notes.get("1.0","end")
   
    
    
    if id_chkout:
        conn = sqlite3.connect('hotel.db')
        c = conn.cursor()
        c.execute("SELECT * from '{}' where nicard = '{}'".format("checkin", id_chkout))
        records = c.fetchall()
        print("Total rows are:  ", len(records))
        print(records[0][0])
        c.execute('INSERT INTO "{}" (name, nicard,checkin, checkout, stay, rooms_booked, allotted, discount,advance, people, roomtype, amenities, remaining, notes) VALUES (?,? ,?, ?, ?,? ,?, ?, ?,?,?,?,?,?)'.format("checkout"), (str(records[0][0]), str(records[0][1]),str(checkin_date_), str(table_name[:2]), str(records[0][2]), str(records[0][3]), str(records[0][4]), str(records[0][5]), str(records[0][6]), str(records[0][7]), str(records[0][8]), str(records[0][9]), str(records[0][10]),str(checkout_notes),))
        c.execute('DELETE from "{}" where nicard = "{}"'.format(table_name, id_chkout))
        conn.commit()
        print(name_chkout, " deleted")
 

def initial_process():
    # try:
    name_client = name_cus.get()
    print(name_client)
    id_num = id_card.get()
    print(id_num)
    stay_ = stay.get()
    room_number = rooms_.get()
    print(room_number)
    room_alloted = room_num.get() 
    advance_ = advance.get()
    discount_ = discount.get()
    people_ = people.get()
    amenities_availed = ""
    room_type = ""
    deluxe_ = deluxe.get()
    ordinary_ = ordinary.get()
    queen_ = queen.get()
    king_ = king.get()

    
    laundry_ = laundry.get()
    transport_ = transport.get()

    per_night_deluxe = 4000
    per_night_ordinary = 3000
    per_night_queen = 5000
    per_night_king = 6000
    in_dt = checkin_.get()
    out_dt = checkout_.get()
    checkin_list = in_dt.split()
    print(checkin_list)
    checkout_list = out_dt.split()
    print(checkout_list)
    laundry_price = 2000
    transport_price = 4000
    total_rent = 0
    total_bill = 0
    amenities = 0
    if(king_):
        total_room_rent = int(per_night_king) * int(stay_) 
        total_rent += int(total_room_rent)
        
        total_bill += int(total_room_rent) 

        
        room_type +="King,"

    if(queen_):
        total_room_rent = int(per_night_queen) * int(stay_) 
        
        total_rent += int(total_room_rent)            
        total_bill += int(total_room_rent) 

        room_type += "Queen,"
        

    if(deluxe_):
        total_room_rent = int(per_night_deluxe) * int(stay_) 
        
        
        total_bill += int(total_room_rent) 
        total_rent += int(total_room_rent)
        room_type += "deluxe,"

    if(ordinary_):
        total_room_rent = int(per_night_ordinary) * int(stay_) 
        
        total_rent += int(total_room_rent)            
        total_bill += int(total_room_rent)  

        room_type += "ordinary,"

    if laundry_:
        amenities += (int(laundry_price) * int(stay_))
        amenities_availed += "Laundry,"
    if(transport_):
        amenities += (int(transport_price) * int(stay_))
        amenities_availed += "Transport,"
    total_bill_actually = 0
    total_bill_actually += int(total_bill) + int(amenities)
    if(discount_):
        total_bill = int(total_bill) - int(discount_)
    
    if(advance_):
        total_bill = int(total_bill) - int(advance_)
    total_bill += amenities
    tmsg.showinfo("Total Bill", f"Room Rent: {total_rent}\n Amenities: {amenities}\n Nigths: {stay_} \n Rooms: {room_number} \n \n\nTotal Bill: {total_bill_actually} \n Advance: {advance_} \n Discount: {discount_} \n Total Bill Remaining: {total_bill}")

    
    
    conn = sqlite3.connect('hotel.db')

    c = conn.cursor()
    c.execute('INSERT INTO "{}" (name, nicard, checkin, checkout, stay, rooms_booked, allotted, discount,advance, people, roomtype, amenities, remaining) VALUES (?,? ,?, ?, ?,? ,?, ?, ?,?,?,?,?)'.format("checkin"), (str(name_client), str(id_num),str(in_dt), str(out_dt), str(stay_), str(room_number), str(room_alloted), str(discount_), str(advance_), str(people_), str(room_type), str(amenities_availed), str(total_bill),))
    conn.commit()
    print("checkin dateeeee", in_dt)

    
l1 = Label(tk, text="Hotel Management App", font="comicsansms 13 bold", padx =200)
l1.pack()

f1 = Frame(tk, borderwidth=6, height=6, bd=1,relief=RIDGE, padx=20)
f1.pack(side=LEFT)
Label(f1, text="CHECK-IN", bg= "black", fg = "white", padx=20).pack()
Label(f1, text="Name", padx=20).pack()
name_cus = Entry(f1, width=30)
name_cus.pack()

Label(f1, text="ID", padx=20).pack()
id_card = Entry(f1, width=30)
id_card.pack()

Label(f1, text="Room Number", padx=20).pack()
room_num = Entry(f1, width=30)
room_num.pack()

Label(f1, text="Checkin Date", padx=20).pack()
checkin_ = Entry(f1, width=30)
checkin_.pack()

Label(f1, text="Checkout Date", padx=20).pack()
checkout_ = Entry(f1, width=30)
checkout_.pack()

Label(f1, text="No. Of Nights", padx=20).pack()
stay = Entry(f1, width=30)
stay.pack()

Label(f1, text="No. Of Rooms", padx=20).pack()
rooms_ = Entry(f1, width=30)
rooms_.pack()

Label(f1, text="advance", padx=20).pack()
advance = Entry(f1, width=30)
advance.pack()

Label(f1, text="Discount", padx=20).pack()
discount = Entry(f1, width=30)
discount.pack()

Label(f1, text="Number of People", padx=20).pack()
people = Entry(f1, width=30)
people.pack()

Label(f1, text="Room",bg="black", fg="white", padx=20).pack()

deluxe = IntVar()
Checkbutton(f1, text="Deluxe", variable=deluxe).pack()
ordinary = IntVar()
Checkbutton(f1, text="Ordinary", variable=ordinary).pack()

queen = IntVar()
Checkbutton(f1, text="Queen", variable=queen).pack()
king = IntVar()
Checkbutton(f1, text="King", variable=king).pack()

Label(f1, text="Amenities", bg= "black", fg = "white", padx=20).pack()

laundry = IntVar()
Checkbutton(f1, text="Laundry", variable=laundry).pack()
transport = IntVar()
Checkbutton(f1, text="Transport", variable=transport).pack()

send = Button(f1, text = "DONE",padx=10, bg="Blue",fg="white", command= initial_process)
send.pack()
# /////////// checkout
f2 = Frame(tk, borderwidth=6, height=6, bd=1,relief=RIDGE, padx=20)
f2.pack(side=LEFT)
Label(f2, text="CHECK-OUT", bg= "black", fg = "white", padx=20).pack()
Label(f2, text="Name", padx=20).pack()

name_ = Entry(f2, width=30)
name_.pack()


Label(f2, text="ID", padx=20).pack()
id_ = Entry(f2, width=30)
id_.pack()

Label(f2, text="Checkin date", padx=20).pack()
checkin_date = Entry(f2, width=30)
checkin_date.pack()

Label(f2, text="Checkout date", padx=20).pack()
checkout_date = Entry(f2, width=30)
checkout_date.pack()

Label(f2, text="Remaining Bill Amount", padx=20).pack()
remaining = Entry(f2, width=30)
remaining.pack()

Label(f2, text="Any Notes", padx=20).pack()
notes = Text(f2, width=20, height= 20)
notes.pack()
send = Button(f2, text = "DONE",padx=10, bg="Blue",fg="white", command= checkout)
send.pack()

# /////////////// info
f3 = Frame(tk, borderwidth=6, height=6, bd=1,relief=RIDGE)
f3.pack(side=LEFT)
Label(f3, text="CUSTOMER-INFO", bg= "black", fg = "white", padx=20).pack()

Label(f3, text="ID", padx=20).pack()
id_customer = Entry(f3, width=30)
id_customer.pack()

Label(f3, text="Room Number", padx=20).pack()
room_no = Entry(f3, width=30)
room_no.pack()
find_ = Button(f3, text = "FIND",padx=10,pady=5, bg="Blue",fg="white", command= info_)
find_.pack()
# ///////////////////////////////////// update

f4 = Frame(tk, borderwidth=6, height=6, bd=1,relief=RIDGE)
f4.pack(side=LEFT)
Label(f4, text="CUSTOMER-UPDATE", bg= "black", fg = "white", padx=20).pack()

OPTIONS = [
"Room",
"amenities",
"payment",
"stay"
] 



variable = StringVar(f4)
variable.set(OPTIONS[0]) 
Label(f4, text="Please select what would you want to update").pack()
w = OptionMenu(f4, variable, *OPTIONS)
w.pack()



def choice():
    choice_item= variable.get()
    if choice_item == "amenities":
        nic_label= Label(f4, text="Enter nic number:")
        nic_label.pack()
        nic_number = Entry(f4, width=30)
        nic_number.pack()

        def amenities_change():
            
            conn = sqlite3.connect('hotel.db')
            c = conn.cursor()
            c.execute("SELECT * from '{}' where nicard = '{}'".format("checkin", nic_number.get()))
            records = c.fetchall()
            amenity_list=[]
            print(type(records[0][11]))
            amenity_list.append(records[0][11])
            print(amenity_list)
            amenity_list=amenity_list[0].split(",")
            current_amenities_label=Label(f4, text="current amenities: "+ records[0][11])
            current_amenities_label.pack()
            
            

            def confirm_amenity():
                conn = sqlite3.connect('hotel.db')
                
                c = conn.cursor()
                
                current_remaining = 0
                c.execute("SELECT * from '{}' where nicard = '{}'".format("checkin", nic_number.get()))
                records = c.fetchall()
                balance= int(records[0][12])
                print("current remaining", current_remaining)
                current_amenities = records[0][11]
                print("current amenities", current_amenities)
                sql_update_query = "Update '{}' set amenities = ? where nicard = ?".format("checkin")
                amn = ""
                if laundry1.get():
                    amn += "Laundry,"
                    if current_amenities == 'Transport,' or current_amenities == "":
                        current_remaining += 2000 
                    
                    if current_amenities == 'Laundry,Transport,':
                        current_remaining += 0 
                    
                if transport1.get():
                    amn += "Transport,"      
                    if current_amenities == 'Laundry,' or current_amenities == "":
                        current_remaining += 4000
                    if current_amenities == 'Laundry,Transport,':
                        current_remaining += 0
                data = (amn, nic_number.get())
                c.execute(sql_update_query, data)
                conn.commit()


                conn = sqlite3.connect('hotel.db')
                c = conn.cursor()
                sql_update_query = "Update '{}' set remaining = ? where nicard = ?".format("checkin")
                
                
                print(balance)
                print(current_remaining)
                print("after amenities", balance + current_remaining)
                balance_update = balance + current_remaining
                data = (balance_update, nic_number.get())
                c.execute(sql_update_query, data)
                conn.commit()
               

                l.destroy()
                confirm_amenities_button.destroy()
                t.destroy()
                amenities_button.destroy()
                nic_label.destroy()
                nic_number.destroy()
                current_amenities_label.destroy()
                tmsg.showinfo("Amenity", f"Amenity record is updated")
                


            
            laundry1 = IntVar()
            transport1 = IntVar()
                
                
            l=Checkbutton(f4, text="Laundry",onvalue = 1, offvalue = 0, variable=laundry1)
            l.pack() 
            t=Checkbutton(f4, text="Transport",onvalue = 1, offvalue = 0, variable=transport1)
            t.pack()
            
            confirm_amenities_button = Button(f4, text="confirm",command=confirm_amenity, bg="red", fg="white")
            confirm_amenities_button.pack()

        amenities_button = Button(f4, text="OK",command=amenities_change, bg="red", fg="white")
        amenities_button.pack()

        
    if choice_item == "Room":
        nic_label= Label(f4, text="Enter nic number:")
        nic_label.pack()
        nic_number = Entry(f4, width=30)
        nic_number.pack()
        def shifting_room():
            
            conn = sqlite3.connect('hotel.db')
            c = conn.cursor()
            c.execute("SELECT * from '{}' where nicard = '{}'".format("checkin", nic_number.get()))
            records = c.fetchall()
            print(records[0][6])
            current_room_label=Label(f4, text="current room: "+ records[0][6])
            current_room_label.pack()
            shift_to_label=Label(f4, text="shift to ")
            shift_to_label.pack()
            shift_to_room = Entry(f4, width=30)
            shift_to_room.pack()

            def shift_to():

                c.execute("UPDATE '{}' SET allotted='{}' WHERE nicard ='{}'".format("checkin", shift_to_room.get(), nic_number.get()))
                conn.commit()
                confirm_shift_label=Label(f4, text="Guest is shifted to "+ shift_to_room.get())
                confirm_shift_label.pack()
                def shift_confirm():
                    shift_to_label.destroy()
                    current_room_label.destroy()
                    nic_label.destroy()
                    confirm_shift_label.destroy()
                    shift_to_room.destroy()
                    nic_number.destroy()
                    shift_confirm_button.destroy()
                    shift_button.destroy()
                    nic_button.destroy()
                shift_confirm_button = Button(f4, text="DONE",command=shift_confirm, bg="red", fg="white")
                shift_confirm_button.pack()
            
            shift_button = Button(f4, text="OK",command=shift_to, bg="red", fg="white")
            shift_button.pack()

            conn.commit()


        nic_button = Button(f4, text="OK",command=shifting_room, bg="red", fg="white")
        nic_button.pack()
        

    if choice_item == "payment":
        nic_label= Label(f4, text="Enter nic number:")
        nic_label.pack()
        nic_number = Entry(f4, width=30)
        nic_number.pack()    
        print("payment")
        def advance_bill_payment():
            conn = sqlite3.connect('hotel.db')
            c = conn.cursor()
            c.execute("SELECT * from '{}' where nicard = '{}'".format("checkin", nic_number.get()))
            records = c.fetchall()
            print(records[0][12], " remaining")
            current_bill = records[0][12]
            print(current_bill)
            current_bill_label=Label(f4, text="current bill: "+ records[0][12])
            current_bill_label.pack()
            advance_payment_label=Label(f4, text="Enter Advance Payment ")
            advance_payment_label.pack()
            advance_payment = Entry(f4, width=30)
            advance_payment.pack()

            def update_bill():
                   
                    bill_updated = int(current_bill) - int(advance_payment.get())
                    c.execute("UPDATE '{}' SET remaining='{}' WHERE nicard ='{}'".format("checkin", bill_updated, nic_number.get()))
                    conn.commit()
                    advance_payment.destroy()
                    update_button.destroy()
                    current_bill_label.destroy()
                    
                    nic_button.destroy()
                    nic_number.destroy()
                    nic_label.destroy()
                    
                    advance_payment_label.destroy()
                    tmsg.showinfo("Advance Payment", f"Remaining Bill Updated")

            update_button = Button(f4, text="Update",command=update_bill, bg="red", fg="white")
            update_button.pack()

        nic_button = Button(f4, text="OK",command=advance_bill_payment, bg="red", fg="white")
        nic_button.pack()

    if choice_item == "stay":
        nic_label= Label(f4, text="Enter nic number:")
        nic_label.pack()
        nic_number = Entry(f4, width=30)
        nic_number.pack()    
        print("stay")
        def extend_stay():
            conn = sqlite3.connect('hotel.db')
            c = conn.cursor()
            c.execute("SELECT * from '{}' where nicard = '{}'".format("checkin", nic_number.get()))
            records = c.fetchall()
            print(records[0][3], " checkout")
            checkout_current = records[0][3]
            print(checkout_current)
            checkout_current_label=Label(f4, text="current checkout: "+ records[0][3])
            checkout_current_label.pack()
            change_checkout_label=Label(f4, text="Enter New Checkout Date: ")
            change_checkout_label.pack()
            new_checkout = Entry(f4, width=30)
            new_checkout.pack()
            options_ = [
                "jan",
                "feb",
                "mar",
                "apr",
                "may",
                "jun",
                "jul",
                "aug",
                "sep",
                "oct",
                "nov",
                "dec"
            ]

            clicked = StringVar()
            clicked.set(options_[0])

            month_checkout_label=Label(f4, text="Select Month: ")
            month_checkout_label.pack()
            menu_month = OptionMenu(f4,clicked, *options_)
            menu_month.pack() 

            year_checkout_label=Label(f4, text="Enter Year: ")
            year_checkout_label.pack()
            new_checkout_year = Entry(f4, width=30)
            new_checkout_year.pack()

            total_nights_label=Label(f4, text="Total Nights ")
            total_nights_label.pack()
            total_nights = Entry(f4, width=30)
            total_nights.pack()

            def update_stay():
                    update_new_checkout= new_checkout.get()
                    month_= clicked.get()
                    print(month_)
                    year_ = new_checkout_year.get()
                    nigths = total_nights.get()
                    c.execute("UPDATE '{}' SET checkout='{}' WHERE nicard ='{}'".format("checkin", update_new_checkout+"-"+month_+"-"+year_, nic_number.get()))
                    conn.commit()
                    c.execute("UPDATE '{}' SET stay='{}' WHERE nicard ='{}'".format("checkin", nigths, nic_number.get()))
                    conn.commit()
                    total_nights.destroy()
                    total_nights_label.destroy()
                    change_checkout_label.destroy()
                    checkout_current_label.destroy()
                    update_checkout.destroy()
                    month_checkout_label.destroy()
                    year_checkout_label.destroy()
                    new_checkout_year.destroy()
                    menu_month.destroy()
                   
                    nic_button.destroy()
                    nic_number.destroy()
                    nic_label.destroy()
                   
                    new_checkout.destroy()
                    tmsg.showinfo("Checkout", f"checkout updated ")

                    
            update_checkout = Button(f4, text="OK",command=update_stay, bg="red", fg="white")
            update_checkout.pack()
        nic_button = Button(f4, text="OK",command=extend_stay, bg="red", fg="white")
        nic_button.pack()

button = Button(f4, text="OK", command=choice, bg="blue", fg="white")
button.pack()



tk.mainloop()
