from tkinter import *
from tkinter import messagebox
import mysql.connector


# =================================================
# MYSQL CONNECTION
# =================================================

def connect_database():

    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="student_management"
    )


# =================================================
# TEACHER REGISTRATION
# =================================================

def create_account():

    window = Toplevel()

    window.title("Teacher Registration")
    window.geometry("800x1000")

    window.config(bg="#0E878E")

    mydb = connect_database()
    mycursor = mydb.cursor()

    Label(
        window,
        text="TEACHER REGISTRATION",
        bg="#0E878E",
        fg="white",
        font=("Arial", 16, "bold")
    ).pack(pady=20)

    Label(
        window,
        text="Teacher Username",
        bg="#0E878E",
        fg="white"
    ).pack()

    teacher_name = Entry(window)

    teacher_name.pack(pady=10)

    Label(
        window,
        text="Password",
        bg="#0E878E",
        fg="white"
    ).pack()

    teacher_password = Entry(
        window,
        show="*"
    )

    teacher_password.pack(pady=10)

    Label(
        window,
        text="Select Subject",
        bg="#0E878E",
        fg="white"
    ).pack()

    subject = StringVar()

    subject.set("Tamil")

    OptionMenu(
        window,
        subject,
        "Tamil",
        "English",
        "Maths",
        "Science",
        "Social"
    ).pack(pady=10)

    def register_teacher():

        name = teacher_name.get().strip()
        pwd = teacher_password.get().strip()
        sub = subject.get()

        if name == "" or pwd == "":

            messagebox.showwarning(
                "Warning",
                "Please enter all details"
            )

            return

        mycursor.execute(
            "SELECT * FROM users WHERE username = %s",
            (name,)
        )

        result = mycursor.fetchone()

        if result:

            messagebox.showerror(
                "Error",
                "Username already exists"
            )

            return

        sql = """
        INSERT INTO users
        (username, password, subject, role)
        VALUES (%s, %s, %s, %s)
        """

        mycursor.execute(
            sql,
            (
                name,
                pwd,
                sub,
                "teacher"
            )
        )

        mydb.commit()

        messagebox.showinfo(
            "Success",
            "Teacher Account Created!"
        )

        teacher_name.delete(0, END)
        teacher_password.delete(0, END)

    Button(
        window,
        text="CREATE ACCOUNT",
        command=register_teacher,
        width=20,
        bg="green",
        fg="white"
    ).pack(pady=20)


# =================================================
# STUDENT REGISTRATION
# =================================================

def student_registration(login_window):

    window = Toplevel(login_window)

    window.title("Student Registration")

    window.geometry("800x1000")

    window.config(
        bg="#E8F6F7"
    )

    Label(
        window,
        text="STUDENT REGISTRATION",
        font=("Arial", 18, "bold"),
        bg="#E8F6F7",
        fg="#0E878E"
    ).pack(pady=20)

    # Student Name

    Label(
        window,
        text="Student Name",
        bg="#E8F6F7"
    ).pack()

    name_entry = Entry(
        window,
        width=30
    )

    name_entry.pack(pady=8)

    # Username

    Label(
        window,
        text="Username",
        bg="#E8F6F7"
    ).pack()

    username_entry = Entry(
        window,
        width=30
    )

    username_entry.pack(pady=8)

    # Password

    Label(
        window,
        text="Password",
        bg="#E8F6F7"
    ).pack()

    password_entry = Entry(
        window,
        width=30,
        show="*"
    )

    password_entry.pack(pady=8)
# Standard

    Label(
    window,
    text="Class / Standard",
    bg="#E8F6F7"
    ).pack()

    standard_var = StringVar()

    standard_var.set("6th")

    standard_menu = OptionMenu(
    window,
    standard_var,
    "6th",
    "7th",
    "8th",
    "9th",
    "10th"
    )

    standard_menu.config(
    width=25
    )

    standard_menu.pack(pady=8)

    # Phone

    Label(
        window,
        text="Phone",
        bg="#E8F6F7"
    ).pack()

    phone_entry = Entry(
        window,
        width=30
    )

    phone_entry.pack(pady=8)

    # Email

    Label(
        window,
        text="Email",
        bg="#E8F6F7"
    ).pack()

    email_entry = Entry(
        window,
        width=30
    )

    email_entry.pack(pady=8)

    # Address

    Label(
        window,
        text="Address",
        bg="#E8F6F7"
    ).pack()

    address_entry = Entry(
        window,
        width=30
    )

    address_entry.pack(pady=8)

    def register_student():

        name = name_entry.get().strip()
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        standard = standard_var.get().strip()
        phone = phone_entry.get().strip()

        if not phone.isdigit():

            messagebox.showwarning(
                "Invalid Mobile Number",
                "Mobile number should contain numbers only!"
            )

            return

        if len(phone) != 10:

            messagebox.showwarning(
                "Invalid Mobile Number",
                "Mobile number must be exactly 10 digits!"
            )

            return

        email = email_entry.get().strip()

        if not email.endswith("@gmail.com"):

            messagebox.showwarning(
                "Ivalid Gmail",
                "please enter a valid Gmail"
            )

            return

        address = address_entry.get().strip()

        if (
            name == ""
            or username == ""
            or password == ""
            or standard == ""
        ):

            messagebox.showwarning(
                "Warning",
                "Please fill required details"
            )

            return

        mydb = connect_database()

        mycursor = mydb.cursor()

        # Check username

        mycursor.execute(
            """
            SELECT id FROM students
            WHERE username = %s
            """,
            (username,)
        )

        if mycursor.fetchone():

            messagebox.showerror(
                "Error",
                "Username already exists"
            )

            mydb.close()

            return

        # Insert student

        sql = """
        INSERT INTO students
        (
            name,
            username,
            password,
            standard,
            phone,
            email,
            address
        )
        VALUES
        (
            %s, %s, %s, %s, %s, %s, %s
        )
        """

        values = (
            name,
            username,
            password,
            standard,
            phone,
            email,
            address
        )

        mycursor.execute(
            sql,
            values
        )

        mydb.commit()

        mydb.close()

        messagebox.showinfo(
            "Success",
            "Student Account Created Successfully!"
        )

        name_entry.delete(0, END)
        username_entry.delete(0, END)
        password_entry.delete(0, END)
        standard_var.set("6th")
        phone_entry.delete(0, END)
        email_entry.delete(0, END)
        address_entry.delete(0, END)

    Button(
        window,
        text="CREATE STUDENT ACCOUNT",
        width=25,
        bg="#0E878E",
        fg="white",
        command=register_student
    ).pack(pady=20)

    # =========================================
    # BACK TO LOGIN
    # =========================================

    def back_to_login():

        window.destroy()

        login_window.deiconify()

    Button(
        window,
        text="BACK TO LOGIN",
        width=25,
        bg="#DC3545",
        fg="white",
        command=back_to_login
    ).pack(pady=5)