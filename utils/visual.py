import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
import seaborn as sns
import pandas as pd
import itertools

# 🔹 Palet warna
WARNA_KELOMPOK = {
    "Herbivora": "#006600",
    "Karnivora": "#993300",
    "Koralivora": "#0033FF"
}

WARNA_FAMILI = {
    "Acanthuridae": "#666666",
    "Chaetodontidae": "#0099FF",
    "Serranidae": "#CC0000",
    "Lethrinidae": "#009999",
    "Siganidae": "#F39C12",
    "Haemulidae": "#996633",
    "Lutjanidae": "#9999CC",
    "Scaridae": "#00FF00"
}

def tampilkan_mean_di_kanan_atas(ax, data, warna_teks='darkred'):
    """
    Menampilkan label 'Mean = ...' di atas batang paling kanan (kanan atas grafik).
    """
    if data is None or not len(data):
        return

    mean_val = sum(data) / len(data)
    x_pos = len(data) - 1  # posisi di batang terakhir
    y_pos = max(data) + max(data) * 0.05  # sedikit di atas batang tertinggi

    ax.text(
        x_pos,
        y_pos,
        f"Mean = {mean_val:.2f}",
        ha="center",
        va="bottom",
        fontsize=11,
        fontweight="bold",
        color=warna_teks,
        bbox=dict(facecolor="white", edgecolor="black", boxstyle="round,pad=0.3", alpha=0.8),
        path_effects=[path_effects.withStroke(linewidth=1.2, foreground="white")]
    )

#indeks
def plot_indeks_ekologi(df_indeks):
    df_plot = df_indeks.set_index("Stasiun")[["Shannon", "Evenness", "Simpson"]]

    fig, ax = plt.subplots(figsize=(10, 5))
    df_plot.plot(kind="bar", ax=ax)
    ax.set_title("Indeks Keanekaragaman dan Kemerataan per Stasiun")
    ax.set_ylabel("Nilai Indeks")
    ax.set_xlabel("Stasiun")
    ax.legend(title="Indeks", bbox_to_anchor=(1.05, 1), loc="upper left")
    st.pyplot(fig)

# 🎯 Poin 2
def plot_pie_by_jenis(df_parsed, judul="Komposisi Kelompok berdasarkan Jumlah Spesies"):
    
    # Hitung jumlah spesies unik per kelompok
    data = df_parsed.groupby("Kelompok")["Spesies"].nunique().sort_values(ascending=False)
    colors = [WARNA_KELOMPOK.get(k, "#cccccc") for k in data.index]

    fig, ax = plt.subplots(figsize=(7, 6))

    # Formatter untuk kombinasi persentase dan jumlah jenis
    def format_label(pct, allvals):
        absolute = int(round(pct / 100 * sum(allvals)))
        return f"{pct:.1f}%\n({absolute} jenis)"

    wedges, texts, autotexts = ax.pie(
        data,
        labels=None,
        colors=colors,
        autopct=lambda pct: format_label(pct, data.values),
        startangle=90,
        textprops=dict(color="white", weight="bold", fontsize=9)
    )

    # Tambahkan efek stroke ke label angka agar tetap terbaca
    for autotext in autotexts:
        autotext.set_path_effects([
            path_effects.withStroke(linewidth=1.2, foreground="black")
        ])

    # Tambahkan legend sebagai keterangan warna
    ax.legend(
        wedges,
        data.index,
        title="Kelompok",
        loc="center left",
        bbox_to_anchor=(1, 0.5),
        frameon=False
    )

    ax.set_title(judul)
    st.pyplot(fig)

