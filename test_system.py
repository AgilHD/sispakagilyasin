#!/usr/bin/env python3
"""
Test script untuk sistem pakar yang sudah dibatasi
"""

from engine import DepressionExpertSystem

def test_system():
    """
    Test sistem pakar dengan gejala G1-G23
    """
    print("TEST SISTEM PAKAR DIAGNOSA DEPRESI")
    print("="*50)
    
    # Inisialisasi sistem
    system = DepressionExpertSystem()
    
    if not system.knowledge_base:
        print("Gagal memuat basis pengetahuan!")
        return
    
    print(f"Basis pengetahuan berhasil dimuat:")
    print(f"- {len(system.knowledge_base.get('gejala', []))} gejala")
    print(f"- {len(system.knowledge_base.get('penyakit', []))} penyakit")
    print(f"- {len(system.knowledge_base.get('komplikasi', []))} komplikasi")
    print(f"- {len(system.knowledge_base.get('aturan_pria', []))} aturan pria")
    print(f"- {len(system.knowledge_base.get('aturan_wanita', []))} aturan wanita")
    print(f"- {len(system.knowledge_base.get('aturan', []))} aturan umum")
    
    print("\n" + "="*50)
    print("TEST SKENARIO PRIA")
    print("="*50)
    
    # Test pria
    system.reset_system()
    system.set_gender("pria")
    
    # Gejala untuk D1 (Depresi Endogen)
    gejala_pria = [
        ("G2", "Tidak ada nafsu makan", 1.0),
        ("G3", "Cenderung menyendiri", 1.0),
        ("G4", "Insomnia (susah tidur)", 1.0)
    ]
    
    print("Gejala yang dimasukkan:")
    for kode, nama, cf in gejala_pria:
        system.add_fact(kode, cf)
        print(f"- {kode}: {nama} (CF: {cf})")
    
    print("\nMenjalankan diagnosa...")
    system.forward_chaining()
    system.print_diagnosis()
    
    print("\n" + "="*50)
    print("TEST SKENARIO WANITA")
    print("="*50)
    
    # Test wanita
    system.reset_system()
    system.set_gender("wanita")
    
    # Gejala untuk D1 (Depresi Endogen) - wanita perlu G1
    gejala_wanita = [
        ("G1", "Sebelum siklus menstruasi", 1.0),
        ("G2", "Tidak ada nafsu makan", 1.0),
        ("G3", "Cenderung menyendiri", 1.0),
        ("G4", "Insomnia (susah tidur)", 1.0)
    ]
    
    print("Gejala yang dimasukkan:")
    for kode, nama, cf in gejala_wanita:
        system.add_fact(kode, cf)
        print(f"- {kode}: {nama} (CF: {cf})")
    
    print("\nMenjalankan diagnosa...")
    system.forward_chaining()
    system.print_diagnosis()

if __name__ == "__main__":
    test_system()
