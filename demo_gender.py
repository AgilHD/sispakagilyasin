#!/usr/bin/env python3
"""
Demo script untuk menunjukkan perbedaan aturan Pria vs Wanita
dalam Sistem Pakar Diagnosa Depresi
"""

from engine import DepressionExpertSystem

def demo_pria():
    """
    Demo untuk pasien Pria
    """
    print("="*60)
    print("DEMO SKENARIO: PASIEN PRIA")
    print("="*60)
    
    system = DepressionExpertSystem()
    
    # Set gender pria
    system.set_gender("pria")
    
    # Gejala yang dialami (sesuai aturan pria)
    gejala_list = [
        ("G2", "Tidak ada nafsu makan", 1.0),
        ("G3", "Cenderung menyendiri", 1.0),
        ("G4", "Insomnia (susah tidur)", 1.0)
    ]
    
    print("Gejala yang dimasukkan:")
    for kode, nama, cf in gejala_list:
        system.add_fact(kode, cf)
        print(f"- {kode}: {nama} (CF: {cf})")
    
    print("\nMenjalankan diagnosa...")
    system.forward_chaining()
    system.print_diagnosis()

def demo_wanita():
    """
    Demo untuk pasien Wanita
    """
    print("\n" + "="*60)
    print("DEMO SKENARIO: PASIEN WANITA")
    print("="*60)
    
    system = DepressionExpertSystem()
    
    # Set gender wanita
    system.set_gender("wanita")
    
    # Gejala yang dialami (sesuai aturan wanita - termasuk G1)
    gejala_list = [
        ("G1", "Sebelum siklus menstruasi", 1.0),
        ("G2", "Tidak ada nafsu makan", 1.0),
        ("G3", "Cenderung menyendiri", 1.0),
        ("G4", "Insomnia (susah tidur)", 1.0)
    ]
    
    print("Gejala yang dimasukkan:")
    for kode, nama, cf in gejala_list:
        system.add_fact(kode, cf)
        print(f"- {kode}: {nama} (CF: {cf})")
    
    print("\nMenjalankan diagnosa...")
    system.forward_chaining()
    system.print_diagnosis()

def demo_perbandingan():
    """
    Demo perbandingan aturan pria vs wanita
    """
    print("\n" + "="*60)
    print("PERBANDINGAN ATURAN PRIA vs WANITA")
    print("="*60)
    
    print("\nATURAN R1 (Depresi Endogen):")
    print("Pria  : IF [G2] AND [G3] AND [G4] THEN D1")
    print("Wanita: IF [G1] AND [G2] AND [G3] AND [G4] THEN D1")
    print("Perbedaan: Wanita memerlukan G1 (Sebelum siklus menstruasi)")
    
    print("\nATURAN R2 (Depresi Agitasi):")
    print("Pria  : IF [G2] AND [G5] AND [G6] AND [G7] AND [G8] AND [G9] AND [G10] THEN D2")
    print("Wanita: IF [G2] AND [G5] AND [G6] AND [G7] AND [G8] AND [G9] AND [G10] AND [G11] THEN D2")
    print("Perbedaan: Wanita memerlukan G11 (Kehilangan siklus menstruasi)")
    
    print("\nATURAN R3 (Depresi Neurotik):")
    print("Pria  : IF [G12] AND [G13] AND [G14] AND [G15] AND [G16] AND [G17] AND [G18] THEN D3")
    print("Wanita: IF [G1] AND [G11] AND [G12] AND [G13] AND [G14] AND [G15] AND [G16] AND [G17] AND [G18] THEN D3")
    print("Perbedaan: Wanita memerlukan G1 dan G11 (gejala menstruasi)")
    
    print("\nATURAN R4 (Depresi Psikotik):")
    print("Pria  : IF [G19] AND [G20] AND [G21] AND [G22] AND [G23] THEN D4")
    print("Wanita: IF [G19] AND [G20] AND [G21] AND [G22] AND [G23] THEN D4")
    print("Perbedaan: SAMA (tidak ada perbedaan)")

def demo_gejala_menstruasi():
    """
    Demo khusus gejala menstruasi untuk wanita
    """
    print("\n" + "="*60)
    print("DEMO GEJALA MENSTRUASI (WANITA)")
    print("="*60)
    
    system = DepressionExpertSystem()
    system.set_gender("wanita")
    
    # Gejala menstruasi + gejala depresi
    gejala_list = [
        ("G1", "Sebelum siklus menstruasi", 1.0),
        ("G11", "Kehilangan siklus menstruasi", 1.0),
        ("G12", "Perubahan kepribadian", 1.0),
        ("G13", "Wajah terlihat murung", 1.0),
        ("G14", "Pasif", 1.0),
        ("G15", "Merasa curiga", 1.0),
        ("G16", "Suka mengkritik", 1.0),
        ("G17", "Penuh pikiran negatif", 1.0),
        ("G18", "Ketakutan berlebihan akan menjadi gila", 1.0)
    ]
    
    print("Gejala yang dimasukkan (termasuk gejala menstruasi):")
    for kode, nama, cf in gejala_list:
        system.add_fact(kode, cf)
        print(f"- {kode}: {nama} (CF: {cf})")
    
    print("\nMenjalankan diagnosa...")
    system.forward_chaining()
    system.print_diagnosis()

def main():
    """
    Fungsi utama untuk menjalankan demo gender
    """
    print("SISTEM PAKAR DIAGNOSA DEPRESI - DEMO GENDER")
    print("Perbedaan Aturan Pria vs Wanita")
    print("="*60)
    
    try:
        # Jalankan semua demo
        demo_perbandingan()
        demo_pria()
        demo_wanita()
        demo_gejala_menstruasi()
        
        print("\n" + "="*60)
        print("DEMO SELESAI")
        print("="*60)
        print("Kesimpulan:")
        print("- Pria: Menggunakan aturan standar tanpa gejala menstruasi")
        print("- Wanita: Menggunakan aturan khusus dengan gejala menstruasi (G1, G11)")
        print("- Gejala menstruasi mempengaruhi diagnosa depresi pada wanita")
        
    except Exception as e:
        print(f"Error dalam demo: {e}")
        print("Pastikan file rules.json ada di direktori yang sama!")

if __name__ == "__main__":
    main()