# 🎯 Poin 3
def plot_pie_by_individu(df_parsed, judul="Komposisi Kelompok berdasarkan Jumlah Individu"):

    # Hitung jumlah individu per kelompok
    data = df_parsed["Kelompok"].value_counts().sort_values(ascending=False)
    colors = [WARNA_KELOMPOK.get(k, "#cccccc") for k in data.index]

    fig, ax = plt.subplots(figsize=(7, 6))

    # Formatter kombinasi persentase dan jumlah individu
    def format_label(pct, allvals):
        absolute = int(round(pct / 100 * sum(allvals)))
        return f"{pct:.1f}%\n({absolute} individu)"

    wedges, texts, autotexts = ax.pie(
        data,
        labels=None,
        colors=colors,
        autopct=lambda pct: format_label(pct, data.values),
        startangle=90,
        textprops=dict(color="white", weight="bold", fontsize=9)
    )

    for autotext in autotexts:
        autotext.set_path_effects([
            path_effects.withStroke(linewidth=1.2, foreground="black")
        ])

    # Legend penjelas warna kelompok
    ax.legend(
        wedges,
        data.index,
        title="Kelompok",
        loc="center left",
        bbox_to_anchor=(1, 0.5),
        frameon=False
    )

    ax.set_title(judul)
    st.pyplot(fig)

# 🎯 Poin 4 keanekaragaman jenis
def plot_keanekaragaman_per_stasiun(df_parsed):
    # Hitung jumlah spesies unik per kelompok per stasiun
    df_grouped = df_parsed.groupby(["Stasiun", "Kelompok"])["Spesies"].nunique().unstack(fill_value=0).sort_index()

    colors = [WARNA_KELOMPOK.get(k, "#CCCCCC") for k in df_grouped.columns]
    fig, ax = plt.subplots(figsize=(10, 6))
    bottom = [0] * len(df_grouped)
    total_per_stasiun = []

    for idx, kelompok in enumerate(df_grouped.columns):
        values = df_grouped[kelompok].values
        ax.bar(df_grouped.index, values, bottom=bottom, color=colors[idx], label=kelompok)

        for i, val in enumerate(values):
            if val > 0:
                ax.text(
                    i,
                    bottom[i] + val / 2,
                    str(int(val)),
                    ha="center",
                    va="center",
                    fontsize=8,
                    color="white",
                    weight="bold",
                    path_effects=[path_effects.withStroke(linewidth=1.2, foreground="black")]
                )
        bottom = [bottom[i] + values[i] for i in range(len(values))]

    for i, total in enumerate(bottom):
        ax.text(
            i,
            total + max(bottom) * 0.02,
            str(int(total)),
            ha="center",
            va="bottom",
            fontsize=9,
            fontweight="bold",
            color="black"
        )
        total_per_stasiun.append(total)  # Kumpulkan total untuk perhitungan rata-rata

    # ✅ Tampilkan rata-rata di posisi kanan atas batang terakhir
    tampilkan_mean_di_kanan_atas(ax, total_per_stasiun)

    ax.set_title("📊 Keanekaragaman Jenis per Stasiun (per Kelompok)", fontsize=12)
    ax.set_ylabel("Jumlah Spesies")
    ax.set_xlabel("Stasiun")
    ax.tick_params(axis='x', rotation=45)
    ax.legend(title="Kelompok", loc="upper right")
    ax.grid(axis="y", linestyle="--", alpha=0.3)

    st.pyplot(fig)
    
def plot_keanekaragaman_koralivora(df_parsed):
    # Filter data hanya untuk kelompok Koralivora
    df_koral = df_parsed[df_parsed["Kelompok"] == "Koralivora"]
    if df_koral.empty:
        st.warning("⚠️ Tidak ada data Koralivora yang dapat ditampilkan.")
        return

    # Hitung jumlah spesies unik per stasiun
    data = df_koral.groupby("Stasiun")["Spesies"].nunique().sort_index()
    warna = WARNA_KELOMPOK.get("Koralivora", "#1E88E5")

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(data.index, data.values, color=warna)

    total_per_stasiun = []  # simpan nilai untuk hitung rata-rata

    # Tambahkan nilai di atas batang
    for i, value in enumerate(data.values):
        ax.text(
            i,
            value + 0.1,
            str(int(value)),
            ha="center",
            va="bottom",
            fontsize=8,
            color="white",
            weight="bold",
            path_effects=[path_effects.withStroke(linewidth=1.2, foreground="black")]
        )
        total_per_stasiun.append(value)

    # 🚀 Tampilkan label rata-rata di kanan atas
    tampilkan_mean_di_kanan_atas(ax, total_per_stasiun)

    ax.set_title("📊 Keanekaragaman Jenis Koralivora per Stasiun")
    ax.set_ylabel("Jumlah Spesies")
    ax.set_xlabel("Stasiun")
    ax.tick_params(axis="x", rotation=45)
    ax.grid(axis="y", linestyle="--", alpha=0.3)

    st.pyplot(fig)

