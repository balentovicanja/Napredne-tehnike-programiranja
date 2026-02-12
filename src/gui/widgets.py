"""
GUI komponente za aplikaciju 
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from decimal import Decimal
from src.models import TransactionStats


class TransactionDialog(tk.Toplevel):
    
    def __init__(
        self,
        parent: tk.Tk,
        title: str = "Nova transakcija",
        initial_data: dict | None = None
    ):
        
        super().__init__(parent)
        self.title(title)
        self.geometry("400x350")
        self.transient(parent)
        self.grab_set()
        
        self.result = None
        self.initial_data = initial_data or {}
        
        self._build_form()
    
    # Forma unosa
    def _build_form(self) -> None:
    
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Iznos
        ttk.Label(main_frame, text="Iznos:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.amount_var = tk.StringVar(value=str(self.initial_data.get('amount', '')))
        ttk.Entry(main_frame, textvariable=self.amount_var).grid(row=0, column=1, sticky=tk.EW, pady=5)
        
        # Tip transakcije
        ttk.Label(main_frame, text="Tip:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.type_var = tk.StringVar(value=self.initial_data.get('type', 'expense'))
        type_frame = ttk.Frame(main_frame)
        type_frame.grid(row=1, column=1, sticky=tk.EW, pady=5)
        ttk.Radiobutton(type_frame, text="Trošak", variable=self.type_var, value="expense").pack(side=tk.LEFT)
        ttk.Radiobutton(type_frame, text="Prihod", variable=self.type_var, value="income").pack(side=tk.LEFT)
        
        # Kategorija
        ttk.Label(main_frame, text="Kategorija:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.category_var = tk.StringVar(value=self.initial_data.get('category', ''))
        categories = ["Hrana", "Transport", "Zabava", "Stanovanje", "Zdravstvo", "Obrazovanje", "Plaća", "Ostalo"]
        category_combo = ttk.Combobox(main_frame, textvariable=self.category_var, values=categories, state="readonly")
        category_combo.grid(row=2, column=1, sticky=tk.EW, pady=5)
        
        # Datum
        ttk.Label(main_frame, text="Datum:").grid(row=3, column=0, sticky=tk.W, pady=5)
        date_str = self.initial_data.get('date', datetime.now())
        if isinstance(date_str, datetime):
            date_str = date_str.strftime("%Y-%m-%d")
        self.date_var = tk.StringVar(value=date_str)
        ttk.Entry(main_frame, textvariable=self.date_var).grid(row=3, column=1, sticky=tk.EW, pady=5)
        
        # Opis
        ttk.Label(main_frame, text="Opis:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.description_var = tk.StringVar(value=self.initial_data.get('description', ''))
        ttk.Entry(main_frame, textvariable=self.description_var).grid(row=4, column=1, sticky=tk.EW, pady=5)
        
        main_frame.columnconfigure(1, weight=1)
        
        # Gumbi
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, sticky=tk.EW, pady=10)
        
        ttk.Button(button_frame, text="Spremi", command=self._on_submit).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Odustani", command=self.destroy).pack(side=tk.LEFT, padx=5)
    
    # Unos
    def _on_submit(self) -> None:
        if not self.amount_var.get() or not self.category_var.get() or not self.description_var.get():
            messagebox.showerror("Greška", "Popunite sva polja")
            return
        
        try:
            self.result = {
                'amount': Decimal(self.amount_var.get()),
                'type': self.type_var.get(),
                'category': self.category_var.get(),
                'date': datetime.strptime(self.date_var.get(), "%Y-%m-%d"),
                'description': self.description_var.get()
            }
            self.destroy()
        except ValueError as e:
            messagebox.showerror("Greška", f"Neispravni unos: {e}")


# Okvir za prikaz statistike
class StatsFrame(ttk.Frame):
    
    def __init__(self, parent: tk.Widget):
    
        super().__init__(parent)
        self.stats_labels: dict[str, ttk.Label] = {}
        self._build()
    
    def _build(self) -> None:
        self.configure(padding="10", relief=tk.SUNKEN, borderwidth=2)
        
        # Naslov
        title = ttk.Label(self, text="Statistika", font=("Arial", 12, "bold"))
        title.pack(fill=tk.X, pady=(0, 10))
        
        # Grid sa statistikom
        stats = [
            ("Prihodi:", "income"),
            ("Troškovi:", "expense"),
            ("Bilanca:", "balance"),
            ("Br. transakcija:", "count")
        ]
        
        for label_text, key in stats:
            row = ttk.Frame(self)
            row.pack(fill=tk.X, pady=5)
            
            label = ttk.Label(row, text=label_text, width=15)
            label.pack(side=tk.LEFT)
            
            value_label = ttk.Label(row, text="0", font=("Arial", 11, "bold"))
            value_label.pack(side=tk.LEFT, padx=(20, 0))
            
            self.stats_labels[key] = value_label


    def update_stats(self, stats: TransactionStats) -> None:
        self.stats_labels["income"].config(text=f"{stats.total_income} EUR")
        self.stats_labels["expense"].config(text=f"{stats.total_expense} EUR")
        self.stats_labels["balance"].config(text=f"{stats.balance} EUR")
        self.stats_labels["count"].config(text=str(stats.transaction_count))
