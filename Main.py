import tkinter as tk
from tkinter import ttk, messagebox
import json

class ToDoListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App")

        self.tasks = []
        self.task_listbox = None  # Initialize task_listbox
        
        self.create_ui()
        self.load_tasks()

    def create_ui(self):
        # Create a notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create different tabs
        self.task_tab = ttk.Frame(self.notebook)
        self.stats_tab = ttk.Frame(self.notebook)
        self.settings_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.task_tab, text="Tasks")
        self.notebook.add(self.stats_tab, text="Statistics")
        self.notebook.add(self.settings_tab, text="Settings")

        # Task Tab
        self.create_task_tab()

        # Statistics Tab
        self.create_stats_tab()

        # Settings Tab
        self.create_settings_tab()

    def create_task_tab(self):
        # Task Entry
        task_frame = ttk.Frame(self.task_tab)
        task_frame.pack(pady=10, padx=10)

        self.task_name_var = tk.StringVar()
        task_entry = ttk.Entry(
            task_frame, textvariable=self.task_name_var, width=50)
        task_entry.grid(row=0, column=0, padx=5, pady=5)

        self.task_listbox = tk.Listbox(self.task_tab, selectmode=tk.SINGLE, bg="white", width=60)
        self.task_listbox.pack(pady=10, fill=tk.BOTH, expand=True)
        
        # Priority Level
        priority_label = ttk.Label(task_frame, text="Priority:")
        priority_label.grid(row=0, column=1, padx=5, pady=5)
        self.priority_var = tk.StringVar()
        priority_combo = ttk.Combobox(
            task_frame, textvariable=self.priority_var, values=("High", "Medium", "Low"))
        priority_combo.grid(row=0, column=2, padx=5, pady=5)
        priority_combo.set("Medium")

        # Due Date
        due_date_label = ttk.Label(task_frame, text="Due Date:")
        due_date_label.grid(row=0, column=3, padx=5, pady=5)
        self.due_date_var = tk.StringVar()
        due_date_entry = ttk.Entry(
            task_frame, textvariable=self.due_date_var, width=12)
        due_date_entry.grid(row=0, column=4, padx=5, pady=5)

        # Category
        category_label = ttk.Label(task_frame, text="Category:")
        category_label.grid(row=0, column=5, padx=5, pady=5)
        self.category_var = tk.StringVar()
        category_entry = ttk.Entry(
            task_frame, textvariable=self.category_var, width=15)
        category_entry.grid(row=0, column=6, padx=5, pady=5)

        # Add Button
        add_button = ttk.Button(
            task_frame, text="Add Task", command=self.add_task)
        add_button.grid(row=0, column=7, padx=5, pady=5)

        # Task List
        self.task_listbox = tk.Listbox(
            self.task_tab, selectmode=tk.SINGLE, bg="white", width=60)
        self.task_listbox.pack(pady=10, fill=tk.BOTH, expand=True)

        # Create buttons for task actions
        button_frame = ttk.Frame(self.task_tab)
        button_frame.pack(pady=10)

        remove_button = ttk.Button(
            button_frame, text="Remove Task", command=self.remove_task)
        remove_button.pack(side=tk.LEFT, padx=5, pady=5)

        edit_button = ttk.Button(
            button_frame, text="Edit Task", command=self.edit_task)
        edit_button.pack(side=tk.LEFT, padx=5, pady=5)

        save_button = ttk.Button(
            button_frame, text="Save Tasks", command=self.save_tasks)
        save_button.pack(side=tk.LEFT, padx=5, pady=5)

    def create_stats_tab(self):
        # Placeholder for statistics tab
        ttk.Label(self.stats_tab,
                  text="Statistics will be shown here.").pack(pady=20)

    def create_settings_tab(self):
        # Placeholder for settings tab
        ttk.Label(self.settings_tab,
                  text="Settings will be available here.").pack(pady=20)

    def add_task(self):
        task_name = self.task_name_var.get()
        task_priority = self.priority_var.get()
        task_due_date = self.due_date_var.get()

        if task_name:
            simplified_task = {
                "name": task_name,
                "priority": task_priority,
                "due_date": task_due_date
            }
            self.task_listbox.insert(tk.END, simplified_task)
            self.clear_task_entry()
        else:
            messagebox.showwarning("Warning", "You must enter a task name!")

    def remove_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            self.task_listbox.delete(selected_task_index)
        else:
            messagebox.showwarning(
                "Warning", "You must select a task to remove!")

    def edit_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            selected_task_data_str = self.task_listbox.get(selected_task_index[0])

            try:
                # Try to parse the selected_task_data_str into a dictionary
                selected_task_data = json.loads(selected_task_data_str)

                self.edit_window = tk.Toplevel(self.root)
                self.edit_window.title("Edit Task")

                # Create entry fields for editing
                edited_name_var = tk.StringVar(value=selected_task_data["name"])
                edited_priority_var = tk.StringVar(
                    value=selected_task_data["priority"])
                edited_due_date_var = tk.StringVar(
                    value=selected_task_data["due_date"])

                name_label = ttk.Label(self.edit_window, text="Name:")
                name_label.pack()
                edited_name_entry = ttk.Entry(
                    self.edit_window, textvariable=edited_name_var, width=50)
                edited_name_entry.pack()

                priority_label = ttk.Label(self.edit_window, text="Priority:")
                priority_label.pack()
                edited_priority_combo = ttk.Combobox(
                    self.edit_window, textvariable=edited_priority_var, values=("High", "Medium", "Low"))
                edited_priority_combo.pack()

                due_date_label = ttk.Label(self.edit_window, text="Due Date:")
                due_date_label.pack()
                edited_due_date_entry = ttk.Entry(
                    self.edit_window, textvariable=edited_due_date_var, width=12)
                edited_due_date_entry.pack()

                # Define the update_task function
                def update_task():
                    updated_task = {
                        "name": edited_name_var.get(),
                        "priority": edited_priority_var.get(),
                        "due_date": edited_due_date_var.get()
                    }

                    self.task_listbox.delete(selected_task_index)
                    self.task_listbox.insert(selected_task_index[0], json.dumps(
                        updated_task))  # Convert back to JSON string
                    self.edit_window.destroy()

                # Create an "Update" button to save changes
                update_button = ttk.Button(
                    self.edit_window, text="Update", command=update_task)
                update_button.pack(pady=10)
            except json.JSONDecodeError:
                messagebox.showerror("Error", "Invalid task data format")
        else:
            messagebox.showwarning("Warning", "You must select a task to edit!")


    def save_tasks(self):
        tasks_to_save = [self.task_listbox.get(
            i) for i in range(self.task_listbox.size())]

        with open("tasks.json", "w") as file:
            json.dump(tasks_to_save, file)
            
    def load_tasks(self):
        try:
            with open("tasks.json", "r") as file:
                tasks = json.load(file)
                for task in tasks:
                    self.task_listbox.insert(tk.END, task)
        except FileNotFoundError:
            pass

    def clear_task_entry(self):
        self.task_name_var.set("")
        self.priority_var.set("Medium")
        self.due_date_var.set("")
        self.category_var.set("")


if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoListApp(root)
    root.mainloop()