def plot_keanekaragaman_herbivora(df_parsed):
    df_herbi = df_parsed[df_parsed["Kelompok"] == "Herbivora"]
    if df_herbi.empty:
        st.warning("⚠️ Tidak ada data Herbivora.")
        return

    # Hitung jumlah spesies unik per stasiun per famili
    df_grouped = df_herbi.groupby(["Stasiun", "Famili"])["Spesies"].nunique().unstack(fill_value=0)
    df_grouped = df_grouped[df_grouped.sum(axis=1) > 0].sort_index()

    famili_list = df_grouped.columns.tolist()
    colors = [WARNA_FAMILI.get(f, "#999999") for f in famili_list]

    fig, ax = plt.subplots(figsize=(10, 6))
    bottom = [0] * len(df_grouped)

    for idx, famili in enumerate(famili_list):
        values = df_grouped[famili].values
        ax.bar(df_grouped.index, values, bottom=bottom, color=colors[idx], label=famili)

        for i, val in enumerate(values):
            if val > 0:
                ax.text(
                    i,
                    bottom[i] + val / 2,
                    str(int(val)),
                    ha="center",
                    va="center",
                    fontsize=8,
                    color="white",
                    weight="bold",
                    path_effects=[path_effects.withStroke(linewidth=1.2, foreground="black")]
                )

        bottom = [bottom[i] + values[i] for i in range(len(values))]

    max_total = max(bottom)
    for i, total in enumerate(bottom):
        ax.text(
            i,
            total + max_total * 0.02,
            str(int(total)),
            ha="center",
            va="bottom",
            fontsize=9,
            fontweight="bold",
            color="black"
        )

    # ✅ Tampilkan nilai rata-rata di kanan atas batang terakhir
    tampilkan_mean_di_kanan_atas(ax, bottom)

    ax.set_title("📊 Keanekaragaman Jenis Herbivora per Stasiun (berdasarkan Famili)")
    ax.set_ylabel("Jumlah Spesies")
    ax.set_xlabel("Stasiun")
    ax.tick_params(axis='x', rotation=45)
    ax.legend(title="Famili", bbox_to_anchor=(1.01, 1), loc="upper left")
    ax.grid(axis='y', linestyle="--", alpha=0.3)

    st.pyplot(fig)

def plot_keanekaragaman_karnivora(df_parsed):
    df_karni = df_parsed[df_parsed["Kelompok"] == "Karnivora"]
    if df_karni.empty:
        st.warning("⚠️ Tidak ada data Karnivora.")
        return

    # Hitung jumlah spesies unik per stasiun per famili
    df_grouped = df_karni.groupby(["Stasiun", "Famili"])["Spesies"].nunique().unstack(fill_value=0)
    df_grouped = df_grouped[df_grouped.sum(axis=1) > 0].sort_index()

    famili_list = df_grouped.columns.tolist()
    colors = [WARNA_FAMILI.get(fam, "#999999") for fam in famili_list]

    fig, ax = plt.subplots(figsize=(10, 6))
    bottom = [0] * len(df_grouped)

    for idx, famili in enumerate(famili_list):
        values = df_grouped[famili].values
        ax.bar(df_grouped.index, values, bottom=bottom, color=colors[idx], label=famili)

        # Label jumlah dalam segmen batang
        for i, val in enumerate(values):
            if val > 0:
                ax.text(
                    i,
                    bottom[i] + val / 2,
                    str(int(val)),
                    ha="center",
                    va="center",
                    fontsize=8,
                    color="white",
                    weight="bold",
                    path_effects=[path_effects.withStroke(linewidth=1.2, foreground="black")]
                )

        bottom = [bottom[i] + values[i] for i in range(len(values))]

    max_total = max(bottom)
    for i, total in enumerate(bottom):
        ax.text(
            i,
            total + max_total * 0.02,
            str(int(total)),
            ha="center",
            va="bottom",
            fontsize=9,
            fontweight="bold",
            color="black"
        )

    # ✅ Tampilkan rata-rata di kanan atas batang terakhir
    tampilkan_mean_di_kanan_atas(ax, bottom)

    ax.set_title("📊 Keanekaragaman Jenis Karnivora per Stasiun (berdasarkan Famili)")
    ax.set_ylabel("Jumlah Spesies")
    ax.set_xlabel("Stasiun")
    ax.tick_params(axis='x', rotation=45)
    ax.legend(title="Famili", bbox_to_anchor=(1.01, 1), loc="upper left")
    ax.grid(axis='y', linestyle="--", alpha=0.3)

    st.pyplot(fig)

