import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
from engine import DepressionExpertSystem

class DepressionDiagnosisUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Pakar Diagnosa Depresi")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        # Inisialisasi sistem pakar
        self.system = DepressionExpertSystem()
        
        # Variabel untuk menyimpan gejala yang dipilih
        self.selected_symptoms = {}
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        """
        Setup antarmuka pengguna
        """
        # Header
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        header_frame.pack(fill='x', padx=10, pady=5)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="SISTEM PAKAR DIAGNOSA DEPRESI", 
                              font=('Arial', 16, 'bold'), fg='white', bg='#2c3e50')
        title_label.pack(expand=True)
        
        subtitle_label = tk.Label(header_frame, text="Forward Chaining + Certainty Factor", 
                                 font=('Arial', 10), fg='#bdc3c7', bg='#2c3e50')
        subtitle_label.pack()
        
        # Main content frame
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Left panel - Gejala selection
        left_frame = tk.Frame(main_frame, bg='#ecf0f1', relief='raised', bd=2)
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        # Gejala selection
        gejala_label = tk.Label(left_frame, text="PILIH GEJALA YANG DIALAMI", 
                               font=('Arial', 12, 'bold'), bg='#ecf0f1')
        gejala_label.pack(pady=10)
        
        # Scrollable frame for symptoms
        canvas = tk.Canvas(left_frame, bg='#ecf0f1')
        scrollbar = ttk.Scrollbar(left_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#ecf0f1')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Load symptoms
        self.load_symptoms(scrollable_frame)
        
        canvas.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scrollbar.pack(side="right", fill="y")
        
        # Right panel - Results and controls
        right_frame = tk.Frame(main_frame, bg='#ecf0f1', relief='raised', bd=2)
        right_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
        # Selected symptoms
        selected_label = tk.Label(right_frame, text="GEJALA YANG DIPILIH", 
                                 font=('Arial', 12, 'bold'), bg='#ecf0f1')
        selected_label.pack(pady=10)
        
        self.selected_listbox = tk.Listbox(right_frame, height=8, font=('Arial', 9))
        self.selected_listbox.pack(fill='x', padx=10, pady=5)
        
        # Control buttons
        button_frame = tk.Frame(right_frame, bg='#ecf0f1')
        button_frame.pack(fill='x', padx=10, pady=10)
        
        diagnose_btn = tk.Button(button_frame, text="JALANKAN DIAGNOSA", 
                               command=self.run_diagnosis, bg='#3498db', fg='white',
                               font=('Arial', 10, 'bold'), padx=20, pady=5)
        diagnose_btn.pack(side='left', padx=5)
        
        clear_btn = tk.Button(button_frame, text="RESET", 
                            command=self.clear_selection, bg='#e74c3c', fg='white',
                            font=('Arial', 10, 'bold'), padx=20, pady=5)
        clear_btn.pack(side='left', padx=5)
        
        # Results area
        results_label = tk.Label(right_frame, text="HASIL DIAGNOSA", 
                                font=('Arial', 12, 'bold'), bg='#ecf0f1')
        results_label.pack(pady=(20, 5))
        
        self.results_text = scrolledtext.ScrolledText(right_frame, height=15, 
                                                     font=('Arial', 9), wrap='word')
        self.results_text.pack(fill='both', expand=True, padx=10, pady=5)
        
    def load_symptoms(self, parent):
        """
        Load gejala dari knowledge base ke UI
        """
        gejala_list = self.system.knowledge_base.get('gejala', [])
        
        for i, gejala in enumerate(gejala_list):
            # Frame for each symptom
            symptom_frame = tk.Frame(parent, bg='#ecf0f1', relief='groove', bd=1)
            symptom_frame.pack(fill='x', padx=5, pady=2)
            
            # Checkbox for symptom selection
            var = tk.BooleanVar()
            checkbox = tk.Checkbutton(symptom_frame, variable=var, 
                                    command=lambda v=var, k=gejala['kode'], n=gejala['nama']: 
                                    self.toggle_symptom(v, k, n),
                                    bg='#ecf0f1')
            checkbox.pack(side='left', padx=5, pady=5)
            
            # Symptom info
            info_frame = tk.Frame(symptom_frame, bg='#ecf0f1')
            info_frame.pack(side='left', fill='x', expand=True, padx=5, pady=5)
            
            # Symptom name
            name_label = tk.Label(info_frame, text=gejala['nama'], 
                                 font=('Arial', 9), bg='#ecf0f1', anchor='w')
            name_label.pack(fill='x')
            
            # Symptom code and CF
            code_label = tk.Label(info_frame, text=f"{gejala['kode']} (CF: {gejala['cf_pakar']})", 
                                 font=('Arial', 8), fg='#7f8c8d', bg='#ecf0f1', anchor='w')
            code_label.pack(fill='x')
            
            # Confidence level input
            conf_frame = tk.Frame(symptom_frame, bg='#ecf0f1')
            conf_frame.pack(side='right', padx=5, pady=5)
            
            conf_label = tk.Label(conf_frame, text="CF:", font=('Arial', 8), bg='#ecf0f1')
            conf_label.pack(side='left')
            
            conf_var = tk.DoubleVar(value=1.0)
            conf_spinbox = tk.Spinbox(conf_frame, from_=0.0, to=1.0, increment=0.1, 
                                    textvariable=conf_var, width=5, font=('Arial', 8))
            conf_spinbox.pack(side='left')
            
            # Store references
            symptom_frame.var = var
            symptom_frame.conf_var = conf_var
            symptom_frame.kode = gejala['kode']
            symptom_frame.nama = gejala['nama']
    
    def toggle_symptom(self, var, kode, nama):
        """
        Toggle gejala selection
        """
        if var.get():
            # Get confidence value from the spinbox
            parent = var.master
            conf_value = parent.conf_var.get()
            self.selected_symptoms[kode] = {
                'nama': nama,
                'cf': conf_value
            }
            self.update_selected_list()
        else:
            if kode in self.selected_symptoms:
                del self.selected_symptoms[kode]
                self.update_selected_list()
    
    def update_selected_list(self):
        """
        Update daftar gejala yang dipilih
        """
        self.selected_listbox.delete(0, tk.END)
        for kode, info in self.selected_symptoms.items():
            self.selected_listbox.insert(tk.END, f"{kode}: {info['nama']} (CF: {info['cf']})")
    
    def run_diagnosis(self):
        """
        Menjalankan diagnosa
        """
        if not self.selected_symptoms:
            messagebox.showwarning("Peringatan", "Pilih minimal satu gejala untuk diagnosa!")
            return
        
        # Clear previous results
        self.results_text.delete(1.0, tk.END)
        
        # Reset system
        self.system.reset_system()
        
        # Add selected symptoms to system
        for kode, info in self.selected_symptoms.items():
            self.system.add_fact(kode, info['cf'])
        
        # Run forward chaining
        self.results_text.insert(tk.END, "=== PROSES DIAGNOSA ===\n\n")
        self.results_text.insert(tk.END, f"Gejala yang dimasukkan: {len(self.selected_symptoms)}\n")
        for kode, info in self.selected_symptoms.items():
            self.results_text.insert(tk.END, f"- {kode}: {info['nama']} (CF: {info['cf']})\n")
        
        self.results_text.insert(tk.END, "\n" + "="*50 + "\n")
        self.results_text.insert(tk.END, "HASIL DIAGNOSA DEPRESI\n")
        self.results_text.insert(tk.END, "="*50 + "\n\n")
        
        # Run inference
        conclusions = self.system.forward_chaining()
        
        if not conclusions:
            self.results_text.insert(tk.END, "Tidak ada kesimpulan yang dapat diambil.\n")
            self.results_text.insert(tk.END, "Pastikan gejala yang dimasukkan sesuai dengan aturan yang ada.\n")
            return
        
        # Get diagnosis results
        results = self.system.get_diagnosis_results()
        
        # Display main diagnosis
        self.results_text.insert(tk.END, "DIAGNOSA UTAMA:\n")
        self.results_text.insert(tk.END, "-" * 30 + "\n")
        
        penyakit_count = 0
        for i, (kode, nama, cf) in enumerate(results, 1):
            if kode.startswith('D'):
                penyakit_count += 1
                confidence = "Sangat Tinggi" if cf >= 0.8 else "Tinggi" if cf >= 0.6 else "Sedang" if cf >= 0.4 else "Rendah"
                self.results_text.insert(tk.END, f"{i}. {nama}\n")
                self.results_text.insert(tk.END, f"   Kode: {kode}\n")
                self.results_text.insert(tk.END, f"   Tingkat Keyakinan: {cf:.3f} ({confidence})\n\n")
        
        if penyakit_count == 0:
            self.results_text.insert(tk.END, "Tidak ada diagnosa penyakit yang dapat ditegakkan.\n\n")
        
        # Display complications
        self.results_text.insert(tk.END, "KOMPLIKASI YANG MUNGKIN:\n")
        self.results_text.insert(tk.END, "-" * 30 + "\n")
        
        komplikasi_found = False
        for kode, nama, cf in results:
            if kode.startswith('K'):
                komplikasi_found = True
                confidence = "Sangat Tinggi" if cf >= 0.8 else "Tinggi" if cf >= 0.6 else "Sedang" if cf >= 0.4 else "Rendah"
                self.results_text.insert(tk.END, f"- {nama}\n")
                self.results_text.insert(tk.END, f"  Kode: {kode}\n")
                self.results_text.insert(tk.END, f"  Tingkat Keyakinan: {cf:.3f} ({confidence})\n\n")
        
        if not komplikasi_found:
            self.results_text.insert(tk.END, "Tidak ada komplikasi yang teridentifikasi.\n\n")
        
        # Display recommendations
        self.results_text.insert(tk.END, "REKOMENDASI:\n")
        self.results_text.insert(tk.END, "-" * 30 + "\n")
        
        if results:
            highest_cf = results[0][2]
            if highest_cf >= 0.8:
                self.results_text.insert(tk.END, "• Segera konsultasi dengan psikolog atau psikiater\n")
                self.results_text.insert(tk.END, "• Pertimbangkan terapi medis dan psikologis\n")
                self.results_text.insert(tk.END, "• Pantau kondisi secara berkala\n")
            elif highest_cf >= 0.6:
                self.results_text.insert(tk.END, "• Konsultasi dengan tenaga kesehatan mental\n")
                self.results_text.insert(tk.END, "• Pertimbangkan konseling atau terapi\n")
                self.results_text.insert(tk.END, "• Lakukan aktivitas yang menenangkan\n")
            else:
                self.results_text.insert(tk.END, "• Konsultasi dengan dokter umum terlebih dahulu\n")
                self.results_text.insert(tk.END, "• Pantau gejala secara berkala\n")
                self.results_text.insert(tk.END, "• Jaga pola hidup sehat\n")
        
        # Scroll to top
        self.results_text.see(1.0)
    
    def clear_selection(self):
        """
        Clear semua pilihan gejala
        """
        self.selected_symptoms.clear()
        self.update_selected_list()
        self.results_text.delete(1.0, tk.END)
        
        # Uncheck all checkboxes
        for widget in self.root.winfo_children():
            self._uncheck_widgets(widget)
    
    def _uncheck_widgets(self, widget):
        """
        Helper function to uncheck all checkboxes recursively
        """
        if hasattr(widget, 'var'):
            widget.var.set(False)
        for child in widget.winfo_children():
            self._uncheck_widgets(child)

def main():
    """
    Fungsi utama untuk menjalankan aplikasi GUI
    """
    root = tk.Tk()
    app = DepressionDiagnosisUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
