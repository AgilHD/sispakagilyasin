# Sistem Pakar Diagnosa Depresi

## Deskripsi
Sistem pakar untuk mendiagnosa jenis depresi menggunakan metode **Forward Chaining** dan **Certainty Factor (CF)**. Sistem ini mengimplementasikan rule-based reasoning untuk memberikan diagnosa berdasarkan gejala yang dialami pasien.

## Fitur Utama
- **Forward Chaining**: Proses inferensi yang berjalan dari fakta menuju kesimpulan
- **Certainty Factor**: Sistem keyakinan untuk mengukur tingkat kepastian diagnosa
- **Aturan Sekuensial**: Aturan yang menggunakan hasil dari aturan lain sebagai premis
- **Aturan Paralel**: Beberapa aturan yang menghasilkan kesimpulan sama dengan tingkat keyakinan berbeda
- **Antarmuka Grafis**: UI sederhana menggunakan tkinter untuk interaksi pengguna

## Struktur Proyek
```
diagnosa_depresi/
├── rules.json          # Basis pengetahuan (knowledge base)
├── engine.py           # Inference engine dengan forward chaining
├── depression_ui.py    # Antarmuka pengguna grafis
├── README.md           # Dokumentasi proyek
└── Laporan.pdf         # Laporan 
```

## Basis Pengetahuan (rules.json)

### Gejala (23 gejala)

### Jenis Depresi (4 jenis)
- D1: Depresi Vegetatif
- D2: Depresi Agitasi  
- D3: Depresi Neurotik
- D4: Depresi Psikotik



### 1. CF Gejala
```
CF_gejala = CF_pakar × CF_user
```

### 2. CF Aturan
```
CF_aturan = min(CF_gejala) × CF_rule
```

### 3. Kombinasi CF Paralel
```
Jika CF1 ≥ 0 dan CF2 ≥ 0:
  CF_combined = CF1 + CF2 - (CF1 × CF2)

Jika CF1 ≤ 0 dan CF2 ≤ 0:
  CF_combined = CF1 + CF2 + (CF1 × CF2)

Jika CF1 dan CF2 berbeda tanda:
  CF_combined = (CF1 + CF2) / (1 - min(|CF1|, |CF2|))
```

## Contoh Penggunaan

### Skenario 1: Depresi Vegetatif
**Gejala yang dipilih:**
- G2: Tidak ada nafsu makan (CF: 1.0)
- G3: Cenderung menyendiri (CF: 1.0)  
- G4: Insomnia (CF: 1.0)

**Hasil:**
- D1: Depresi Vegetatif(CF: 0.8)