def plot_individu_per_stasiun(df_parsed):
    data = df_parsed["Stasiun"].value_counts().sort_index()
    fig, ax = plt.subplots()
    data.plot(kind="bar", ax=ax, color="#00897B")
    ax.set_title("Jumlah Individu per Stasiun")
    ax.set_ylabel("Jumlah Individu")
    ax.set_xlabel("Stasiun")
    st.pyplot(fig)

def plot_kelimpahan_per_stasiun(df, konversi_func=None, mode_tampilan="Data Terkonversi"):
    # Hitung jumlah individu per kelompok per stasiun
    grouped = df.groupby(["Stasiun", "Kelompok"]).size().unstack(fill_value=0).sort_index()
    data = konversi_func(grouped) if konversi_func else grouped

    colors = [WARNA_KELOMPOK.get(k, "#cccccc") for k in data.columns]
    fig, ax = plt.subplots(figsize=(10, 6))
    bottom = [0] * len(data)
    total_per_stasiun = []

    for idx, kelompok in enumerate(data.columns):
        values = data[kelompok].values
        ax.bar(data.index, values, bottom=bottom, color=colors[idx], label=kelompok)

        for i, val in enumerate(values):
            if val > 0:
                ax.text(
                    i,
                    bottom[i] + val / 2,
                    str(int(round(val))),
                    ha="center",
                    va="center",
                    fontsize=8,
                    color="white",
                    weight="bold",
                    path_effects=[path_effects.withStroke(linewidth=1.2, foreground="black")]
                )

        bottom = [bottom[i] + values[i] for i in range(len(values))]

    total_max = max(bottom)
    for i, total in enumerate(bottom):
        ax.text(
            i,
            total + total_max * 0.02,
            str(int(round(total))),
            ha="center",
            va="bottom",
            fontsize=9,
            fontweight="bold",
            color="black"
        )
        total_per_stasiun.append(total)

    # ✅ Tampilkan rata-rata di kanan atas batang terakhir
    tampilkan_mean_di_kanan_atas(ax, total_per_stasiun)

    satuan = "Individu per Hektar" if mode_tampilan == "Data Terkonversi" else "Individu per 350 m²"
    ax.set_title("📊 Kelimpahan per Kelompok di Tiap Stasiun")
    ax.set_ylabel(satuan)
    ax.set_xlabel("Stasiun")
    ax.tick_params(axis='x', rotation=45)
    ax.legend(title="Kelompok", bbox_to_anchor=(1.05, 1), loc="upper left")
    ax.grid(axis='y', linestyle="--", alpha=0.3)
    st.pyplot(fig)

