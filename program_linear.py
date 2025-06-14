import streamlit as st
from scipy.optimize import linprog
import matplotlib.pyplot as plt
import numpy as np

st.title("🔧 Optimasi Biaya Produksi Roti")
st.write("Aplikasi ini menghitung jumlah optimal Roti Manis dan Tawar untuk meminimalkan biaya produksi.")

# Input pengguna
st.sidebar.header("Input Parameter Produksi")

max_kapasitas = st.sidebar.number_input("Kapasitas Produksi Maksimum (unit)", min_value=1, value=1000)
budget = st.sidebar.number_input("Anggaran Maksimal (Rp)", min_value=1, value=1800000)

harga_roti_manis = st.sidebar.number_input("Biaya/unit Roti Manis (Rp)", min_value=1, value=2000)
harga_roti_tawar = st.sidebar.number_input("Biaya/unit Roti Tawar (Rp)", min_value=1, value=1500)

permintaan_min_manis = st.sidebar.number_input("Permintaan Min Roti Manis", min_value=0, value=300)
permintaan_min_tawar = st.sidebar.number_input("Permintaan Min Roti Tawar", min_value=0, value=400)

if st.button("🔍 Hitung Optimasi"):
    # Fungsi objektif
    c = [harga_roti_manis, harga_roti_tawar]

    # Kendala
    A = [
        [1, 1],  # kapasitas produksi
        [harga_roti_manis, harga_roti_tawar]  # biaya
    ]
    b = [max_kapasitas, budget]

    bounds = [(permintaan_min_manis, None), (permintaan_min_tawar, None)]

    res = linprog(c=c, A_ub=A, b_ub=b, bounds=bounds, method='highs')

    if res.success:
        x_opt = res.x[0]
        y_opt = res.x[1]
        total_cost = c[0]*x_opt + c[1]*y_opt

        st.success("✔ Optimasi Berhasil!")
        st.write(f"**Roti Manis**: {x_opt:.0f} unit")
        st.write(f"**Roti Tawar**: {y_opt:.0f} unit")
        st.write(f"**Total Biaya**: Rp{int(total_cost):,}")

        # ---------- Visualisasi ----------
        fig, ax = plt.subplots(figsize=(8, 6))

        x_vals = np.linspace(permintaan_min_manis, max_kapasitas, 400)

        # Garis kendala kapasitas
        y1 = max_kapasitas - x_vals
        ax.plot(x_vals, y1, label="Kapasitas: x + y ≤ {}".format(max_kapasitas), color='blue')

        # Garis kendala biaya
        y2 = (budget - harga_roti_manis * x_vals) / harga_roti_tawar
        ax.plot(x_vals, y2, label="Anggaran: {}x + {}y ≤ {}".format(harga_roti_manis, harga_roti_tawar, budget), color='green')

        # Plot batas minimum
        ax.axvline(permintaan_min_manis, linestyle='--', color='orange', label="Min Roti Manis")
        ax.axhline(permintaan_min_tawar, linestyle='--', color='purple', label="Min Roti Tawar")

        # Plot titik optimal
        ax.plot(x_opt, y_opt, 'ro', label="Titik Optimal")

        ax.set_xlim(0, max_kapasitas + 100)
        ax.set_ylim(0, max_kapasitas + 100)
        ax.set_xlabel("Roti Manis (x)")
        ax.set_ylabel("Roti Tawar (y)")
        ax.set_title("Visualisasi Optimasi Produksi")
        ax.legend()
        ax.grid(True)

        st.pyplot(fig)

    else:
        st.error("❌ Optimasi gagal. Silakan periksa parameter input.")
