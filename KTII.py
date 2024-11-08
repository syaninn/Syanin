import streamlit as st
import pandas as pd
from datetime import datetime

# Inisialisasi state sesi untuk menyimpan catatan berat badan
if 'weight_records' not in st.session_state:
    st.session_state.weight_records = []

# Fungsi untuk menghitung BMI
def calculate_bmi(weight, height_cm):
    height_m = height_cm / 100  # Mengonversi tinggi dari cm ke m
    bmi = weight / (height_m ** 2)
    return bmi

# Fungsi untuk menghitung berat badan ideal
def ideal_weight(gender, height_cm):
    if gender == "Laki-laki":
        return (height_cm - 100) - ((height_cm - 100) * 0.1)  # Rumus berat badan ideal laki-laki
    else:  # Perempuan
        return (height_cm - 100) - ((height_cm - 100) * 0.15)  # Rumus berat badan ideal perempuan

# Fungsi untuk memberikan keterangan ideal tidaknya berat badan
def weight_status(weight, ideal_weight_value):
    if weight < ideal_weight_value - 5:
        return "Berat badan Anda di bawah ideal."
    elif weight > ideal_weight_value + 5:
        return "Berat badan Anda di atas ideal."
    else:
        return "Berat badan Anda berada dalam rentang ideal."

# Fungsi untuk memberikan saran
def weight_advice(current_weight, ideal_weight):
    if current_weight < ideal_weight:
        return "Anda perlu menambah berat badan. Pertimbangkan untuk meningkatkan asupan kalori dengan makanan bergizi seperti kacang-kacangan, alpukat, dan protein sehat."
    elif current_weight > ideal_weight:
        return "Anda perlu mengurangi berat badan. Cobalah untuk mengurangi asupan kalori dan meningkatkan aktivitas fisik, seperti berolahraga secara teratur."
    else:
        return "Berat badan Anda sudah ideal. Pertahankan pola makan sehat dan gaya hidup aktif."

# Fungsi untuk mengatur tema
def set_theme(background_color, font_family, font_size):
    st.markdown(
        f"""
        <style>
        body {{
            background-color: {background_color};
            font-family: '{font_family}';
            font-size: {font_size}px;
            color: #000000;  /* Set text color to black */
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Menu utama menggunakan radio button
menu = st.sidebar.radio("Pilih Menu", ["Mulai", "Pengaturan", "Keluar"])

if menu == "Keluar":
    st.write("Yakin ingin keluar aplikasi?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Yakin"):
            st.write("Terima kasih telah menggunakan aplikasi ini!")
            st.stop()
    with col2:
        if st.button("Nanti Dulu"):
            st.write("Anda kembali ke menu utama.")

elif menu == "Pengaturan":
    st.title("Pengaturan Aplikasi")
    
    # Pilihan warna latar belakang
    background_color = st.color_picker("Pilih Warna Latar Belakang:", "#FFFFFF")
    
    # Pilihan font
    font_family = st.selectbox("Pilih Font:", ["Arial", "Courier New", "Georgia", "Times New Roman", "Verdana"])
    
    # Pilihan ukuran font
    font_size = st.slider("Pilih Ukuran Font:", min_value=10, max_value=50, value=16)

    # Tombol untuk menerapkan pengaturan
    if st.button("Terapkan"):
        set_theme(background_color, font_family, font_size)
        st.success("Warna latar belakang, font, dan ukuran font telah diperbarui!")

elif menu == "Mulai":
    st.title("Aplikasi Pemantau Berat Badan Mingguan")

    # Input data dari pengguna
    name = st.text_input("Nama:")
    date = st.date_input("Tanggal:", value=datetime.today())
    initial_weight = st.number_input("Berat Badan Awal (kg):", min_value=0.0, step=0.1)
    initial_height_cm = st.number_input("Tinggi Badan Awal (cm):", min_value=0, step=1)
    age = st.number_input("Umur (tahun):", min_value=0, step=1)
    gender = st.selectbox("Jenis Kelamin:", ["Laki-l aki", "Perempuan"])

    # Tombol untuk mengirim data
    if st.button("Kirim"):
        if name and initial_weight > 0 and initial_height_cm > 0 and age > 0:
            bmi = calculate_bmi(initial_weight, initial_height_cm)
            ideal_weight_value = ideal_weight(gender, initial_height_cm)
            status = weight_status(initial_weight, ideal_weight_value)
            advice = weight_advice(initial_weight, ideal_weight_value)
            st.write(f"Nama: {name}")
            st.write(f"Tanggal: {date}")
            st.write(f"BMI: {bmi:.2f}")
            st.write(f"Berat Badan Ideal: {ideal_weight_value:.2f} kg")
            st.write(status)
            st.write(advice)
            st.session_state.weight_records.append({
                "name": name,
                "date": date,
                "weight": initial_weight,
                "height": initial_height_cm,
                "age": age,
                "gender": gender
            }) 
            st.success("Data berhasil disimpan!")
        else:
            st.error("Silakan lengkapi semua data yang diperlukan.")

        