def plot_kelimpahan_koralivora(df, konversi_func=None, mode_tampilan="Data Terkonversi"):
    df_koral = df[df["Kelompok"] == "Koralivora"]
    if df_koral.empty:
        st.warning("⚠️ Tidak ada data kelompok Koralivora.")
        return

    grouped = df_koral.groupby(["Stasiun", "Famili"]).size().unstack(fill_value=0).sort_index()
    data = konversi_func(grouped) if konversi_func else grouped
    colors = [WARNA_FAMILI.get(f, "#cccccc") for f in data.columns]

    fig, ax = plt.subplots(figsize=(10, 5))
    bottom = [0] * len(data)
    total_per_stasiun = []

    for idx, famili in enumerate(data.columns):
        values = data[famili].values
        ax.bar(data.index, values, bottom=bottom, color=colors[idx], label=famili)

        for i, val in enumerate(values):
            if val > 0:
                ax.text(
                    i,
                    bottom[i] + val / 2,
                    str(int(round(val))),
                    ha="center",
                    va="center",
                    fontsize=8,
                    color="white",
                    weight="bold",
                    path_effects=[path_effects.withStroke(linewidth=1.2, foreground="black")]
                )

        bottom = [bottom[i] + values[i] for i in range(len(bottom))]

    # ✅ Hitung total dan tampilkan label rata-rata
    total_per_stasiun = bottom
    tampilkan_mean_di_kanan_atas(ax, total_per_stasiun)

    y_label = "Individu per Hektar" if mode_tampilan == "Data Terkonversi" else "Individu per 350 m²"
    ax.set_title("📊 Kelimpahan Koralivora per Famili")
    ax.set_ylabel(y_label)
    ax.set_xlabel("Stasiun")
    ax.tick_params(axis="x", rotation=45)
    ax.legend(title="Famili", bbox_to_anchor=(1.05, 1), loc="upper left")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    st.pyplot(fig)

def plot_kelimpahan_herbivora_famili(df, konversi_func=None, mode_tampilan="Data Terkonversi"):
    df_herbi = df[df["Kelompok"] == "Herbivora"]
    if df_herbi.empty:
        st.warning("⚠️ Tidak ada data Herbivora.")
        return

    grouped = df_herbi.groupby(["Stasiun", "Famili"]).size().unstack(fill_value=0).sort_index()
    data = konversi_func(grouped) if konversi_func else grouped

    colors = [WARNA_FAMILI.get(f, "#cccccc") for f in data.columns]
    fig, ax = plt.subplots(figsize=(10, 5))
    bottom = [0] * len(data)
    total_per_stasiun = []

    for idx, famili in enumerate(data.columns):
        values = data[famili].values
        ax.bar(data.index, values, bottom=bottom, color=colors[idx], label=famili)

        for i, val in enumerate(values):
            if val > 0:
                ax.text(
                    i,
                    bottom[i] + val / 2,
                    str(int(round(val))),
                    ha="center",
                    va="center",
                    fontsize=8,
                    color="white",
                    weight="bold",
                    path_effects=[path_effects.withStroke(linewidth=1.2, foreground="black")]
                )

        bottom = [bottom[i] + values[i] for i in range(len(values))]

    total_max = max(bottom)
    for i, total in enumerate(bottom):
        ax.text(
            i,
            total + total_max * 0.02,
            str(int(round(total))),
            ha="center",
            va="bottom",
            fontsize=9,
            fontweight="bold",
            color="black"
        )
        total_per_stasiun.append(total)

    # ✅ Gunakan bottom sebagai input ke label rata-rata
    tampilkan_mean_di_kanan_atas(ax, total_per_stasiun)

    satuan = "Individu per Hektar" if mode_tampilan == "Data Terkonversi" else "Individu per 350 m²"
    ax.set_title("📊 Kelimpahan Herbivora per Famili")
    ax.set_ylabel(satuan)
    ax.set_xlabel("Stasiun")
    ax.tick_params(axis="x", rotation=45)
    ax.legend(title="Famili", bbox_to_anchor=(1.05, 1), loc="upper left")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    st.pyplot(fig)

