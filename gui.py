"""Графический интерфейс приложения "Менеджер задач" на Tkinter."""

import tkinter as tk
from tkinter import ttk, messagebox

from classes import Task, TaskManager

# Календарь берём из tkcalendar (виджет на базе ttk).
# Если библиотека не установлена, используем обычное поле Entry.
try:
    from tkcalendar import DateEntry
    HAS_CALENDAR = True
except ImportError:
    HAS_CALENDAR = False


COLORS = {
    "window": "#0f1117",
    "surface": "#171a23",
    "surface_alt": "#1f2430",
    "field": "#232936",
    "border": "#2c3345",
    "text": "#e8ebf5",
    "muted": "#98a0b8",
    "accent": "#7c5cff",
    "accent_hover": "#9a82ff",
    "accent_pressed": "#6a4ae0",
    "selection": "#3b3178",
    "red": "#ff6b81",
    "danger_bg": "#3a2430",
    "danger_hover": "#4a2a38",
}

FONT = ("Segoe UI", 10)
FONT_MEDIUM = ("Segoe UI", 11)
FONT_BOLD = ("Segoe UI", 10, "bold")
FONT_TITLE = ("Segoe UI", 24, "bold")
FONT_SUBTITLE = ("Segoe UI", 10)
FONT_SECTION = ("Segoe UI", 12, "bold")


