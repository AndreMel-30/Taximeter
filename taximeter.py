import tkinter as tk
from tkinter import messagebox
import time

class TaximeterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("JJ-Studio-Taximeter 2.0")
        self.root.geometry('800x600')
        self.root.configure(bg='#f0f0f0')

        # --- Variabili di Stato ---
        self.running = False
        self.start_time = 0
        self.elapsed_time = 0
        
        # --- Interfaccia Grafica (GUI) ---
        self.create_widgets()

    def create_widgets(self):
        # Frame Principale
        main_frame = tk.Frame(self.root, bg='white', padx=20, pady=20, bd=2, relief="groove")
        main_frame.pack(expand=True)

        # Input Costo Orario
        tk.Label(main_frame, text='Costo Orario (€):', font=('Helvetica', 14), bg='white').grid(row=0, column=0, padx=5, pady=5)
        
        self.entry_costo = tk.Entry(main_frame, font=('Helvetica', 14), width=10, justify='center')
        self.entry_costo.grid(row=0, column=1, padx=5, pady=5)
        self.entry_costo.insert(0, "30.00") # Valore di default per comodità

        # Pulsanti di Controllo
        btn_frame = tk.Frame(main_frame, bg='white')
        btn_frame.grid(row=1, column=0, columnspan=2, pady=20)

        self.btn_start = tk.Button(btn_frame, text='START', font=('Helvetica', 12, 'bold'), bg="#4CAF50", fg="white", width=10, command=self.start)
        self.btn_start.pack(side=tk.LEFT, padx=5)

        self.btn_stop = tk.Button(btn_frame, text='STOP', font=('Helvetica', 12, 'bold'), bg="#f44336", fg="white", width=10, state='disabled', command=self.stop)
        self.btn_stop.pack(side=tk.LEFT, padx=5)

        self.btn_reset = tk.Button(btn_frame, text='RESET', font=('Helvetica', 12, 'bold'), bg="#FF9800", fg="white", width=10, state='disabled', command=self.reset)
        self.btn_reset.pack(side=tk.LEFT, padx=5)

        # Display Tempo
        self.lbl_time = tk.Label(main_frame, text='00:00:00', font=('Helvetica', 48, 'bold'), bg='white', fg="#333")
        self.lbl_time.grid(row=2, column=0, columnspan=2, pady=10)

        # Display Costo
        self.lbl_costo = tk.Label(main_frame, text='Costo: 0.00 €', font=('Helvetica', 20), bg='white', fg="#0056b3")
        self.lbl_costo.grid(row=3, column=0, columnspan=2, pady=10)

    def start(self):
        try:
            # Sostituisce la virgola con il punto per supportare formato italiano
            costo_str = self.entry_costo.get().replace(',', '.')
            self.costo_orario = float(costo_str)
        except ValueError:
            messagebox.showerror("Errore", "Inserisci un costo orario valido (es. 25.50)")
            return

        if not self.running:
            self.running = True
            # Imposta il tempo di inizio sottraendo il tempo già trascorso (per permettere pausa/ripresa)
            self.start_time = time.time() - self.elapsed_time
            self.update_timer()
            
            # Gestione stato pulsanti
            self.btn_start.config(state='disabled')
            self.btn_stop.config(state='normal')
            self.btn_reset.config(state='disabled')
            self.entry_costo.config(state='disabled')

    def stop(self):
        if self.running:
            self.running = False
            self.btn_start.config(state='normal')
            self.btn_stop.config(state='disabled')
            self.btn_reset.config(state='normal')
            self.calculate_cost()

    def reset(self):
        self.running = False
        self.elapsed_time = 0
        self.lbl_time.config(text="00:00:00")
        self.lbl_costo.config(text="Costo: 0.00 €")
        
        self.btn_start.config(state='normal')
        self.btn_stop.config(state='disabled')
        self.btn_reset.config(state='disabled')
        self.entry_costo.config(state='normal')

    def update_timer(self):
        if self.running:
            # Calcolo preciso basato sul clock di sistema
            self.elapsed_time = time.time() - self.start_time
            self.update_display()
            self.root.after(100, self.update_timer) # Aggiorna ogni 100ms per fluidità

    def calculate_cost(self):
        # Costo = (Secondi Totali / 3600) * Costo Orario
        totale = (self.elapsed_time / 3600) * self.costo_orario
        self.lbl_costo.config(text=f"Costo: {totale:.2f} €")

    def update_display(self):
        # Conversione secondi totali in Ore:Minuti:Secondi
        minutes, seconds = divmod(int(self.elapsed_time), 60)
        hours, minutes = divmod(minutes, 60)
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        self.lbl_time.config(text=time_str)
        
        # Aggiornamento dinamico del costo mentre gira (opzionale, carino da vedere)
        self.calculate_cost()

if __name__ == "__main__":
    root = tk.Tk()
    # Esegue l'app
    app = TaximeterApp(root)
    root.mainloop()
