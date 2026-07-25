import tkinter as tk
from tkinter import messagebox
import json

FILE_NAME = "tasks.json"


# ---------- TASK CLASS ----------

class Task:

    def __init__(
        self,
        title,
        description,
        category,
        priority,
        completed=False
    ):

        self.title = title

        self.description = description

        self.category = category

        self.priority = priority

        self.completed = completed


# ---------- FILE HANDLING ----------

def save_tasks():

    with open(
        FILE_NAME,
        "w"
    ) as file:

        json.dump(

            [task.__dict__
             for task in tasks],

            file,

            indent=4

        )


def load_tasks():

    try:

        with open(
            FILE_NAME,
            "r"
        ) as file:

            data = json.load(file)

            loaded_tasks = []

            for item in data:

                task = Task(

                    item["title"],

                    item["description"],

                    item["category"],

                    item.get(
                        "priority",
                        "Medium"
                    ),

                    item.get(
                        "completed",
                        False
                    )

                )

                loaded_tasks.append(
                    task
                )

            return loaded_tasks

    except FileNotFoundError:

        return []


# ---------- FUNCTIONS ----------

def refresh_tasks():

    task_list.delete(
        0,
        tk.END
    )

    for index, task in enumerate(
        tasks
    ):

        status = (

            "Completed"

            if task.completed

            else "Pending"

        )

        task_list.insert(

            tk.END,

            f"{index+1}. "

            f"{task.title} | "

            f"{task.category} | "

            f"{task.priority} | "

            f"{status}"

        )


def add_task():

    title = title_entry.get()

    description = description_entry.get()

    category = category_entry.get()

    priority = priority_var.get()

    if title == "":

        messagebox.showwarning(

            "Warning",

            "Enter title"

        )

        return

    task = Task(

        title,

        description,

        category,

        priority

    )

    tasks.append(
        task
    )

    save_tasks()

    refresh_tasks()

    clear_entries()

    messagebox.showinfo(

        "Success",

        "Task Added"

    )


def complete_task():

    selected = task_list.curselection()

    if not selected:

        messagebox.showwarning(

            "Warning",

            "Select a task"

        )

        return

    index = selected[0]

    tasks[index].completed = True

    save_tasks()

    refresh_tasks()

    messagebox.showinfo(

        "Success",

        "Task Completed"

    )


def delete_task():

    selected = task_list.curselection()

    if not selected:

        messagebox.showwarning(

            "Warning",

            "Select a task"

        )

        return

    index = selected[0]

    tasks.pop(index)

    save_tasks()

    refresh_tasks()

    messagebox.showinfo(

        "Success",

        "Task Deleted"

    )


def clear_entries():

    title_entry.delete(
        0,
        tk.END
    )

    description_entry.delete(
        0,
        tk.END
    )

    category_entry.delete(
        0,
        tk.END
    )

    priority_var.set(
        "Medium"
    )


# ---------- MAIN WINDOW ----------

tasks = load_tasks()

root = tk.Tk()

root.title(
    "Personal To Do List Application"
)

root.geometry(
    "700x600"
)


heading = tk.Label(

    root,

    text="Personal To Do List Application",

    font=(

        "Arial",

        18,

        "bold"

    )

)

heading.pack(
    pady=10
)


# Title

tk.Label(

    root,

    text="Title"

).pack()

title_entry = tk.Entry(

    root,

    width=40

)

title_entry.pack()


# Description

tk.Label(

    root,

    text="Description"

).pack()

description_entry = tk.Entry(

    root,

    width=40

)

description_entry.pack()


# Category

tk.Label(

    root,

    text="Category"

).pack()

category_entry = tk.Entry(

    root,

    width=40

)

category_entry.pack()


# Priority

tk.Label(

    root,

    text="Priority"

).pack()

priority_var = tk.StringVar()

priority_var.set(
    "Medium"
)

priority_menu = tk.OptionMenu(

    root,

    priority_var,

    "Low",

    "Medium",

    "High"

)

priority_menu.pack()


# Buttons

tk.Button(

    root,

    text="Add Task",

    width=20,

    command=add_task

).pack(
    pady=5
)


tk.Button(

    root,

    text="Mark Completed",

    width=20,

    command=complete_task

).pack(
    pady=5
)


tk.Button(

    root,

    text="Delete Task",

    width=20,

    command=delete_task

).pack(
    pady=5
)


# Task list

task_list = tk.Listbox(

    root,

    width=70,

    height=12

)

task_list.pack(
    pady=15
)


refresh_tasks()

root.mainloop()