def plot_kelimpahan_karnivora_famili(df, konversi_func=None, mode_tampilan="Data Terkonversi"):
    df_karni = df[df["Kelompok"] == "Karnivora"]
    if df_karni.empty:
        st.warning("⚠️ Tidak ada data Karnivora.")
        return

    # Hitung kelimpahan individu per famili per stasiun
    grouped = df_karni.groupby(["Stasiun", "Famili"]).size().unstack(fill_value=0).sort_index()
    data = konversi_func(grouped) if konversi_func else grouped
    colors = [WARNA_FAMILI.get(f, "#cccccc") for f in data.columns]

    fig, ax = plt.subplots(figsize=(10, 5))
    bottom = [0] * len(data)
    total_per_stasiun = []

    for idx, famili in enumerate(data.columns):
        values = data[famili].values
        ax.bar(data.index, values, bottom=bottom, color=colors[idx], label=famili)

        for i, val in enumerate(values):
            if val > 0:
                ax.text(
                    i,
                    bottom[i] + val / 2,
                    str(int(round(val))),
                    ha="center",
                    va="center",
                    fontsize=8,
                    color="white",
                    weight="bold",
                    path_effects=[path_effects.withStroke(linewidth=1.2, foreground="black")]
                )

        bottom = [bottom[i] + values[i] for i in range(len(values))]

    max_total = max(bottom)
    for i, total in enumerate(bottom):
        ax.text(
            i,
            total + max_total * 0.02,
            str(int(round(total))),
            ha="center",
            va="bottom",
            fontsize=9,
            fontweight="bold",
            color="black"
        )
        total_per_stasiun.append(total)

    # ✅ Tampilkan rata-rata dengan input yang benar
    tampilkan_mean_di_kanan_atas(ax, total_per_stasiun)

    y_label = "Individu per Hektar" if mode_tampilan == "Data Terkonversi" else "Individu per 350 m²"
    ax.set_title("📊 Kelimpahan Karnivora per Famili")
    ax.set_ylabel(y_label)
    ax.set_xlabel("Stasiun")
    ax.tick_params(axis="x", rotation=45)
    ax.legend(title="Famili", bbox_to_anchor=(1.05, 1), loc="upper left")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    st.pyplot(fig)

def plot_biomassa_per_stasiun(df_merge, mode_tampilan="Data Terkonversi"):
    df_valid = df_merge[
        df_merge["Biomassa"].notna() & df_merge["Kelompok"].isin(["Herbivora", "Karnivora"])
    ]
    if df_valid.empty:
        st.warning("⚠️ Tidak ada data biomassa Herbivora/Karnivora yang valid.")
        return

    grouped = df_valid.groupby(["Stasiun", "Kelompok"])["Biomassa"].sum().unstack(fill_value=0).sort_index()
    colors = [WARNA_KELOMPOK.get(k, "#cccccc") for k in grouped.columns]

    fig, ax = plt.subplots(figsize=(10, 6))
    bottom = [0] * len(grouped)
    total_per_stasiun = []

    for idx, kelompok in enumerate(grouped.columns):
        values = grouped[kelompok].values
        ax.bar(grouped.index, values, bottom=bottom, color=colors[idx], label=kelompok)

        for i, val in enumerate(values):
            if val > 0:
                ax.text(
                    i,
                    bottom[i] + val / 2,
                    f"{val:.1f}",
                    ha="center",
                    va="center",
                    fontsize=8,
                    color="white",
                    weight="bold",
                    path_effects=[path_effects.withStroke(linewidth=1.2, foreground="black")]
                )

        bottom = [bottom[i] + values[i] for i in range(len(values))]

    max_y = max(bottom)
    for i, total in enumerate(bottom):
        ax.text(
            i,
            total + max_y * 0.02,
            f"{total:.1f}",
            ha="center",
            va="bottom",
            fontsize=9,
            fontweight="bold",
            color="black"
        )
        total_per_stasiun.append(total)

    # ✅ Ganti dari data.values ke bottom
    tampilkan_mean_di_kanan_atas(ax, total_per_stasiun)

    label_y = "Total Biomassa (kg/ha)" if mode_tampilan == "Data Terkonversi" else "Total Biomassa (g)"
    ax.set_title("📊 Biomassa Herbivora dan Karnivora per Stasiun")
    ax.set_ylabel(label_y)
    ax.set_xlabel("Stasiun")
    ax.tick_params(axis="x", rotation=45)
    ax.legend(title="Kelompok", bbox_to_anchor=(1.05, 1), loc="upper left")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    st.pyplot(fig)

