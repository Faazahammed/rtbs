import tkinter as tk
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

# Define unique ticket capacity limits per train string match
TRAIN_LIMITS = {
    "325432       DHURANDH EXPRESS": 50,
    "543254       MANGORE EXPRESS": 80,  # Set to maximum allowed value
    "656565       KASARGOD EXPRESS":75,
    "232323       TRIVANDRUM EXPRESS": 90
}

def show1():
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

        lbl_remaining = tk.Label(root, text="", font=("Arial", 12, "bold"), fg="#03818C", bg="#ffffff")
        lbl_remaining.place(x=650, y=390, width=280)

        def update_remaining_display(event=None):
            selected_train = combo.get()
            # If train is recognized, calculate its specific remaining capacity
            if selected_train in TRAIN_LIMITS:
                max_capacity = TRAIN_LIMITS[selected_train]
                cursor.execute("SELECT SUM(ticket_count) FROM train WHERE train_name = %s", (selected_train,))
                result = cursor.fetchone()
                current_booked = int(result[0]) if result[0] is not None else 0
                remaining = max_capacity - current_booked
                
                if remaining <= 0:
                    lbl_remaining.config(text="REMAINING TICKETS: 0", fg="#D9534F")
                else:
                    lbl_remaining.config(text=f"REMAINING TICKETS: {remaining}", fg="#03818C")
            else:
                lbl_remaining.config(text="")

        # Bind event to refresh live counter whenever a new train selection drops
        combo.bind("<<ComboboxSelected>>", update_remaining_display)
        update_remaining_display()

        def save_data():
            name = entryNAME.get().strip()
            gen = radio_var.get()
            detail = combo.get()
            count_str = spinbox.get()

            if name == "":
                messagebox.showerror("ERROR", "Please enter PASSENGER NAME")
                return
            if detail == "":
                messagebox.showerror("ERROR", "Please select a TRAIN")
                return
            if count_str == "":
                messagebox.showerror("ERROR", "Please enter TICKET COUNT")
                return

            try:
                requested_tickets = int(count_str)
            except ValueError:
                messagebox.showerror("ERROR", "Ticket count must be a number")
                return

            # Check if selected train exists in defined limits dictionary
            if detail not in TRAIN_LIMITS:
                messagebox.showerror("ERROR", "Selected train capacity configurations missing")
                return

            max_limit = TRAIN_LIMITS[detail]

            # Fetch targeted total booked seats for this specific train name
            cursor.execute("SELECT SUM(ticket_count) FROM train WHERE train_name = %s", (detail,))
            sum_result = cursor.fetchone()
            total_booked = int(sum_result[0]) if sum_result[0] is not None else 0

            tickets_left = max_limit - total_booked

            # Rule 1: Check if train limit has already peaked
            if total_booked >= max_limit:
                messagebox.showerror("ERROR", "TICKETS FINISHED")
                update_remaining_display()
                return

            # Rule 2: Ensure transaction size doesn't push train over capacity boundaries
            if requested_tickets > tickets_left:
                messagebox.showwarning(
                    "Insufficient Tickets", 
                    f"Cannot book {requested_tickets} tickets.\nOnly {tickets_left} remaining tickets left on this train!"
                )
                return

            # Insert Data securely
            query = """
            INSERT INTO train (passenger_name, gender, train_name, ticket_count)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (name, gen, detail, requested_tickets))
            conn.commit()

            ticket_no = cursor.lastrowid

            receipt = (
                f"TICKET BOOKED SUCCESSFULLY!\n\n"
                f"TICKET NO: {ticket_no}\n"
                f"PASSENGER NAME: {name}\n"
                f"TRAIN: {detail}\n"
                f"TICKETS: {requested_tickets}"
            )
            messagebox.showinfo("BOOKING CONFIRMED", receipt)
            print("Data inserted safely")
            
            update_remaining_display()

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
    cancel_window.title("CANCELK TRAIN")
    cancel_window.geometry("500x300")
    cancel_window.config(bg="#ffffff")

    labely = tk.Label(cancel_window, text="ENTER TICKET NUMBER", fg="#1e1e1e", bg="#ffffff", font=("arial", 14))
    labely.pack(pady=20)

    entryy = tk.Entry(cancel_window, bd=2, font=("Arial", 12))
    entryy.pack(pady=10, ipadx=60, ipady=4)

    def cancel_booking():
        tick_no = entryy.get().strip()

        if tick_no == "":
            messagebox.showerror("ERROR", "Please enter your TICKET NUMBER")
            return

        cursor.execute("SELECT passenger_name, train_name, ticket_count FROM train WHERE id = %s", (tick_no,))
        record = cursor.fetchone()

        if record:
            p_name, t_name, t_count = record
            
            cursor.execute("DELETE FROM train WHERE id = %s", (tick_no,))
            conn.commit()

            cancellation_receipt = (
                f"TICKET CANCELED SUCCESSFULLY!\n\n"
                f"TICKET NO: {tick_no}\n"
                f"PASSANGER: {p_name}\n"
                f"TRAIN: {t_name}\n"
                f"TICKETS CANCELED: {t_count}"
            )
            messagebox.showinfo("SUCCESS", cancellation_receipt)
            cancel_window.destroy()
        else:
            messagebox.showwarning("NOT FOUND ", "No matching booking found with that TICKET NUMBER")

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

root.mainloop()
