import json
import math
from typing import Dict, List, Tuple, Set

class DepressionExpertSystem:
    def __init__(self, rules_file: str = "rules.json"):
        """
        Inisialisasi sistem pakar diagnosa depresi
        """
        self.rules_file = rules_file
        self.knowledge_base = self.load_knowledge_base()
        self.facts = {}  # Menyimpan fakta yang diketahui
        self.conclusions = {}  # Menyimpan kesimpulan dengan CF
        
    def load_knowledge_base(self) -> Dict:
        """
        Memuat basis pengetahuan dari file JSON
        """
        try:
            with open(self.rules_file, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"File {self.rules_file} tidak ditemukan!")
            return {}
        except json.JSONDecodeError:
            print(f"Error parsing JSON file {self.rules_file}")
            return {}
    
    def add_fact(self, gejala_kode: str, cf_user: float = 1.0):
        """
        Menambahkan fakta gejala dengan tingkat keyakinan user
        """
        self.facts[gejala_kode] = cf_user
        print(f"Fakta ditambahkan: {gejala_kode} dengan CF = {cf_user}")
    
    def get_gejala_info(self, kode: str) -> Dict:
        """
        Mendapatkan informasi gejala berdasarkan kode
        """
        for gejala in self.knowledge_base.get('gejala', []):
            if gejala['kode'] == kode:
                return gejala
        return {}
    
    def get_penyakit_info(self, kode: str) -> Dict:
        """
        Mendapatkan informasi penyakit berdasarkan kode
        """
        for penyakit in self.knowledge_base.get('penyakit', []):
            if penyakit['kode'] == kode:
                return penyakit
        return {}
    
    def get_komplikasi_info(self, kode: str) -> Dict:
        """
        Mendapatkan informasi komplikasi berdasarkan kode
        """
        for komplikasi in self.knowledge_base.get('komplikasi', []):
            if komplikasi['kode'] == kode:
                return komplikasi
        return {}
    
    def calculate_cf_gejala(self, gejala_kode: str) -> float:
        """
        Menghitung CF gejala berdasarkan CF pakar dan CF user
        CF = CF_pakar * CF_user
        """
        gejala_info = self.get_gejala_info(gejala_kode)
        if not gejala_info:
            return 0.0
        
        cf_pakar = gejala_info.get('cf_pakar', 0.0)
        cf_user = self.facts.get(gejala_kode, 1.0)
        
        return cf_pakar * cf_user
    
    def calculate_cf_rule(self, rule: Dict) -> float:
        """
        Menghitung CF aturan berdasarkan gejala yang ada
        CF_rule = min(CF_gejala) * CF_rule
        """
        gejala_list = rule.get('jika', [])
        if not gejala_list:
            return 0.0
        
        # Hitung CF minimum dari semua gejala dalam aturan
        cf_gejala_list = []
        for gejala_kode in gejala_list:
            if gejala_kode in self.facts:
                cf_gejala = self.calculate_cf_gejala(gejala_kode)
                cf_gejala_list.append(cf_gejala)
        
        if not cf_gejala_list:
            return 0.0
        
        min_cf_gejala = min(cf_gejala_list)
        cf_rule = rule.get('cf_rule', 0.0)
        
        return min_cf_gejala * cf_rule
    
    def combine_cf_parallel(self, cf1: float, cf2: float) -> float:
        """
        Menggabungkan CF untuk aturan paralel (menghasilkan kesimpulan yang sama)
        CF_combined = CF1 + CF2 - (CF1 * CF2) jika CF1 dan CF2 > 0
        CF_combined = CF1 + CF2 + (CF1 * CF2) jika CF1 dan CF2 < 0
        CF_combined = (CF1 + CF2) / (1 - min(|CF1|, |CF2|)) jika CF1 dan CF2 berbeda tanda
        """
        if cf1 >= 0 and cf2 >= 0:
            return cf1 + cf2 - (cf1 * cf2)
        elif cf1 <= 0 and cf2 <= 0:
            return cf1 + cf2 + (cf1 * cf2)
        else:
            return (cf1 + cf2) / (1 - min(abs(cf1), abs(cf2)))
    
    def forward_chaining(self) -> Dict:
        """
        Implementasi forward chaining untuk inferensi
        """
        print("\n=== PROSES FORWARD CHAINING ===")
        
        # Reset kesimpulan
        self.conclusions = {}
        
        # Dapatkan semua aturan
        rules = self.knowledge_base.get('aturan', [])
        
        # Proses aturan secara iteratif sampai tidak ada perubahan
        changed = True
        iteration = 1
        
        while changed:
            changed = False
            print(f"\n--- Iterasi {iteration} ---")
            
            for rule in rules:
                rule_id = rule.get('id', '')
                kondisi = rule.get('jika', [])
                kesimpulan = rule.get('maka', '')
                cf_rule = rule.get('cf_rule', 0.0)
                
                print(f"Memproses aturan {rule_id}: {kondisi} -> {kesimpulan}")
                
                # Cek apakah semua kondisi terpenuhi
                kondisi_terpenuhi = True
                for kondisi_kode in kondisi:
                    if kondisi_kode not in self.facts and kondisi_kode not in self.conclusions:
                        kondisi_terpenuhi = False
                        break
                
                if kondisi_terpenuhi:
                    # Hitung CF aturan
                    cf_calculated = self.calculate_cf_rule(rule)
                    print(f"  CF aturan {rule_id}: {cf_calculated:.3f}")
                    
                    if cf_calculated > 0:
                        # Jika kesimpulan sudah ada, gabungkan CF (aturan paralel)
                        if kesimpulan in self.conclusions:
                            old_cf = self.conclusions[kesimpulan]
                            new_cf = self.combine_cf_parallel(old_cf, cf_calculated)
                            print(f"  Menggabungkan CF: {old_cf:.3f} + {cf_calculated:.3f} = {new_cf:.3f}")
                            self.conclusions[kesimpulan] = new_cf
                        else:
                            self.conclusions[kesimpulan] = cf_calculated
                            print(f"  Kesimpulan baru: {kesimpulan} dengan CF = {cf_calculated:.3f}")
                        
                        changed = True
            
            iteration += 1
            if iteration > 10:  # Mencegah infinite loop
                break
        
        return self.conclusions
    
    def get_diagnosis_results(self) -> List[Tuple[str, str, float]]:
        """
        Mendapatkan hasil diagnosa yang sudah diurutkan berdasarkan CF
        """
        results = []
        
        # Proses kesimpulan penyakit
        for kode, cf in self.conclusions.items():
            if kode.startswith('D'):  # Penyakit
                penyakit_info = self.get_penyakit_info(kode)
                if penyakit_info:
                    results.append((kode, penyakit_info['nama'], cf))
            elif kode.startswith('K'):  # Komplikasi
                komplikasi_info = self.get_komplikasi_info(kode)
                if komplikasi_info:
                    results.append((kode, komplikasi_info['nama'], cf))
        
        # Urutkan berdasarkan CF (tertinggi dulu)
        results.sort(key=lambda x: x[2], reverse=True)
        return results
    
    def print_diagnosis(self):
        """
        Mencetak hasil diagnosa
        """
        print("\n" + "="*50)
        print("HASIL DIAGNOSA DEPRESI")
        print("="*50)
        
        if not self.conclusions:
            print("Tidak ada kesimpulan yang dapat diambil.")
            print("Pastikan gejala yang dimasukkan sesuai dengan aturan yang ada.")
            return
        
        results = self.get_diagnosis_results()
        
        print("\nDIAGNOSA UTAMA:")
        print("-" * 30)
        for i, (kode, nama, cf) in enumerate(results, 1):
            if kode.startswith('D'):
                confidence = "Sangat Tinggi" if cf >= 0.8 else "Tinggi" if cf >= 0.6 else "Sedang" if cf >= 0.4 else "Rendah"
                print(f"{i}. {nama}")
                print(f"   Kode: {kode}")
                print(f"   Tingkat Keyakinan: {cf:.3f} ({confidence})")
                print()
        
        print("\nKOMPLIKASI YANG MUNGKIN:")
        print("-" * 30)
        komplikasi_found = False
        for kode, nama, cf in results:
            if kode.startswith('K'):
                komplikasi_found = True
                confidence = "Sangat Tinggi" if cf >= 0.8 else "Tinggi" if cf >= 0.6 else "Sedang" if cf >= 0.4 else "Rendah"
                print(f"- {nama}")
                print(f"  Kode: {kode}")
                print(f"  Tingkat Keyakinan: {cf:.3f} ({confidence})")
                print()
        
        if not komplikasi_found:
            print("Tidak ada komplikasi yang teridentifikasi.")
        
        print("\nREKOMENDASI:")
        print("-" * 30)
        if results:
            highest_cf = results[0][2]
            if highest_cf >= 0.8:
                print("• Segera konsultasi dengan psikolog atau psikiater")
                print("• Pertimbangkan terapi medis dan psikologis")
                print("• Pantau kondisi secara berkala")
            elif highest_cf >= 0.6:
                print("• Konsultasi dengan tenaga kesehatan mental")
                print("• Pertimbangkan konseling atau terapi")
                print("• Lakukan aktivitas yang menenangkan")
            else:
                print("• Konsultasi dengan dokter umum terlebih dahulu")
                print("• Pantau gejala secara berkala")
                print("• Jaga pola hidup sehat")
    
    def reset_system(self):
        """
        Reset sistem untuk diagnosa baru
        """
        self.facts = {}
        self.conclusions = {}
        print("Sistem telah direset. Siap untuk diagnosa baru.")

