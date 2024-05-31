import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import firebase_admin
from firebase_admin import credentials, firestore, storage
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Initialize Firebase
cred = credentials.Certificate('path/to/your/GoogleService-Info.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'your-project-id.appspot.com'
})
db = firestore.client()
bucket = storage.bucket()

class ToDoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Javis")
        self.geometry("400x600")

        self.current_theme = 'Light Mode'
        self.current_security = 'None'
        self.pin_code = None

        self.theme_colors = {
            'Light Mode': {'bg': 'white', 'fg': 'black'},
            'Dark Mode': {'bg': 'gray20', 'fg': 'white'},
            'AMOLED Dark Mode': {'bg': 'black', 'fg': 'white'},
            'Blue on White': {'bg': 'white', 'fg': 'blue'},
            'Pink on White': {'bg': 'white', 'fg': 'hot pink'},
            'Yellow on Black': {'bg': 'black', 'fg': 'yellow'},
            'Blue on Black': {'bg': 'black', 'fg': 'blue'},
        }

        self.configure(bg=self.theme_colors[self.current_theme]['bg'])

        self.task_listbox = tk.Listbox(self, bg=self.theme_colors[self.current_theme]['bg'], fg=self.theme_colors[self.current_theme]['fg'])
        self.task_listbox.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        self.task_listbox.bind('<Double-Button-1>', self.show_context_menu)

        self.task_input = tk.Entry(self, width=30, bg=self.theme_colors[self.current_theme]['bg'], fg=self.theme_colors[self.current_theme]['fg'])
        self.task_input.pack(pady=5)

        self.add_task_button = tk.Button(self, text="Add Task", command=self.add_task)
        self.add_task_button.pack(pady=5)

        self.theme_spinner = tk.OptionMenu(self, tk.StringVar(value="Light Mode"), *self.theme_colors.keys(), command=self.change_theme)
        self.theme_spinner.pack(pady=5)

        self.security_spinner = tk.OptionMenu(self, tk.StringVar(value="None"), "None", "PIN", "Face ID", command=self.change_security)
        self.security_spinner.pack(pady=5)

        self.save_button = tk.Button(self, text="Save to Cloud", command=self.save_to_cloud)
        self.save_button.pack(pady=5)

        self.export_button = tk.Button(self, text="Export as PDF", command=self.export_to_pdf)
        self.export_button.pack(pady=5)

        self.check_security()

    def add_task(self):
        task_text = self.task_input.get()
        if task_text:
            self.task_listbox.insert(tk.END, task_text)
            self.task_input.delete(0, tk.END)

    def change_theme(self, theme_name):
        self.current_theme = theme_name
        self.configure(bg=self.theme_colors[theme_name]['bg'])
        self.task_listbox.configure(bg=self.theme_colors[theme_name]['bg'], fg=self.theme_colors[theme_name]['fg'])
        self.task_input.configure(bg=self.theme_colors[theme_name]['bg'], fg=self.theme_colors[theme_name]['fg'])

    def change_security(self, security_type):
        self.current_security = security_type
        if security_type == 'PIN':
            self.set_pin_code()
        self.check_security()

    def set_pin_code(self):
        self.pin_code = simpledialog.askstring("Set PIN", "Enter a 6-digit PIN", show='*')

    def check_security(self):
        if self.current_security == 'Face ID':
            self.authenticate_face_id()
        elif self.current_security == 'PIN':
            self.authenticate_pin()
        # No security does not require authentication

    def authenticate_face_id(self):
        messagebox.showerror("Error", "Face ID Authentication is not supported yet.")

    def authenticate_pin(self):
        pin = simpledialog.askstring("Enter PIN", "Enter your 6-digit PIN", show='*')
        if pin != self.pin_code:
            messagebox.showerror("Error", "Incorrect PIN")

    def show_context_menu(self, event):
        context_menu = tk.Menu(self, tearoff=0)
        context_menu.add_command(label="Delete", command=lambda: self.delete_task(event))
        context_menu.add_command(label="Modify", command=lambda: self.modify_task(event))
        context_menu.add_command(label="Mark as Done", command=lambda: self.mark_task_done(event))
        context_menu.tk_popup(event.x_root, event.y_root)

    def delete_task(self, event):
        selected_task_index = self.task_listbox.nearest(event.y)
        self.task_listbox.delete(selected_task_index)

    def modify_task(self, event):
        selected_task_index = self.task_listbox.nearest(event.y)
        selected_task = self.task_listbox.get(selected_task_index)
        new_text = simpledialog.askstring("Modify Task", "Enter new task text", initialvalue=selected_task)
        if new_text:
            self.task_listbox.delete(selected_task_index)
            self.task_listbox.insert(selected_task_index, new_text)

    def mark_task_done(self, event):
        selected_task_index = self.task_listbox.nearest(event.y)
        selected_task = self.task_listbox.get(selected_task_index)
        self.task_listbox.delete(selected_task_index)
        self.task_listbox.insert(selected_task_index, f"[Done] {selected_task}")

    def save_to_cloud(self):
        tasks = [self.task_listbox.get(idx) for idx in range(self.task_listbox.size())]
        task_data = {'tasks': tasks}
        db.collection('todos').document('my_todo_list').set(task_data)
        messagebox.showinfo("Info", "Tasks saved to cloud!")

    def export_to_pdf(self):
        tasks = [self.task_listbox.get(idx) for idx in range(self.task_listbox.size())]
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if file_path:
            pdf = canvas.Canvas(file_path, pagesize=letter)
            width, height = letter

            pdf.drawString(100, height - 100, "To-Do List")

            for i, task in enumerate(tasks):
                pdf.drawString(100, height - 130 - i * 20, task)

            pdf.save()
            messagebox.showinfo("Info", "Tasks exported to PDF!")

if __name__ == '__main__':
    app = ToDoApp()
    app.mainloop()
