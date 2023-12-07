import tkinter as tk
from tkinter import filedialog, simpledialog
import os


class DialogFactory:
    @staticmethod
    def create_folder_dialog(parent):
        return CreateFolderDialog(parent)


class CreateFolderDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.folder_path = None
        self.title("Escolha ou crie uma pasta")
        self.geometry("400x150")
        tk.Button(self, text="Escolher Pasta", command=self.choose_folder).pack(pady=10)
        tk.Button(self, text="Criar Nova Pasta", command=self.create_folder).pack(
            pady=10
        )

    def choose_folder(self):
        self.folder_path = filedialog.askdirectory(parent=self)
        self.close_dialog()

    def create_folder(self):
        new_folder_name = simpledialog.askstring(
            "Nova Pasta", "Nome da Pasta:", parent=self
        )
        if new_folder_name:
            initial_dir = filedialog.askdirectory(parent=self)
            if initial_dir:
                new_folder_path = os.path.join(initial_dir, new_folder_name)
                os.makedirs(new_folder_path, exist_ok=True)
                self.folder_path = new_folder_path
                self.close_dialog()

    def close_dialog(self):
        self.destroy()