def main():
    """
    Fungsi utama untuk menjalankan sistem pakar
    """
    print("SISTEM PAKAR DIAGNOSA DEPRESI")
    print("="*40)
    
    # Inisialisasi sistem
    system = DepressionExpertSystem()
    
    if not system.knowledge_base:
        print("Gagal memuat basis pengetahuan!")
        return
    
    print(f"Basis pengetahuan berhasil dimuat:")
    print(f"- {len(system.knowledge_base.get('gejala', []))} gejala")
    print(f"- {len(system.knowledge_base.get('penyakit', []))} jenis depresi")
    print(f"- {len(system.knowledge_base.get('komplikasi', []))} komplikasi")
    print(f"- {len(system.knowledge_base.get('aturan', []))} aturan")
    
    while True:
        print("\n" + "="*40)
        print("MENU UTAMA")
        print("="*40)
        print("1. Tambah gejala")
        print("2. Lihat gejala yang sudah dimasukkan")
        print("3. Jalankan diagnosa")
        print("4. Reset sistem")
        print("5. Keluar")
        
        choice = input("\nPilih menu (1-5): ").strip()
        
        if choice == '1':
            print("\n--- TAMBAH GEJALA ---")
            print("Gejala yang tersedia:")
            
            gejala_list = system.knowledge_base.get('gejala', [])
            for i, gejala in enumerate(gejala_list, 1):
                print(f"{i:2d}. {gejala['kode']} - {gejala['nama']}")
            
            try:
                gejala_idx = int(input("\nPilih nomor gejala: ")) - 1
                if 0 <= gejala_idx < len(gejala_list):
                    gejala_kode = gejala_list[gejala_idx]['kode']
                    cf_user = float(input("Tingkat keyakinan (0.0 - 1.0): "))
                    if 0.0 <= cf_user <= 1.0:
                        system.add_fact(gejala_kode, cf_user)
                    else:
                        print("Tingkat keyakinan harus antara 0.0 dan 1.0!")
                else:
                    print("Nomor gejala tidak valid!")
            except ValueError:
                print("Input tidak valid!")
        
        elif choice == '2':
            print("\n--- GEJALA YANG SUDAH DIMASUKKAN ---")
            if system.facts:
                for kode, cf in system.facts.items():
                    gejala_info = system.get_gejala_info(kode)
                    print(f"- {kode}: {gejala_info.get('nama', 'Unknown')} (CF: {cf})")
            else:
                print("Belum ada gejala yang dimasukkan.")
        
        elif choice == '3':
            if not system.facts:
                print("\nBelum ada gejala yang dimasukkan!")
                continue
            
            print("\n--- MENJALANKAN DIAGNOSA ---")
            system.forward_chaining()
            system.print_diagnosis()
        
        elif choice == '4':
            system.reset_system()
        
        elif choice == '5':
            print("\nTerima kasih telah menggunakan sistem pakar diagnosa depresi!")
            break
        
        else:
            print("\nPilihan tidak valid!")

if __name__ == "__main__":
    main()