class TaskManagerApp:
    """Главное окно приложения."""

    def __init__(self, root):
        self.manager = TaskManager()
        self.root = root
        self.root.title("TaskFlow")
        self.root.geometry("1000x720")
        self.root.minsize(860, 620)
        self.root.configure(bg=COLORS["window"])
        self.setup_styles()
        self.setup_ui()
        self.center_window()

    def center_window(self):
        """Размещает окно по центру экрана."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = max((self.root.winfo_screenwidth() - width) // 2, 0)
        y = max((self.root.winfo_screenheight() - height) // 2, 0)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def setup_styles(self):
        """Настраивает стили ttk-виджетов под тёмную тему."""
        style = ttk.Style()
        style.theme_use("clam")

        # Этот стиль использует и выпадающий календарь tkcalendar:
        # DateEntry копирует оформление TCombobox.
        style.configure(
            "TCombobox",
            background=COLORS["field"],
            foreground=COLORS["text"],
            fieldbackground=COLORS["field"],
            insertcolor=COLORS["text"],
            arrowcolor=COLORS["text"],
            bordercolor=COLORS["border"],
            lightcolor=COLORS["border"],
            darkcolor=COLORS["border"],
            font=FONT_MEDIUM,
        )
        style.map(
            "TCombobox",
            fieldbackground=[
                ("readonly", COLORS["field"]),
                ("disabled", COLORS["field"]),
            ],
            foreground=[
                ("readonly", COLORS["text"]),
                ("disabled", COLORS["muted"]),
            ],
            selectbackground=[("readonly", COLORS["field"])],
            selectforeground=[("readonly", COLORS["text"])],
            background=[
                ("readonly", COLORS["field"]),
                ("active", COLORS["field"]),
                ("pressed", COLORS["field"]),
            ],
            arrowcolor=[("disabled", COLORS["muted"])],
            bordercolor=[("focus", COLORS["accent"])],
            lightcolor=[("focus", COLORS["accent"])],
            darkcolor=[("focus", COLORS["accent"])],
        )

        style.configure(
            "Treeview",
            background=COLORS["surface_alt"],
            fieldbackground=COLORS["surface_alt"],
            foreground=COLORS["text"],
            rowheight=34,
            font=FONT_MEDIUM,
            borderwidth=0,
            bordercolor=COLORS["border"],
            lightcolor=COLORS["border"],
            darkcolor=COLORS["border"],
        )
        style.map(
            "Treeview",
            background=[("selected", COLORS["selection"])],
            foreground=[("selected", "#ffffff")],
        )
        style.configure(
            "Treeview.Heading",
            background=COLORS["surface"],
            foreground=COLORS["muted"],
            font=FONT_BOLD,
            relief="flat",
            padding=(10, 8),
            borderwidth=0,
        )
        style.map(
            "Treeview.Heading",
            background=[("active", COLORS["surface_alt"])],
        )

        style.configure(
            "TScrollbar",
            background=COLORS["field"],
            troughcolor=COLORS["surface_alt"],
            bordercolor=COLORS["surface_alt"],
            arrowcolor=COLORS["muted"],
            lightcolor=COLORS["field"],
            darkcolor=COLORS["field"],
        )

    def setup_ui(self):
        # Шапка
        header = tk.Frame(self.root, bg=COLORS["window"])
        header.pack(fill="x", padx=24, pady=(20, 16))
        tk.Label(
            header,
            text="TaskFlow",
            bg=COLORS["window"],
            fg=COLORS["text"],
            font=FONT_TITLE,
        ).pack(anchor="w")
        tk.Label(
            header,
            text="Планируйте задачи и держите всё под контролем",
            bg=COLORS["window"],
            fg=COLORS["muted"],
            font=FONT_SUBTITLE,
        ).pack(anchor="w", pady=(2, 0))
        tk.Frame(
            header, bg=COLORS["accent"], height=2, width=52
        ).pack(anchor="w", pady=(10, 0))

        # Карточка формы
        form_card = tk.Frame(
            self.root,
            bg=COLORS["surface"],
            highlightbackground=COLORS["border"],
            highlightthickness=1,
            bd=0,
        )
        form_card.pack(fill="x", padx=24, pady=(0, 14))

        form = tk.Frame(form_card, bg=COLORS["surface"])
        form.pack(fill="x", padx=18, pady=16)
        form.columnconfigure(1, weight=1)

        tk.Label(
            form,
            text="Новая задача",
            bg=COLORS["surface"],
            fg=COLORS["text"],
            font=FONT_SECTION,
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 12))

        tk.Label(
            form,
            text="Название",
            bg=COLORS["surface"],
            fg=COLORS["muted"],
            font=FONT_BOLD,
            anchor="w",
        ).grid(row=1, column=0, sticky="w", padx=(0, 14), pady=(0, 10))

        self.title_entry = tk.Entry(
            form,
            bg=COLORS["field"],
            fg=COLORS["text"],
            insertbackground=COLORS["text"],
            selectbackground=COLORS["selection"],
            selectforeground="#ffffff",
            relief="flat",
            bd=4,
            highlightthickness=1,
            highlightbackground=COLORS["border"],
            highlightcolor=COLORS["accent"],
            font=FONT_MEDIUM,
        )
        self.title_entry.grid(row=1, column=1, sticky="ew", pady=(0, 10))

        tk.Label(
            form,
            text="Описание",
            bg=COLORS["surface"],
            fg=COLORS["muted"],
            font=FONT_BOLD,
            anchor="nw",
        ).grid(row=2, column=0, sticky="nw", padx=(0, 14), pady=(0, 10))

        self.desc_text = tk.Text(
            form,
            height=3,
            wrap="word",
            bg=COLORS["field"],
            fg=COLORS["text"],
            insertbackground=COLORS["text"],
            selectbackground=COLORS["selection"],
            selectforeground="#ffffff",
            relief="flat",
            bd=0,
            highlightthickness=1,
            highlightbackground=COLORS["border"],
            highlightcolor=COLORS["accent"],
            font=FONT_MEDIUM,
            padx=8,
            pady=6,
        )
        self.desc_text.grid(row=2, column=1, sticky="ew", pady=(0, 10))

        tk.Label(
            form,
            text="Срок выполнения",
            bg=COLORS["surface"],
            fg=COLORS["muted"],
            font=FONT_BOLD,
            anchor="w",
        ).grid(row=3, column=0, sticky="w", padx=(0, 14), pady=(0, 10))

        if HAS_CALENDAR:
            self.date_entry = DateEntry(
                form,
                width=16,
                date_pattern="yyyy-mm-dd",
                font=FONT_MEDIUM,
                borderwidth=0,
                background=COLORS["surface_alt"],
                foreground=COLORS["text"],
                headersbackground=COLORS["surface"],
                headersforeground=COLORS["muted"],
                selectbackground=COLORS["accent"],
                selectforeground="#ffffff",
                normalbackground=COLORS["surface_alt"],
                normalforeground=COLORS["text"],
                weekendbackground=COLORS["surface_alt"],
                weekendforeground=COLORS["red"],
                othermonthbackground=COLORS["surface"],
                othermonthforeground=COLORS["muted"],
                othermonthwebackground=COLORS["surface"],
                othermonthweforeground=COLORS["muted"],
                bordercolor=COLORS["border"],
            )
        else:
            self.date_entry = tk.Entry(
                form,
                bg=COLORS["field"],
                fg=COLORS["text"],
                insertbackground=COLORS["text"],
                selectbackground=COLORS["selection"],
                selectforeground="#ffffff",
                relief="flat",
                bd=4,
                highlightthickness=1,
                highlightbackground=COLORS["border"],
                highlightcolor=COLORS["accent"],
                font=FONT_MEDIUM,
            )
        self.date_entry.grid(row=3, column=1, sticky="w", pady=(0, 10))

        actions = tk.Frame(form, bg=COLORS["surface"])
        actions.grid(row=4, column=0, columnspan=2, sticky="e", pady=(6, 0))

        self.delete_button = tk.Button(
            actions,
            text="Удалить задачу",
            command=self.delete_task,
            bg=COLORS["danger_bg"],
            fg=COLORS["red"],
            activebackground=COLORS["danger_hover"],
            activeforeground=COLORS["red"],
            relief="flat",
            bd=0,
            highlightthickness=0,
            padx=16,
            pady=8,
            cursor="hand2",
            font=FONT_BOLD,
        )
        self.delete_button.pack(side="left", padx=(0, 10))

        self.add_button = tk.Button(
            actions,
            text="Добавить задачу",
            command=self.add_task,
            bg=COLORS["accent"],
            fg="#ffffff",
            activebackground=COLORS["accent_hover"],
            activeforeground="#ffffff",
            relief="flat",
            bd=0,
            highlightthickness=0,
            padx=18,
            pady=8,
            cursor="hand2",
            font=FONT_BOLD,
        )
        self.add_button.pack(side="left")

        # Карточка списка
        list_card = tk.Frame(
            self.root,
            bg=COLORS["surface"],
            highlightbackground=COLORS["border"],
            highlightthickness=1,
            bd=0,
        )
        list_card.pack(fill="both", expand=True, padx=24, pady=(0, 24))

        list_header = tk.Frame(list_card, bg=COLORS["surface"])
        list_header.pack(fill="x", padx=18, pady=(16, 10))
        tk.Label(
            list_header,
            text="Список задач",
            bg=COLORS["surface"],
            fg=COLORS["text"],
            font=FONT_SECTION,
        ).pack(side="left")
        self.count_label = tk.Label(
            list_header,
            text="",
            bg=COLORS["surface"],
            fg=COLORS["muted"],
            font=FONT,
        )
        self.count_label.pack(side="right")

        list_body = tk.Frame(list_card, bg=COLORS["surface"])
        list_body.pack(fill="both", expand=True, padx=18, pady=(0, 18))

        self.task_tree = ttk.Treeview(
            list_body,
            columns=("title", "due", "description"),
            show="headings",
            selectmode="browse",
        )
        self.task_tree.heading("title", text="Задача", anchor="w")
        self.task_tree.heading("due", text="Срок", anchor="center")
        self.task_tree.heading("description", text="Описание", anchor="w")

        self.task_tree.column(
            "title", width=300, minwidth=180, anchor="w", stretch=True
        )
        self.task_tree.column(
            "due", width=120, minwidth=100, anchor="center", stretch=False
        )
        self.task_tree.column(
            "description", width=360, minwidth=200, anchor="w", stretch=True
        )

        self.tasks_scrollbar = ttk.Scrollbar(
            list_body, orient="vertical", command=self.task_tree.yview
        )
        self.task_tree.configure(yscrollcommand=self.tasks_scrollbar.set)
        self.tasks_scrollbar.pack(side="right", fill="y")
        self.task_tree.pack(side="left", fill="both", expand=True)

        self.update_task_list()

    def add_task(self):
        """Создаёт задачу из полей ввода и добавляет её в менеджер."""
        title = self.title_entry.get()
        description = self.desc_text.get("1.0", tk.END).strip()
        due_date = self.date_entry.get()
        if title and description and due_date:
            task = Task(title, description, due_date)
            self.manager.add_task(task)
            self.update_task_list()
            self.clear_inputs()
        else:
            messagebox.showwarning("Ошибка", "Заполните все поля!")

    def delete_task(self):
        """Удаляет выбранную в списке задачу."""
        selected = self.task_tree.selection()
        if selected:
            index = self.task_tree.index(selected[0])
            self.manager.delete_task(index)
            self.update_task_list()
        else:
            messagebox.showinfo("Информация", "Выберите задачу для удаления.")

    def update_task_list(self):
        """Перерисовывает список задач."""
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)

        for task in self.manager.tasks:
            self.task_tree.insert(
                "",
                tk.END,
                values=(
                    task.title,
                    task.due_date,
                    " ".join(task.description.split()),
                ),
            )

        count = len(self.manager.tasks)
        self.count_label.config(
            text="Пока нет задач" if count == 0 else f"Всего задач: {count}"
        )

    def clear_inputs(self):
        """Очищает поля формы после добавления задачи."""
        self.title_entry.delete(0, tk.END)
        self.desc_text.delete("1.0", tk.END)
        if not HAS_CALENDAR:
            self.date_entry.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()
