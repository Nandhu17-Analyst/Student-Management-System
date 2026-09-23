from tkinter import *
from tkinter import messagebox, filedialog
import mysql.connector
import csv

try:
    from openpyxl import Workbook
except ImportError:
    Workbook = None


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
# ADMIN DASHBOARD
# =================================================

def admin_dashboard(login_window):

    window = Toplevel(login_window)
    window.title("Admin Dashboard")

    # =================================================
    # FULL SCREEN / MAXIMIZED WINDOW
    # =================================================

    window.state("zoomed")
    window.config(bg="#E8F6F7")

    # =================================================
    # MAIN SCROLLABLE PAGE
    # =================================================

    main_canvas = Canvas(
        window,
        bg="#E8F6F7",
        highlightthickness=0
    )

    main_scrollbar = Scrollbar(
        window,
        orient=VERTICAL,
        command=main_canvas.yview
    )

    main_scrollbar.pack(
        side=RIGHT,
        fill=Y
    )

    main_canvas.pack(
        side=LEFT,
        fill=BOTH,
        expand=True
    )

    main_canvas.configure(
        yscrollcommand=main_scrollbar.set
    )

    main_frame = Frame(
        main_canvas,
        bg="#E8F6F7"
    )

    main_window = main_canvas.create_window(
        (0, 0),
        window=main_frame,
        anchor="nw"
    )

    # =================================================
    # UPDATE MAIN SCROLL REGION
    # =================================================

    def update_main_scroll(event=None):

        main_canvas.configure(
            scrollregion=main_canvas.bbox("all")
        )

    main_frame.bind(
        "<Configure>",
        update_main_scroll
    )

    # =================================================
    # MAKE CONTENT FULL WIDTH
    # =================================================

    def update_canvas_width(event):

        main_canvas.itemconfig(
            main_window,
            width=event.width
        )

    main_canvas.bind(
        "<Configure>",
        update_canvas_width
    )

    # =================================================
    # MOUSE SCROLL
    # =================================================

    def mouse_scroll(event):

        main_canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    main_canvas.bind_all(
        "<MouseWheel>",
        mouse_scroll
    )

    # =================================================
    # HEADER
    # =================================================

    header = Frame(
        main_frame,
        bg="#0E878E",
        height=90
    )

    header.pack(
        fill="x"
    )

    header.pack_propagate(False)

    Label(
        header,
        text="SCOPE SCHOOL OF TECHNOLOGY",
        font=("Arial", 21, "bold"),
        bg="#0E878E",
        fg="white"
    ).pack(
        pady=(15, 3)
    )

    Label(
        header,
        text="ADMIN DASHBOARD",
        font=("Arial", 11),
        bg="#0E878E",
        fg="white"
    ).pack()

    # =================================================
    # SUMMARY
    # =================================================

    summary = Frame(
        main_frame,
        bg="#E8F6F7"
    )

    summary.pack(
        pady=15
    )

    def make_card(column, title, color):

        frame = Frame(
            summary,
            bg="white",
            width=190,
            height=100,
            bd=1,
            relief="solid"
        )

        frame.grid(
            row=0,
            column=column,
            padx=6
        )

        frame.grid_propagate(False)

        Label(
            frame,
            text=title,
            bg="white",
            fg="#666666",
            font=("Arial", 9, "bold")
        ).pack(
            pady=(12, 4)
        )

        value = Label(
            frame,
            text="0",
            bg="white",
            fg=color,
            font=("Arial", 18, "bold")
        )

        value.pack()

        return value

    total_students_label = make_card(
        0,
        "TOTAL STUDENTS",
        "#0E878E"
    )

    highest_total_label = make_card(
        1,
        "HIGHEST TOTAL",
        "green"
    )

    topper_label = make_card(
        2,
        "OVERALL TOPPER",
        "#D97706"
    )

    average_label = make_card(
        3,
        "AVERAGE %",
        "#7C3AED"
    )

    # =================================================
    # ADD STUDENT
    # =================================================

    registration = Frame(
        main_frame,
        bg="white",
        bd=1,
        relief="solid"
    )

    registration.pack(
        fill="x",
        padx=30,
        pady=5
    )

    Label(
        registration,
        text="ADD STUDENT",
        bg="white",
        fg="#0E878E",
        font=("Arial", 12, "bold")
    ).pack(
        side=LEFT,
        padx=20,
        pady=15
    )

    student_name = Entry(
        registration,
        width=30
    )

    student_name.pack(
        side=LEFT,
        padx=10
    )

    def add_student():

        name = student_name.get().strip()

        if name == "":

            messagebox.showwarning(
                "Warning",
                "Enter student name"
            )

            return

        try:

            mydb = connect_database()
            cursor = mydb.cursor()

            cursor.execute(
                "INSERT INTO students (name) VALUES (%s)",
                (name,)
            )

            mydb.commit()
            mydb.close()

            student_name.delete(
                0,
                END
            )

            messagebox.showinfo(
                "Success",
                "Student Added Successfully!"
            )

            show_students()

        except mysql.connector.Error as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

    Button(
        registration,
        text="ADD STUDENT",
        width=18,
        bg="#0E878E",
        fg="white",
        command=add_student
    ).pack(
        side=LEFT,
        padx=10
    )

    # =================================================
    # SUBJECT WISE TOPPERS
    # =================================================

    Label(
        main_frame,
        text="SUBJECT WISE TOPPERS",
        bg="#E8F6F7",
        fg="#0E878E",
        font=("Arial", 13, "bold")
    ).pack(
        pady=(15, 5)
    )

    subject_topper_frame = Frame(
        main_frame,
        bg="white",
        bd=1,
        relief="solid"
    )

    subject_topper_frame.pack(
        padx=30,
        fill="x"
    )

    subject_topper_label = Label(
        subject_topper_frame,
        text="No data",
        bg="white",
        font=("Arial", 10),
        justify=LEFT
    )

    subject_topper_label.pack(
        padx=15,
        pady=12
    )

    # =================================================
    # CLASS WISE TOPPERS
    # =================================================

    Label(
        main_frame,
        text="CLASS WISE TOPPERS",
        bg="#E8F6F7",
        fg="#0E878E",
        font=("Arial", 13, "bold")
    ).pack(
        pady=(15, 5)
    )

    class_topper_frame = Frame(
        main_frame,
        bg="white",
        bd=1,
        relief="solid"
    )

    class_topper_frame.pack(
        padx=30,
        fill="x"
    )

    class_topper_labels = {}

    classes = [
        "6th",
        "7th",
        "8th",
        "9th",
        "10th"
    ]

    for standard in classes:

        frame = Frame(
            class_topper_frame,
            bg="white"
        )

        frame.pack(
            fill="x",
            padx=15,
            pady=4
        )

        label = Label(
            frame,
            text=standard + " : No data",
            bg="white",
            font=("Arial", 10, "bold"),
            anchor="w"
        )

        label.pack(
            fill="x"
        )

        class_topper_labels[
            standard
        ] = label

    # =================================================
    # STANDARD FILTER
    # =================================================

    filter_frame = Frame(
        main_frame,
        bg="#E8F6F7"
    )

    filter_frame.pack(
        pady=10
    )

    Label(
        filter_frame,
        text="Select Standard:",
        bg="#E8F6F7",
        font=("Arial", 10, "bold")
    ).pack(
        side=LEFT,
        padx=5
    )

    standard_filter = StringVar()
    standard_filter.set("All")

    standard_menu = OptionMenu(
        filter_frame,
        standard_filter,
        "All",
        "6th",
        "7th",
        "8th",
        "9th",
        "10th"
    )

    standard_menu.config(
        width=12
    )

    standard_menu.pack(
        side=LEFT,
        padx=5
    )

    # =================================================
    # EXPORT FUNCTIONS
    # =================================================

    def get_export_data():

        db = connect_database()
        cursor = db.cursor()

        selected_standard = standard_filter.get()

        if selected_standard == "All":

            cursor.execute(
                """
                SELECT
                    id,
                    name,
                    standard,
                    phone,
                    email,
                    address,
                    tamil,
                    english,
                    maths,
                    science,
                    social
                FROM students
                ORDER BY id
                """
            )

        else:

            cursor.execute(
                """
                SELECT
                    id,
                    name,
                    standard,
                    phone,
                    email,
                    address,
                    tamil,
                    english,
                    maths,
                    science,
                    social
                FROM students
                WHERE standard = %s
                ORDER BY id
                """,
                (selected_standard,)
            )

        students = cursor.fetchall()

        db.close()

        headers = [
            "ID",
            "Student Name",
            "Class",
            "Phone",
            "Email",
            "Address",
            "Tamil",
            "English",
            "Maths",
            "Science",
            "Social",
            "Total",
            "Percentage"
        ]

        rows = []

        for student in students:

            tamil = student[6] or 0
            english = student[7] or 0
            maths = student[8] or 0
            science = student[9] or 0
            social = student[10] or 0

            total = (
                tamil +
                english +
                maths +
                science +
                social
            )

            percentage = (
                total / 500
            ) * 100

            rows.append([
                student[0],
                student[1],
                student[2] or "-",
                student[3] or "-",
                student[4] or "-",
                student[5] or "-",
                tamil,
                english,
                maths,
                science,
                social,
                total,
                f"{percentage:.2f}%"
            ])

        return headers, rows

    # =================================================
    # EXPORT CSV
    # =================================================

    def export_csv():

        try:

            headers, rows = get_export_data()

            if not rows:

                messagebox.showwarning(
                    "No Data",
                    "No student data available to export."
                )

                return

            selected = standard_filter.get()

            filename = filedialog.asksaveasfilename(
                title="Save Student CSV File",
                defaultextension=".csv",
                filetypes=[
                    ("CSV Files", "*.csv")
                ],
                initialfile=(
                    "student_details_" +
                    selected +
                    ".csv"
                )
            )

            if not filename:
                return

            with open(
                filename,
                "w",
                newline="",
                encoding="utf-8-sig"
            ) as file:

                writer = csv.writer(file)

                writer.writerow(headers)
                writer.writerows(rows)

            messagebox.showinfo(
                "Export Successful",
                "Student details exported successfully!\n\n"
                + filename
            )

        except mysql.connector.Error as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

        except Exception as e:

            messagebox.showerror(
                "Export Error",
                str(e)
            )

    # =================================================
    # EXPORT EXCEL
    # =================================================

    def export_excel():

        if Workbook is None:

            messagebox.showerror(
                "Missing Package",
                "Excel export requires openpyxl.\n\n"
                "Install it using:\n"
                "pip install openpyxl"
            )

            return

        try:

            headers, rows = get_export_data()

            if not rows:

                messagebox.showwarning(
                    "No Data",
                    "No student data available to export."
                )

                return

            selected = standard_filter.get()

            filename = filedialog.asksaveasfilename(
                title="Save Student Excel File",
                defaultextension=".xlsx",
                filetypes=[
                    ("Excel Files", "*.xlsx")
                ],
                initialfile=(
                    "student_details_" +
                    selected +
                    ".xlsx"
                )
            )

            if not filename:
                return

            workbook = Workbook()

            sheet = workbook.active
            sheet.title = "Student Details"

            sheet.append(headers)

            for row in rows:

                sheet.append(row)

            # Make columns readable
            for column in sheet.columns:

                max_length = 0

                column_letter = (
                    column[0].column_letter
                )

                for cell in column:

                    if cell.value is not None:

                        length = len(
                            str(cell.value)
                        )

                        if length > max_length:
                            max_length = length

                sheet.column_dimensions[
                    column_letter
                ].width = min(
                    max_length + 2,
                    35
                )

            sheet.freeze_panes = "A2"

            sheet.auto_filter.ref = (
                sheet.dimensions
            )

            workbook.save(filename)

            messagebox.showinfo(
                "Export Successful",
                "Student details exported successfully!\n\n"
                + filename
            )

        except mysql.connector.Error as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

        except Exception as e:

            messagebox.showerror(
                "Export Error",
                str(e)
            )

    # =================================================
    # EXPORT BUTTONS
    # =================================================

    Label(
        main_frame,
        text="DOWNLOAD STUDENT DETAILS",
        bg="#E8F6F7",
        fg="#0E878E",
        font=("Arial", 13, "bold")
    ).pack(
        pady=(15, 5)
    )

    export_frame = Frame(
        main_frame,
        bg="white",
        bd=1,
        relief="solid"
    )

    export_frame.pack(
        padx=30,
        fill="x",
        pady=5
    )

    Label(
        export_frame,
        text=(
            "Download student details with marks, "
            "class, phone, email and address."
        ),
        bg="white",
        fg="#555555",
        font=("Arial", 10)
    ).pack(
        pady=(12, 8)
    )

    Button(
        export_frame,
        text="DOWNLOAD CSV",
        width=20,
        bg="#0E878E",
        fg="white",
        font=("Arial", 10, "bold"),
        command=export_csv
    ).pack(
        side=LEFT,
        padx=10,
        pady=12
    )

    Button(
        export_frame,
        text="DOWNLOAD EXCEL",
        width=20,
        bg="#198754",
        fg="white",
        font=("Arial", 10, "bold"),
        command=export_excel
    ).pack(
        side=LEFT,
        padx=10,
        pady=12
    )

    # =================================================
    # TABLE TITLE
    # =================================================

    Label(
        main_frame,
        text="STUDENT MARK DETAILS",
        bg="#E8F6F7",
        fg="#0E878E",
        font=("Arial", 14, "bold")
    ).pack(
        pady=5
    )

    # =================================================
    # TABLE
    # =================================================

    outer = Frame(
        main_frame,
        bg="white"
    )

    outer.pack(
        padx=30,
        pady=5,
        fill="both",
        expand=True
    )

    canvas = Canvas(
        outer,
        bg="white",
        height=300
    )

    canvas.pack(
        side=LEFT,
        fill="both",
        expand=True
    )

    scrollbar = Scrollbar(
        outer,
        orient=VERTICAL,
        command=canvas.yview
    )

    scrollbar.pack(
        side=RIGHT,
        fill=Y
    )

    canvas.configure(
        yscrollcommand=scrollbar.set
    )

    table = Frame(
        canvas,
        bg="white"
    )

    table_window = canvas.create_window(
        (0, 0),
        window=table,
        anchor="nw"
    )

    # =================================================
    # TABLE SCROLL REGION
    # =================================================

    def update_table_scroll(event=None):

        canvas.configure(
            scrollregion=canvas.bbox("all")
        )

    table.bind(
        "<Configure>",
        update_table_scroll
    )

    # =================================================
    # MAKE TABLE FULL WIDTH
    # =================================================

    def update_table_width(event):

        canvas.itemconfig(
            table_window,
            width=event.width
        )

    canvas.bind(
        "<Configure>",
        update_table_width
    )

    # =================================================
    # TABLE HEADINGS
    # =================================================

    headings = [
        "ID",
        "STUDENT",
        "CLASS",
        "TAMIL",
        "ENGLISH",
        "MATHS",
        "SCIENCE",
        "SOCIAL",
        "TOTAL",
        "OVERALL %"
    ]

    for col, heading in enumerate(headings):

        Label(
            table,
            text=heading,
            width=14,
            height=2,
            bg="#0E878E",
            fg="white",
            font=("Arial", 9, "bold"),
            relief="solid"
        ).grid(
            row=0,
            column=col,
            sticky="nsew"
        )

    # =================================================
    # SHOW STUDENTS
    # =================================================

    def show_students():

        try:

            for widget in table.winfo_children():

                if int(
                    widget.grid_info()["row"]
                ) > 0:

                    widget.destroy()

            db = connect_database()
            cursor = db.cursor()

            selected_standard = (
                standard_filter.get()
            )

            if selected_standard == "All":

                cursor.execute(
                    """
                    SELECT
                        id,
                        name,
                        standard,
                        tamil,
                        english,
                        maths,
                        science,
                        social
                    FROM students
                    """
                )

            else:

                cursor.execute(
                    """
                    SELECT
                        id,
                        name,
                        standard,
                        tamil,
                        english,
                        maths,
                        science,
                        social
                    FROM students
                    WHERE standard = %s
                    """,
                    (selected_standard,)
                )

            students = cursor.fetchall()

            db.close()

            total_students_label.config(
                text=str(len(students))
            )

            if not students:

                highest_total_label.config(
                    text="0 / 500"
                )

                topper_label.config(
                    text="-"
                )

                average_label.config(
                    text="0%"
                )

                subject_topper_label.config(
                    text="No student data"
                )

                for standard in classes:

                    class_topper_labels[
                        standard
                    ].config(
                        text=standard + " : No data"
                    )

                return

            highest_total = -1
            overall_topper = "-"
            percentage_sum = 0

            subject_marks = {

                "Tamil": (-1, "-"),
                "English": (-1, "-"),
                "Maths": (-1, "-"),
                "Science": (-1, "-"),
                "Social": (-1, "-")

            }

            row = 1

            for student in students:

                student_id = student[0]
                name = student[1]
                standard = student[2]

                tamil = student[3] or 0
                english = student[4] or 0
                maths = student[5] or 0
                science = student[6] or 0
                social = student[7] or 0

                total = (
                    tamil +
                    english +
                    maths +
                    science +
                    social
                )

                percentage = (
                    total / 500
                ) * 100

                percentage_sum += percentage

                if total > highest_total:

                    highest_total = total
                    overall_topper = name

                marks = {

                    "Tamil": tamil,
                    "English": english,
                    "Maths": maths,
                    "Science": science,
                    "Social": social

                }

                for subject_name, mark in marks.items():

                    if mark > subject_marks[
                        subject_name
                    ][0]:

                        subject_marks[
                            subject_name
                        ] = (
                            mark,
                            name
                        )

                values = [

                    student_id,
                    name,
                    standard or "-",
                    tamil,
                    english,
                    maths,
                    science,
                    social,
                    total,
                    f"{percentage:.2f}%"

                ]

                for col, value in enumerate(values):

                    Label(
                        table,
                        text=value,
                        width=14,
                        height=2,
                        bg="white",
                        relief="solid"
                    ).grid(
                        row=row,
                        column=col,
                        sticky="nsew"
                    )

                row += 1

            average = (
                percentage_sum /
                len(students)
            )

            highest_total_label.config(
                text=str(highest_total) +
                " / 500"
            )

            topper_label.config(
                text=overall_topper
            )

            average_label.config(
                text=f"{average:.2f}%"
            )

            topper_text = (

                "Tamil    : " +
                subject_marks["Tamil"][1] +
                " (" +
                str(subject_marks["Tamil"][0]) +
                ")\n" +

                "English  : " +
                subject_marks["English"][1] +
                " (" +
                str(subject_marks["English"][0]) +
                ")\n" +

                "Maths    : " +
                subject_marks["Maths"][1] +
                " (" +
                str(subject_marks["Maths"][0]) +
                ")\n" +

                "Science  : " +
                subject_marks["Science"][1] +
                " (" +
                str(subject_marks["Science"][0]) +
                ")\n" +

                "Social   : " +
                subject_marks["Social"][1] +
                " (" +
                str(subject_marks["Social"][0]) +
                ")"

            )

            subject_topper_label.config(
                text=topper_text
            )

            # =================================================
            # CLASS WISE TOPPERS
            # =================================================

            for standard in classes:

                class_topper_labels[
                    standard
                ].config(
                    text=standard + " : No data"
                )

            db = connect_database()
            cursor = db.cursor()

            cursor.execute(
                """
                SELECT
                    name,
                    standard,
                    tamil,
                    english,
                    maths,
                    science,
                    social
                FROM students
                WHERE standard IS NOT NULL
                """
            )

            all_students = cursor.fetchall()

            db.close()

            class_toppers = {}

            for student in all_students:

                name = student[0]
                standard = student[1]

                tamil = student[2] or 0
                english = student[3] or 0
                maths = student[4] or 0
                science = student[5] or 0
                social = student[6] or 0

                total = (
                    tamil +
                    english +
                    maths +
                    science +
                    social
                )

                percentage = (
                    total / 500
                ) * 100

                if standard not in class_toppers:

                    class_toppers[
                        standard
                    ] = (
                        name,
                        total,
                        percentage
                    )

                elif total > class_toppers[
                    standard
                ][1]:

                    class_toppers[
                        standard
                    ] = (
                        name,
                        total,
                        percentage
                    )

            for standard in classes:

                if standard in class_toppers:

                    topper_name = (
                        class_toppers[
                            standard
                        ][0]
                    )

                    topper_total = (
                        class_toppers[
                            standard
                        ][1]
                    )

                    topper_percentage = (
                        class_toppers[
                            standard
                        ][2]
                    )

                    class_topper_labels[
                        standard
                    ].config(
                        text=(
                            standard +
                            " : " +
                            topper_name +
                            "  |  " +
                            str(topper_total) +
                            " / 500  |  " +
                            f"{topper_percentage:.2f}%"
                        )
                    )

        except mysql.connector.Error as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

    # =================================================
    # STANDARD FILTER EVENT
    # =================================================

    standard_filter.trace_add(
        "write",
        lambda *args: show_students()
    )

    # =================================================
    # LOGOUT
    # =================================================

    def logout():

        main_canvas.unbind_all(
            "<MouseWheel>"
        )

        window.destroy()

        login_window.deiconify()

    # =================================================
    # BOTTOM BUTTONS
    # =================================================

    button_frame = Frame(
        main_frame,
        bg="#E8F6F7"
    )

    button_frame.pack(
        pady=15
    )

    Button(
        button_frame,
        text="BACK TO LOGIN",
        width=18,
        bg="#DC3545",
        fg="white",
        font=("Arial", 10, "bold"),
        command=logout
    ).pack(
        side=LEFT,
        padx=5
    )

    Button(
        button_frame,
        text="REFRESH DATA",
        width=18,
        bg="green",
        fg="white",
        font=("Arial", 10, "bold"),
        command=show_students
    ).pack(
        side=LEFT,
        padx=5
    )

    # =================================================
    # INITIAL LOAD
    # =================================================

    show_students()


