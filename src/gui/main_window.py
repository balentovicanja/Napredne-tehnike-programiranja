"""
Glavni prozor aplikacije 
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from decimal import Decimal
from src.business.manager import ExpenseManager
from src.storage.json_storage import JsonStorage
from .widgets import TransactionDialog, StatsFrame
from config import DATA_FILE, CATEGORIES


class MainWindow(tk.Tk):
    
    def __init__(self):
        super().__init__()
        
        self.title("Finance Tracker - Praćenje osobnih troškova")
        self.geometry("900x700")
        
        # Inicijalizacija managera
        storage = JsonStorage(DATA_FILE)
        self.manager = ExpenseManager(storage)
        
        # Elementi sučelja
        self.tree: ttk.Treeview | None = None
        self.stats_frame: StatsFrame | None = None
        
        # Filteri
        self.category_filter = tk.StringVar(value="Sve")
        self.type_filter = tk.StringVar(value="Sve")
        
        # Sortiranje
        self.sort_column = "Datum"
        self.sort_ascending = False
        
        self._build_ui()
        self._refresh_data()
    

    # Korisničko sučelje
    def _build_ui(self) -> None:
        # Gornja traka s gumbima
        toolbar = ttk.Frame(self, padding="10")
        toolbar.pack(fill=tk.X, side=tk.TOP)
        
        ttk.Button(toolbar, text="+ Nova transakcija", command=self._add_transaction).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Uređivanje", command=self._edit_transaction).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Brisanje", command=self._delete_transaction).pack(side=tk.LEFT, padx=5)
        
        # Filtri
        filter_frame = ttk.LabelFrame(self, text="Filtri", padding="10")
        filter_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(filter_frame, text="Kategorija:").pack(side=tk.LEFT, padx=5)
        categories = ["Sve"] + CATEGORIES
        category_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.category_filter,
            values=categories,
            state="readonly",
            width=15
        )
        category_combo.pack(side=tk.LEFT, padx=5)
        category_combo.bind("<<ComboboxSelected>>", lambda e: self._refresh_data())
        
        ttk.Label(filter_frame, text="Tip:").pack(side=tk.LEFT, padx=5)
        type_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.type_filter,
            values=["Sve", "Trošak", "Prihod"],
            state="readonly",
            width=10
        )
        type_combo.pack(side=tk.LEFT, padx=5)
        type_combo.bind("<<ComboboxSelected>>", lambda e: self._refresh_data())
        
        
        main_paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        left_frame = ttk.Frame(main_paned)
        main_paned.add(left_frame, weight=3)
        
        # Tabela transakcija
        columns = ("Datum", "Kategorija", "Vrsta", "Iznos", "Opis")
        self.tree = ttk.Treeview(left_frame, columns=columns, height=20)
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("Datum", anchor=tk.W, width=100)
        self.tree.column("Kategorija", anchor=tk.W, width=100)
        self.tree.column("Vrsta", anchor=tk.CENTER, width=80)
        self.tree.column("Iznos", anchor=tk.E, width=100)
        self.tree.column("Opis", anchor=tk.W, width=150)
        
        self.tree.heading("#0", text="", anchor=tk.W)
        self.tree.heading("Datum", text="Datum ↓", anchor=tk.W)
        self.tree.heading("Kategorija", text="Kategorija", anchor=tk.W)
        self.tree.heading("Vrsta", text="Vrsta", anchor=tk.CENTER)
        self.tree.heading("Iznos", text="Iznos", anchor=tk.E)
        self.tree.heading("Opis", text="Opis", anchor=tk.W)
        
        # Vezanje eventi na klik zaglavlja
        self.tree.heading("Datum", command=lambda: self._on_heading_click("Datum"))
        self.tree.heading("Kategorija", command=lambda: self._on_heading_click("Kategorija"))
        self.tree.heading("Vrsta", command=lambda: self._on_heading_click("Vrsta"))
        self.tree.heading("Iznos", command=lambda: self._on_heading_click("Iznos"))
        self.tree.heading("Opis", command=lambda: self._on_heading_click("Opis"))
        
        scrollbar = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky=tk.NSEW)
        scrollbar.grid(row=0, column=1, sticky=tk.NS)
        
        left_frame.grid_rowconfigure(0, weight=1)
        left_frame.grid_columnconfigure(0, weight=1)
        
        # Desna strana - statistika
        right_frame = ttk.Frame(main_paned)
        main_paned.add(right_frame, weight=1)
        
        self.stats_frame = StatsFrame(right_frame)
        self.stats_frame.pack(fill=tk.BOTH, expand=True)
    

    def _add_transaction(self) -> None:
        dialog = TransactionDialog(self, "Nova transakcija")
        self.wait_window(dialog)
        
        if dialog.result:
            try:
                transaction_type = dialog.result['type']
                self.manager.add_transaction(
                    amount=dialog.result['amount'],
                    category=dialog.result['category'],
                    description=dialog.result['description'],
                    transaction_type=transaction_type,  # type: ignore
                    date_time=dialog.result['date']
                )
                self._refresh_data()
                messagebox.showinfo("Uspjeh", "Transakcija je dodana")
            except ValueError as e:
                messagebox.showerror("Greška", str(e))
    

    def _edit_transaction(self) -> None:
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Upozorenje", "Odaberite transakciju za uređivanje")
            return
        
        # Dohvati ID iz tag-a
        item = self.tree.item(selection[0])
        if not item['tags']:
            messagebox.showerror("Greška", "Nije moguće pronaći ID transakcije")
            return
        
        transaction_id = item['tags'][0]
        transaction = self.manager.get_transaction(transaction_id)
        
        if not transaction:
            messagebox.showerror("Greška", f"Transakcija {transaction_id} nije pronađena")
            return
        
        
        initial_data = {
            'amount': transaction.amount,
            'type': transaction.type,
            'category': transaction.category,
            'date': transaction.date,
            'description': transaction.description
        }
        
        dialog = TransactionDialog(self, "Uređivanje transakcije", initial_data=initial_data)
        self.wait_window(dialog)
        
        if dialog.result:
            try:
                self.manager.update_transaction(
                    transaction_id=transaction_id,
                    amount=dialog.result['amount'],
                    category=dialog.result['category'],
                    description=dialog.result['description'],
                    date_time=dialog.result['date']
                )
                self._refresh_data()
                messagebox.showinfo("Uspjeh", "Transakcija je ažurirana")
                print(f"✓ Transakcija {transaction_id} je ažurirana")
            except ValueError as e:
                messagebox.showerror("Greška", str(e))
    
    def _delete_transaction(self) -> None:
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Upozorenje", "Odaberite transakciju za brisanje")
            return
        
        if messagebox.askyesno("Potvrda", "Jeste li sigurni da želite obrisati ovu transakciju?"):
            try:
                # Pronađi ID iz vrijednosti
                item = self.tree.item(selection[0])
                # ID je pohranjen kao tag
                if item['tags']:
                    self.manager.delete_transaction(item['tags'][0])
                    self._refresh_data()
                    messagebox.showinfo("Uspjeh", "Transakcija je obrisana")
            except Exception as e:
                messagebox.showerror("Greška", str(e))
    
    def _refresh_data(self) -> None:
        if not self.tree:
            return
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        transactions = self.manager.get_all_transactions()

        category_filter = self.category_filter.get()
        type_filter = self.type_filter.get()
        
        filtered = transactions
        
        if category_filter != "Sve":
            filtered = [t for t in filtered if t.category == category_filter]
        
        if type_filter == "Trošak":
            filtered = [t for t in filtered if t.type == "expense"]
        elif type_filter == "Prihod":
            filtered = [t for t in filtered if t.type == "income"]
        
        # Sortiraj prema odabranoj koloni
        self._sort_transactions(filtered)
        
        # Prikazi
        for transaction in filtered:
            date_str = transaction.date.strftime("%Y-%m-%d")
            type_str = "Prihod" if transaction.type == "income" else "Trošak"
            amount_str = f"{transaction.amount} EUR"
            
            self.tree.insert(
                "",
                "end",
                values=(
                    date_str,
                    transaction.category,
                    type_str,
                    amount_str,
                    transaction.description
                ),
                tags=(transaction.id,)
            )
        
        # Debug ispis
        print(f"✓ Osvježivanje: Pronađeno {len(filtered)} od {len(transactions)} transakcija")
        
        # Ažuriraj statistiku
        if self.stats_frame:
            stats = self.manager.calculate_stats(filtered)
            self.stats_frame.update_stats(stats)
    
    def _on_heading_click(self, column: str) -> None:
        """Metoda za klik na zaglavlje kolone."""
        if self.sort_column == column:
            # Ako je ista kolona, promijeni smjer sortiranja
            self.sort_ascending = not self.sort_ascending
        else:
            # Ako je nova kolona, sortiraj po njoj (descending po defaultu)
            self.sort_column = column
            self.sort_ascending = False
        
        # Ažuriraj zaglavlja s pokazivačima
        self._update_heading_indicators()
        
        # Osvježi podatke
        self._refresh_data()
    
    def _update_heading_indicators(self) -> None:
        """Ažurira zaglavlja s pokazivačima smjera sortiranja."""
        arrow_up = " ↑"
        arrow_down = " ↓"
        
        columns = ["Datum", "Kategorija", "Vrsta", "Iznos", "Opis"]
        
        for col in columns:
            if col == self.sort_column:
                indicator = arrow_up if self.sort_ascending else arrow_down
                self.tree.heading(col, text=f"{col}{indicator}")
            else:
                self.tree.heading(col, text=col)
    
    def _sort_transactions(self, transactions: list) -> None:
        """Sortira transakcije prema odabranoj koloni."""
        sort_key = None
        
        if self.sort_column == "Datum":
            sort_key = lambda x: x.date
        elif self.sort_column == "Kategorija":
            sort_key = lambda x: x.category
        elif self.sort_column == "Vrsta":
            sort_key = lambda x: x.type
        elif self.sort_column == "Iznos":
            sort_key = lambda x: x.amount
        elif self.sort_column == "Opis":
            sort_key = lambda x: x.description
        else:
            sort_key = lambda x: x.date
        
        transactions.sort(key=sort_key, reverse=not self.sort_ascending)
