from tkinter import *
from tkinter import messagebox
import mysql.connector
import dashboard
import register


# ---------------- MYSQL CONNECTION ----------------

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="student_management"
)

mycursor = mydb.cursor()


# ---------------- LOGIN FUNCTION ----------------

def login():

    user = username.get().strip()
    pwd = password.get().strip()

    if user == "" or pwd == "":
        messagebox.showwarning(
            "Warning",
            "Please enter username and password"
        )
        return


    # ---------------- ADMIN LOGIN ----------------

    if user == "admin" and pwd == "1234":

        window.withdraw()

        dashboard.admin_dashboard(window)

        return


    # ---------------- TEACHER LOGIN ----------------

    sql = """
    SELECT username, subject
    FROM users
    WHERE username = %s
    AND password = %s
    """

    mycursor.execute(
        sql,
        (user, pwd)
    )

    teacher = mycursor.fetchone()


    if teacher:

        teacher_name = teacher[0]
        subject = teacher[1]

        window.withdraw()

        dashboard.teacher_dashboard(
            teacher_name,
            subject,window
        )

        return


    # ---------------- STUDENT LOGIN ----------------

    sql = """
    SELECT id, name
    FROM students
    WHERE username = %s
    AND password = %s
    """

    mycursor.execute(
        sql,
        (user, pwd)
    )

    student = mycursor.fetchone()


    if student:

        student_id = student[0]
        student_name = student[1]

        window.withdraw()

        dashboard.student_dashboard(
            student_id,
            student_name,window
        )

        return


    # ---------------- INVALID LOGIN ----------------

    messagebox.showerror(
        "Login Error",
        "Invalid Username or Password"
    )


# ---------------- TEACHER REGISTER ----------------

def open_teacher_register():

    register.create_account()


# ---------------- STUDENT REGISTER ----------------

def open_student_register():

    register.student_registration(window)


# =================================================
# LOGIN WINDOW
# =================================================

window = Tk()

window.title("School Login")

window.geometry("800x1000")

window.config(
    bg="#0E878E"
)


frame = Frame(
    window,
    bg="#0E878E",
    bd=2,
    relief="solid"
)

frame.pack(
    padx=40,
    pady=40,
    fill="both",
    expand=True
)


Label(
    frame,
    text="SCOPE SCHOOL OF TECHNOLOGY",
    bg="#0E878E",
    fg="white",
    font=("Arial", 13, "bold")
).pack(
    pady=20
)


Label(
    frame,
    text="LOGIN",
    bg="#0E878E",
    fg="white",
    font=("Arial", 18, "bold")
).pack(
    pady=10
)


# Username

Label(
    frame,
    text="Username",
    bg="#0E878E",
    fg="white"
).pack()

username = Entry(
    frame,
    width=25
)

username.pack(
    pady=10
)


# Password

Label(
    frame,
    text="Password",
    bg="#0E878E",
    fg="white"
).pack()

password = Entry(
    frame,
    width=25,
    show="*"
)

password.pack(
    pady=10
)


# Login Button

Button(
    frame,
    text="LOGIN",
    width=10,
    command=login
).pack(
    pady=15
)


# Teacher Register

Button(
    frame,
    text="TEACHER REGISTER",
    width=20,
    command=open_teacher_register
).pack(
    pady=5
)


# Student Register

Button(
    frame,
    text="STUDENT REGISTER",
    width=20,
    command=open_student_register
).pack(
    pady=5
)


window.mainloop()