# =================================================
# TEACHER DASHBOARD
# =================================================

def teacher_dashboard(
    teacher_name,
    subject,
    login_window
):

    window = Toplevel(login_window)

    window.title("Teacher Dashboard")
    window.geometry("800x1000")
    window.config(bg="#F4F8F9")

    Label(
        window,
        text="TEACHER DASHBOARD",
        font=("Arial", 22, "bold"),
        bg="#F4F8F9",
        fg="#0E878E"
    ).pack(pady=15)

    Label(
        window,
        text="Welcome, " + teacher_name,
        font=("Arial", 13, "bold"),
        bg="#F4F8F9"
    ).pack()

    Label(
        window,
        text="Your Subject : " + subject,
        font=("Arial", 13, "bold"),
        bg="#F4F8F9",
        fg="#0E878E"
    ).pack(pady=10)

    class_filter_frame = Frame(
        window,
        bg="#F4F8F9"
    )

    class_filter_frame.pack(pady=5)

    Label(
        class_filter_frame,
        text="Select Class:",
        bg="#F4F8F9",
        font=("Arial", 10, "bold")
    ).pack(side=LEFT, padx=5)

    class_var = StringVar()
    class_var.set("All")

    class_menu = OptionMenu(
        class_filter_frame,
        class_var,
        "All",
        "6th",
        "7th",
        "8th",
        "9th",
        "10th"
    )

    class_menu.config(width=12)
    class_menu.pack(side=LEFT, padx=5)

    outer = Frame(window, bg="white")
    outer.pack(
        padx=20,
        pady=15,
        fill="both",
        expand=True
    )

    canvas = Canvas(
        outer,
        bg="white"
    )

    canvas.pack(
        side=LEFT,
        fill="both",
        expand=True
    )

    scroll = Scrollbar(
        outer,
        orient=VERTICAL,
        command=canvas.yview
    )

    scroll.pack(side=RIGHT, fill=Y)

    canvas.configure(
        yscrollcommand=scroll.set
    )

    table = Frame(
        canvas,
        bg="white"
    )

    canvas.create_window(
        (0, 0),
        window=table,
        anchor="nw"
    )

    def update_scroll(event):
        canvas.configure(
            scrollregion=canvas.bbox("all")
        )

    table.bind("<Configure>", update_scroll)

    headings = [
        "ID",
        "STUDENT",
        "CLASS",
        "TAMIL",
        "ENGLISH",
        "MATHS",
        "SCIENCE",
        "SOCIAL",
        "TOTAL",
        "PERCENTAGE"
    ]

    for col, heading in enumerate(headings):

        Label(
            table,
            text=heading,
            width=13,
            height=2,
            bg="#0E878E",
            fg="white",
            font=("Arial", 9, "bold"),
            relief="solid"
        ).grid(row=0, column=col)

    edit_frame = Frame(
        window,
        bg="#F4F8F9"
    )

    edit_frame.pack(pady=10)

    Label(
        edit_frame,
        text="Select Student:",
        bg="#F4F8F9"
    ).grid(row=1, column=0, padx=5)

    student_var = StringVar()

    student_menu = OptionMenu(
        edit_frame,
        student_var,
        ""
    )

    student_menu.config(width=20)
    student_menu.grid(row=1, column=1, padx=5)

    Label(
        edit_frame,
        text=subject + " Mark:",
        bg="#F4F8F9"
    ).grid(row=1, column=2, padx=5)

    mark_entry = Entry(
        edit_frame,
        width=10
    )

    mark_entry.grid(row=1, column=3, padx=5)

    student_dict = {}

    def load_students():

        try:

            db = connect_database()
            cursor = db.cursor()

            selected_class = class_var.get()

            for widget in table.winfo_children():

                if int(
                    widget.grid_info()["row"]
                ) > 0:

                    widget.destroy()

            if selected_class == "All":

                cursor.execute(
                    """
                    SELECT
                        id,
                        name,
                        standard,
                        tamil,
                        english,
                        maths,
                        science,
                        social
                    FROM students
                    """
                )

            else:

                cursor.execute(
                    """
                    SELECT
                        id,
                        name,
                        standard,
                        tamil,
                        english,
                        maths,
                        science,
                        social
                    FROM students
                    WHERE standard = %s
                    """,
                    (selected_class,)
                )

            students = cursor.fetchall()
            db.close()

            student_dict.clear()

            menu = student_menu["menu"]

            menu.delete(0, "end")

            for student in students:

                student_id = student[0]
                name = student[1]

                student_dict[name] = student_id

                menu.add_command(
                    label=name,
                    command=lambda value=name:
                    student_var.set(value)
                )

            if students:
                student_var.set(students[0][1])
            else:
                student_var.set("")

            row = 1

            for student in students:

                student_id = student[0]
                name = student[1]
                standard = student[2]

                tamil = student[3] or 0
                english = student[4] or 0
                maths = student[5] or 0
                science = student[6] or 0
                social = student[7] or 0

                total = (
                    tamil +
                    english +
                    maths +
                    science +
                    social
                )

                percentage = (
                    total / 500
                ) * 100

                values = [
                    student_id,
                    name,
                    standard or "-",
                    tamil,
                    english,
                    maths,
                    science,
                    social,
                    total,
                    f"{percentage:.2f}%"
                ]

                for col, value in enumerate(values):

                    Label(
                        table,
                        text=value,
                        width=13,
                        height=2,
                        bg="white",
                        relief="solid"
                    ).grid(row=row, column=col)

                row += 1

        except mysql.connector.Error as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

    def save_mark():

        name = student_var.get()
        value = mark_entry.get().strip()

        if name == "" or value == "":

            messagebox.showwarning(
                "Warning",
                "Select student and enter mark"
            )
            return

        try:
            value = int(value)
        except ValueError:

            messagebox.showerror(
                "Error",
                "Enter numbers only"
            )
            return

        if value < 0 or value > 100:

            messagebox.showerror(
                "Error",
                "Mark must be between 0 and 100"
            )
            return

        student_id = student_dict[name]

        column_map = {
            "Tamil": "tamil",
            "English": "english",
            "Maths": "maths",
            "Science": "science",
            "Social": "social"
        }

        column = column_map.get(subject)

        if column is None:

            messagebox.showerror(
                "Error",
                "Invalid subject"
            )
            return

        try:

            db = connect_database()
            cursor = db.cursor()

            sql = (
                "UPDATE students SET "
                + column +
                " = %s WHERE id = %s"
            )

            cursor.execute(
                sql,
                (value, student_id)
            )

            db.commit()
            db.close()

            messagebox.showinfo(
                "Success",
                subject + " mark updated!"
            )

            mark_entry.delete(0, END)

            load_students()

        except mysql.connector.Error as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

    Button(
        edit_frame,
        text="SAVE MARK",
        bg="#0E878E",
        fg="white",
        width=15,
        command=save_mark
    ).grid(row=1, column=4, padx=10)

    def logout():

        window.destroy()
        login_window.deiconify()

    Button(
        window,
        text="BACK TO LOGIN",
        width=20,
        bg="#DC3545",
        fg="white",
        command=logout
    ).pack(pady=10)

    class_var.trace_add(
        "write",
        lambda *args: load_students()
    )

    load_students()