def plot_biomassa_by_kelompok(df_merge):
    df_valid = df_merge[df_merge["Biomassa"].notna()]
    if df_valid.empty:
        st.warning("⚠️ Tidak ada data biomassa untuk kelompok.")
        return

    # Hitung total biomassa per kelompok
    data = df_valid.groupby("Kelompok")["Biomassa"].sum().sort_values(ascending=False)
    colors = [WARNA_KELOMPOK.get(k, "#cccccc") for k in data.index]
    total_per_kelompok = data.values  # ✅ pastikan array 1D

    fig, ax = plt.subplots()
    data.plot(kind="bar", ax=ax, color=colors)

    tampilkan_mean_di_kanan_atas(ax, total_per_kelompok)

    ax.set_title("📊 Biomassa Berdasarkan Kelompok")
    ax.set_ylabel("Biomassa (g)")
    ax.set_xlabel("Kelompok")
    ax.tick_params(axis="x", rotation=0)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    st.pyplot(fig)


def plot_biomassa_famili(df_merge, target_kelompok, mode_tampilan="Data Terkonversi"):
    df_valid = df_merge[
        (df_merge["Kelompok"] == target_kelompok) & df_merge["Biomassa"].notna()
    ]
    if df_valid.empty:
        st.warning(f"⚠️ Tidak ada data biomassa {target_kelompok}.")
        return

    grouped = df_valid.groupby(["Stasiun", "Famili"])["Biomassa"].sum().unstack(fill_value=0).sort_index()
    colors = [WARNA_FAMILI.get(f, "#cccccc") for f in grouped.columns]

    fig, ax = plt.subplots(figsize=(10, 6))
    bottom = [0] * len(grouped)
    total_per_stasiun = []

    for idx, famili in enumerate(grouped.columns):
        values = grouped[famili].values
        ax.bar(grouped.index, values, bottom=bottom, color=colors[idx], label=famili)

        for i, val in enumerate(values):
            if val > 0:
                ax.text(
                    i, bottom[i] + val / 2, f"{val:.1f}",
                    ha="center", va="center",
                    fontsize=8, color="white", weight="bold",
                    path_effects=[path_effects.withStroke(linewidth=1.2, foreground="black")]
                )

        bottom = [bottom[i] + values[i] for i in range(len(values))]

    max_y = max(bottom)
    for i, total in enumerate(bottom):
        ax.text(
            i, total + max_y * 0.02, f"{total:.1f}",
            ha="center", va="bottom",
            fontsize=9, fontweight="bold", color="black"
        )
        total_per_stasiun.append(total)

    # ✅ Tampilkan mean biomassa di kanan atas batang terakhir
    tampilkan_mean_di_kanan_atas(ax, total_per_stasiun)

    label_y = "Total Biomassa (kg/ha)" if mode_tampilan == "Data Terkonversi" else "Total Biomassa (g)"
    ax.set_title(f"📊 Biomassa {target_kelompok} per Famili di Tiap Stasiun")
    ax.set_ylabel(label_y)
    ax.set_xlabel("Stasiun")
    ax.tick_params(axis='x', rotation=45)
    ax.legend(title="Famili", bbox_to_anchor=(1.05, 1), loc="upper left")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    st.pyplot(fig)


def plot_biomassa_by_spesies(df_merge):
    df_valid = df_merge[df_merge["Biomassa"].notna()]
    if df_valid.empty:
        st.warning("⚠️ Tidak ada data biomassa untuk spesies.")
        return

    # Ambil 10 spesies dengan biomassa tertinggi
    data = df_valid.groupby("Spesies")["Biomassa"].sum().sort_values(ascending=False).head(10)
    total_biomassa = data.values  # ✅ pastikan array 1D

    fig, ax = plt.subplots()
    data.plot(kind="bar", ax=ax, color="#546E7A")

    tampilkan_mean_di_kanan_atas(ax, total_biomassa)

    ax.set_title("📊 Top 10 Spesies dengan Biomassa Tertinggi")
    ax.set_ylabel("Biomassa (g)")
    ax.set_xlabel("Spesies")
    ax.tick_params(axis="x", rotation=45)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    st.pyplot(fig)