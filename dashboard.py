import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="TrafficSense AI - DS Dashboard", layout="wide", page_icon="📊")

# --- 2. DATA DARI HASIL EDA (110.916 Objek) ---
data_eda = {
    'Kategori': ['Motorcycle', 'Car', 'Truck', 'Bus'],
    'Jumlah': [48229, 42913, 12539, 7235],
    'Persentase': [43.48, 38.69, 11.30, 6.52],
    'smp_Weight': [0.50, 1.00, 1.30, 1.30]
}
df_eda = pd.DataFrame(data_eda)

# --- 3. SIDEBAR NAVIGATION ---
st.sidebar.title("🚀 TrafficSense AI")
st.sidebar.markdown("### *Data Scientist Portal*")
menu = st.sidebar.selectbox("Pilih Analisis:", 
    ["Dataset Overview", "EDA & Sebaran Data", "Logika PKJI & smp", "A/B Testing Result", "Simulasi Kalkulator Kepadatan"])

# --- 4. HALAMAN 1: DATASET OVERVIEW ---
if menu == "Dataset Overview":
    st.title("📂 Dataset Integrity & Quality Report")
    st.write("Laporan proses Data Wrangling dan Penjaminan Mutu Dataset.")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Citra Terintegrasi", "26.124", "Final Split")
    col2.metric("Total Objek Terverifikasi", "110.916", "High Scale")
    col3.metric("Data Purging (Null Images)", "7.121", "-27% Efficiency")

    st.divider()
    st.markdown("""
    ### 🛠️ Aktivitas Data Science yang Telah Diselesaikan:
    1. **Gathering:** Integrasi 5 dataset heterogen via API.
    2. **Cleaning:** Remapping 45 kelas redundan menjadi 4 kelas identitas (Motor, Mobil, Bus, Truk).
    3. **Purging:** Menghapus 7.121 gambar tanpa label (Noise) untuk mempercepat training.
    4. **Balancing:** Memastikan rasio kelas mayoritas (Motor & Mobil) berada pada angka ~1:1.
    """)
    st.success("✅ Dataset dinyatakan VALID dan siap diproses oleh AI Engineer.")

# --- 5. HALAMAN 2: EDA & SEBARAN DATA ---
elif menu == "EDA & Sebaran Data":
    st.title("📊 Exploratory Data Analysis (EDA)")
    
    col_a, col_b = st.columns([2, 1])
    with col_a:
        fig = px.bar(df_eda, x='Kategori', y='Jumlah', text='Jumlah', color='Kategori',
                     title="Distribusi Kendaraan Standar PKJI 2023",
                     color_discrete_sequence=px.colors.qualitative.Vivid)
        st.plotly_chart(fig, use_container_width=True)
    
    with col_b:
        st.write("### 💡 Data Insight")
        st.info(f"Kategori terbanyak: **{df_eda.iloc[0]['Kategori']}**")
        st.write(f"Selisih Motor & Mobil hanya **4.79%**. Ini membuktikan dataset **Sangat Seimbang**.")
        st.write("Jumlah data Bus & Truk sudah melampaui batas minimum training (>2.000 objek).")

# --- 6. HALAMAN 3: LOGIKA PKJI & SMP ---
elif menu == "Logika PKJI & smp":
    st.title("📖 Data Dictionary & Feature Engineering")
    st.write("Transformasi data mentah menjadi metrik beban jalan (smp).")
    
    st.subheader("1. Tabel Bobot smp (Satuan Mobil Penumpang)")
    st.table(df_eda[['Kategori', 'smp_Weight']])
    
    st.subheader("2. Ambang Batas (Threshold) Kepadatan")
    threshold_data = {
        'Status': ['🟢 LANCAR', '🟡 RAMAI LANCAR', '🟠 PADAT', '🔴 MACET'],
        'Range smp': ['< 8.0', '8.0 - 15.0', '15.0 - 25.0', '> 25.0'],
        'Keterangan': ['Arus bebas', 'Volume meningkat', 'Kecepatan menurun', 'Arus terhenti/Antrian']
    }
    st.dataframe(pd.DataFrame(threshold_data), use_container_width=True)

# --- 7. HALAMAN 4: A/B TESTING RESULT ---
elif menu == "A/B Testing Result":
    st.title("🧪 A/B Testing: Optimasi Logika")
    st.write("Membandingkan Metode Hitung Biasa vs Metode smp PKJI.")
    
    col_x, col_y = st.columns(2)
    with col_x:
        st.write("**Grup A: Simple Counting**")
        st.error("20.0% False Alarm (Macet)")
    with col_y:
        st.write("**Grup B: Weighted smp**")
        st.success("8.0% Real Macet")
        
    st.divider()
    st.warning("⚠️ **Kesimpulan:** Penggunaan bobot smp mengurangi kesalahan interpretasi data (False Positive) sebesar **12%** dibandingkan hanya menghitung unit kendaraan.")

# --- 8. HALAMAN 5: SIMULASI KALKULATOR ---
elif menu == "Simulasi Kalkulator Kepadatan":
    st.title("🧮 Kalkulator Simulasi Kepadatan")
    st.write("Masukkan jumlah kendaraan hasil deteksi untuk melihat status jalan.")
    
    c1, c2, c3, c4 = st.columns(4)
    mc = c1.number_input("Jumlah Motor", 0, 100, 10)
    car = c2.number_input("Jumlah Mobil", 0, 100, 5)
    bus = c3.number_input("Jumlah Bus", 0, 50, 1)
    truck = c4.number_input("Jumlah Truk", 0, 50, 0)
    
    total_smp = (mc * 0.5) + (car * 1.0) + (bus * 1.3) + (truck * 1.3)
    
    if total_smp < 8: status = "🟢 LANCAR"
    elif 8 <= total_smp < 15: status = "🟡 RAMAI LANCAR"
    elif 15 <= total_smp < 25: status = "🟠 PADAT"
    else: status = "🔴 MACET"
    
    st.metric("Total Skor Beban Jalan (smp)", f"{total_smp:.2f}")
    st.header(f"Status Jalan: {status}")

# --- FOOTER ---
st.sidebar.markdown("---")
st.sidebar.caption("TrafficSense AI v1.0 | Data Science Team")