# =================================================
# STUDENT DASHBOARD
# =================================================

def student_dashboard(
    student_id,
    student_name,
    login_window
):

    window = Toplevel(login_window)

    window.title("Student Dashboard")
    window.geometry("800x1000")
    window.config(bg="#E8F6F7")

    Label(
        window,
        text="STUDENT DASHBOARD",
        font=("Arial", 22, "bold"),
        bg="#E8F6F7",
        fg="#0E878E"
    ).pack(pady=20)

    try:

        db = connect_database()
        cursor = db.cursor()

        cursor.execute(
            """
            SELECT
                name,
                standard,
                phone,
                email,
                address,
                tamil,
                english,
                maths,
                science,
                social
            FROM students
            WHERE id = %s
            """,
            (student_id,)
        )

        student = cursor.fetchone()
        db.close()

    except mysql.connector.Error as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )

        window.destroy()
        return

    if not student:

        messagebox.showerror(
            "Error",
            "Student details not found"
        )

        window.destroy()
        return

    details = Frame(
        window,
        bg="white",
        bd=1,
        relief="solid"
    )

    details.pack(
        padx=40,
        pady=10,
        fill="x"
    )

    Label(
        details,
        text="PERSONAL DETAILS",
        font=("Arial", 14, "bold"),
        bg="white",
        fg="#0E878E"
    ).pack(pady=10)

    details_text = (

        "Name : " +
        str(student[0]) +

        "\nClass / Standard : " +
        str(student[1] or "-") +

        "\nPhone : " +
        str(student[2] or "-") +

        "\nEmail : " +
        str(student[3] or "-") +

        "\nAddress : " +
        str(student[4] or "-")

    )

    Label(
        details,
        text=details_text,
        justify=LEFT,
        bg="white",
        font=("Arial", 11)
    ).pack(
        padx=20,
        pady=10
    )

    tamil = student[5] or 0
    english = student[6] or 0
    maths = student[7] or 0
    science = student[8] or 0
    social = student[9] or 0

    total = (
        tamil +
        english +
        maths +
        science +
        social
    )

    percentage = (
        total / 500
    ) * 100

    marks_frame = Frame(
        window,
        bg="white",
        bd=1,
        relief="solid"
    )

    marks_frame.pack(
        padx=40,
        pady=15,
        fill="x"
    )

    Label(
        marks_frame,
        text="MY MARKS",
        font=("Arial", 14, "bold"),
        bg="white",
        fg="#0E878E"
    ).pack(pady=10)

    marks = (

        "Tamil     : " +
        str(tamil) +

        "\nEnglish   : " +
        str(english) +

        "\nMaths     : " +
        str(maths) +

        "\nScience   : " +
        str(science) +

        "\nSocial    : " +
        str(social) +

        "\n\nTOTAL MARKS : " +
        str(total) +
        " / 500" +

        "\nOVERALL PERCENTAGE : " +
        f"{percentage:.2f}%"

    )

    Label(
        marks_frame,
        text=marks,
        justify=LEFT,
        bg="white",
        font=("Arial", 12)
    ).pack(
        padx=20,
        pady=10
    )

    def back_to_login():

        window.destroy()
        login_window.deiconify()

    Button(
        window,
        text="BACK TO LOGIN",
        width=20,
        bg="#DC3545",
        fg="white",
        font=("Arial", 10, "bold"),
        command=back_to_login
    ).pack(pady=15)
