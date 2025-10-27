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
└── README.md           # Dokumentasi proyek
```

## Basis Pengetahuan (rules.json)

### Gejala (30 gejala)
- G1-G23: Gejala depresi dasar
- G24-G30: Gejala tambahan untuk diagnosa yang lebih akurat

### Jenis Depresi (7 jenis)
- D1: Depresi Endogen
- D2: Depresi Agitasi  
- D3: Depresi Neurotik
- D4: Depresi Psikotik
- D5: Depresi Mayor
- D6: Depresi Ringan
- D7: Depresi Berat

### Komplikasi (5 jenis)
- K1: Gangguan Kecemasan
- K2: Gangguan Tidur Kronis
- K3: Gangguan Makan
- K4: Penyalahgunaan Zat
- K5: Risiko Bunuh Diri Tinggi

### Aturan (13 aturan)
- R1-R7: Aturan diagnosa penyakit
- R8-R11: Aturan sekuensial (komplikasi)
- R12-R13: Aturan paralel (diagnosa ganda)

## Implementasi Aturan Sekuensial dan Paralel

### Aturan Sekuensial
Aturan R8-R11 menggunakan hasil diagnosa penyakit sebagai premis untuk menentukan komplikasi:
```json
{
  "id": "R8",
  "jika": ["D1", "D3"],
  "maka": "K1",
  "cf_rule": 0.6
}
```

### Aturan Paralel
Aturan R12 dan R13 menghasilkan kesimpulan berbeda dengan gejala yang sama:
```json
{
  "id": "R12",
  "jika": ["G2", "G3", "G4", "G24", "G25"],
  "maka": "D1",
  "cf_rule": 0.9
},
{
  "id": "R13", 
  "jika": ["G2", "G3", "G4", "G24", "G25"],
  "maka": "D5",
  "cf_rule": 0.8
}
```

## Algoritma Certainty Factor

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

## Cara Menjalankan

### 1. Mode Command Line
```bash
python engine.py
```

### 2. Mode GUI
```bash
python depression_ui.py
```

## Cara Penggunaan

### Mode GUI (Recommended)
1. Jalankan `python depression_ui.py`
2. Pilih gejala yang dialami dengan mencentang checkbox
3. Sesuaikan tingkat keyakinan (CF) jika diperlukan
4. Klik "JALANKAN DIAGNOSA"
5. Lihat hasil diagnosa di panel kanan

### Mode Command Line
1. Jalankan `python engine.py`
2. Pilih menu "1" untuk menambah gejala
3. Pilih nomor gejala yang sesuai
4. Masukkan tingkat keyakinan (0.0 - 1.0)
5. Ulangi untuk gejala lainnya
6. Pilih menu "3" untuk menjalankan diagnosa

## Contoh Penggunaan

### Skenario 1: Depresi Endogen
**Gejala yang dipilih:**
- G2: Tidak ada nafsu makan (CF: 1.0)
- G3: Cenderung menyendiri (CF: 1.0)  
- G4: Insomnia (CF: 1.0)

**Hasil:**
- D1: Depresi Endogen (CF: 0.8)
- K1: Gangguan Kecemasan (CF: 0.48)

### Skenario 2: Depresi Berat
**Gejala yang dipilih:**
- G9: Merasa sangat bersalah (CF: 1.0)
- G10: Ingin bunuh diri (CF: 1.0)
- G29: Merasa putus asa (CF: 1.0)
- G30: Pikiran bunuh diri berulang (CF: 1.0)

**Hasil:**
- D7: Depresi Berat (CF: 0.95)
- K3: Gangguan Makan (CF: 0.76)
- K5: Risiko Bunuh Diri Tinggi (CF: 0.855)

## Penelitian Acuan
Sistem ini dikembangkan berdasarkan penelitian tentang diagnosa depresi menggunakan sistem pakar dengan metode certainty factor. Aturan-aturan yang digunakan mengacu pada kriteria diagnostik depresi menurut DSM-5 dan ICD-10.

## Referensi Tambahan
- American Psychiatric Association. (2013). Diagnostic and statistical manual of mental disorders (5th ed.)
- World Health Organization. (2019). International Classification of Diseases (11th ed.)
- Shortliffe, E. H., & Buchanan, B. G. (1975). A model of inexact reasoning in medicine

## Teknologi yang Digunakan
- **Python 3.x**: Bahasa pemrograman utama
- **JSON**: Format penyimpanan basis pengetahuan
- **Tkinter**: Library untuk antarmuka grafis
- **Forward Chaining**: Algoritma inferensi
- **Certainty Factor**: Sistem keyakinan

## Kontributor
- Tim Mahasiswa Sistem Pakar
- Mata Kuliah: Sistem Pakar
- Semester: 5

## Lisensi
Proyek ini dibuat untuk keperluan akademik dan pembelajaran.