'''import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Combobox
import mysql.connector

# Database connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="fazain"
)
cursor = conn.cursor()
print("connected to database")

from TRAM import train1

root = tk.Tk()
root.config(bg="#ffffff")
root.title("KRAIL")
root.geometry("2000x2500")
label = tk.Label(root, text="KRAIL ONLINE PLATFORM", fg="#1e1e1e", font=("classic", 20), bg="#ffffff")
label.pack()
root.resizable(True, True)

def show1():
    # Pack management for layout safety
    labelname = tk.Label(root, text="ENTER YOUR NAME ", fg="#1e1e1e", font=("Arial", 14), bg="#ffffff")
    labelname.place(x=650, y=100)

    entryNAME = tk.Entry(root, bd=2, font=("Arial", 12))
    entryNAME.place(x=650, y=150, width=280, height=30)
    
    radio_var = tk.StringVar(value="M")

    r1 = tk.Radiobutton(root, text="MALE", variable=radio_var, value="M", bg="#ffffff")
    r2 = tk.Radiobutton(root, text="FEMALE", variable=radio_var, value="F", bg="#ffffff")

    r1.place(x=700, y=180, width=100, height=28)
    r2.place(x=800, y=180, width=100, height=28)

    label3 = tk.Label(root, text="TRAINS", font=("ARIAL", 16), fg="#1e1e1e", bg="#ffffff")
    label3.place(x=760, y=230)

    combo = Combobox(root)
    combo['values'] = train1
    combo.place(x=650, y=270, width=280, height=25)

    def show2():
        label4 = tk.Label(root, text="TICKET COUNT", font=("ARIAL", 16), fg="#1e1e1e", bg="#ffffff")
        label4.place(x=720, y=310)

        spinbox = tk.Spinbox(root, from_=1, to=15, font=("Arial", 12))
        spinbox.place(x=650, y=350, width=280, height=30)

        def save_data():
            name = entryNAME.get().strip()
            gen = radio_var.get()
            detail = combo.get()
            count = spinbox.get()

            if name == "":
                messagebox.showerror("Error", "Please enter passenger name")
                return
            if detail == "":
                messagebox.showerror("Error", "Please select a train")
                return
            if count == "":
                messagebox.showerror("Error", "Please enter ticket count")
                return

            # Insert Data - ID auto-generates safely
            query = """
            INSERT INTO train (passenger_name, gender, train_name, ticket_count)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (name, gen, detail, count))
            conn.commit()

            # Retrieve the specific ID generated for this ticket
            ticket_no = cursor.lastrowid

            # Pop-up showing comprehensive final booking details
            receipt = (
                f"TICKET BOOKED SUCCESSFULLY!\n\n"
                f"Ticket No: {ticket_no}\n"
                f"Passenger Name: {name}\n"
                f"Train: {detail}\n"
                f"Tickets: {count}"
            )
            messagebox.showinfo("Booking Confirmed", receipt)
            print("Data inserted safely")

        btn4 = tk.Button(
            root,
            text="CONFIRM BOOKING",
            font=("Arial", 15),
            bg="#F2A464",
            command=save_data
        )
        btn4.place(x=520, y=500, width=500, height=50)

    btn2 = tk.Button(
        root,
        text="BOOK TRAIN",
        font=("Arial", 15),
        bg="#03818C",
        fg="#ffffff",
        command=show2
    )
    btn2.place(x=520, y=430, width=500, height=50)

def close():
    root.quit()

def cancel():
    cancel_window = tk.Toplevel(root)
    cancel_window.title("Cancel Train")
    cancel_window.geometry("500x300")
    cancel_window.config(bg="#ffffff")

    # Only matching the exact Ticket Number required for explicit deletion
    labely = tk.Label(cancel_window, text="ENTER TICKET NUMBER", fg="#1e1e1e", bg="#ffffff", font=("arial", 14))
    labely.pack(pady=20)

    entryy = tk.Entry(cancel_window, bd=2, font=("Arial", 12))
    entryy.pack(pady=10, ipadx=60, ipady=4)

    def cancel_booking():
        tick_no = entryy.get().strip()

        if tick_no == "":
            messagebox.showerror("Error", "Please enter your Ticket Number")
            return

        # Fetch details BEFORE deleting so we can show them to the user
        cursor.execute("SELECT passenger_name, train_name, ticket_count FROM train WHERE id = %s", (tick_no,))
        record = cursor.fetchone()

        if record:
            p_name, t_name, t_count = record
            
            # Target specifically by Primary Key ID. Values are removed without modifying other keys.
            cursor.execute("DELETE FROM train WHERE id = %s", (tick_no,))
            conn.commit()

            cancellation_receipt = (
                f"TICKET CANCELED SUCCESSFULLY!\n\n"
                f"Ticket No: {tick_no}\n"
                f"Passenger: {p_name}\n"
                f"Train: {t_name}\n"
                f"Tickets Cleared: {t_count}"
            )
            messagebox.showinfo("Success", cancellation_receipt)
            cancel_window.destroy()
        else:
            messagebox.showwarning("Not Found", "No matching booking found with that Ticket Number")

    btn_submit = tk.Button(
        cancel_window,
        text="CONFIRM CANCELLATION",
        font=("Arial", 12, "bold"),
        bg="#D9534F",
        fg="#ffffff",
        command=cancel_booking
    )
    btn_submit.pack(pady=20)

btn1 = tk.Button(root, text="VIEW TRAIN OPTIONS", font=("Arial", 15), bg="#03818C", fg="#ffffff", command=show1)
btn1.place(x=520, y=40, width=500, height=45)

btn5 = tk.Button(root, text="CANCEL TRAIN", font=("Arial", 15), bg="#03818C", fg="#ffffff", command=cancel)
btn5.place(x=1200, y=200, width=350, height=50)

btn6 = tk.Button(root, text="EXIT PAGE", font=("Arial", 15), bg="#03818C", fg="#ffffff", command=close)
btn6.place(x=1200, y=300, width=350, height=50)

root.mainloop()'''