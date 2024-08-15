import streamlit as st
import pandas as pd
import plotly.express as px
from statsmodels.tsa.arima.model import ARIMA
import plotly.graph_objs as go

# Judul Aplikasi Streamlit
st.title("Dashboard Tingkat Inflasi")

# Tentukan jalur ke file lokal Anda
file_path = '1/final-tingkat-inflasi-bulan-ke-bulan-provinsi-aceh.csv'
file_path_2 = 'tingkat-inflasi-tahun-ke-tahun-menurut-kabupaten-kota.csv'

# Baca file CSV
df = pd.read_csv(file_path, delimiter=',')
df_2 = pd.read_csv(file_path_2, delimiter=',')

# Sidebar untuk memilih fitur
st.sidebar.title("Opsi")
feature = st.sidebar.selectbox(
    "Pilih Fitur",
    ("Visualisasi Inflasi Bulanan", "Prediksi Inflasi", "Inflasi Berdasarkan Wilayah")
)

if feature == "Inflasi Berdasarkan Wilayah":
    st.subheader("Inflasi Berdasarkan Wilayah")

    # Memilih tahun tertentu
    year_options = sorted(df_2['tahun'].unique().tolist())
    selected_year = st.selectbox("Pilih Tahun", options=year_options)

    # Memfilter data berdasarkan tahun yang dipilih
    df_filtered = df_2[df_2['tahun'] == int(selected_year)]

    # Definisikan skala warna kustom
    color_sequence = ['red', 'yellow', 'blue']

    # Membuat grafik garis dengan Plotly
    fig = px.line(
        df_filtered,
        x='bulan',
        y='tingkat_inflasi_tahun_ke_tahun',
        color='bps_nama_kabupaten_kota',
        title=f'Tingkat Inflasi Berdasarkan Wilayah ({selected_year})',
        labels={'bulan': 'Bulan', 'tingkat_inflasi_tahun_ke_tahun': 'Tingkat Inflasi (%)'},
        markers=True,
        line_shape='linear',
        color_discrete_sequence=color_sequence  # Terapkan warna kustom
    )

    # Memperbarui tata letak untuk visualisasi yang lebih baik
    fig.update_layout(
        xaxis_title='Bulan',
        yaxis_title='Tingkat Inflasi (%)',
        hovermode='x unified'  # Menampilkan nilai semua garis saat hover
    )

    # Tampilkan grafik di Streamlit
    st.plotly_chart(fig)

       # Menampilkan informasi tambahan di bawah grafik
    st.write(f"Grafik di atas menunjukkan perubahan tingkat inflasi tahunan di setiap kabupaten/kota di tahun {selected_year}. Perubahan tingkat inflasi ini memberikan gambaran mengenai fluktuasi harga barang dan jasa di berbagai wilayah sepanjang tahun {selected_year}.")

    # Menambahkan visualisasi rata-rata inflasi tahunan
    st.subheader("Rata-Rata Inflasi Tahunan Berdasarkan Wilayah (2013-2023)")

    # Menghitung rata-rata inflasi per bulan dan menggabungkan menjadi inflasi tahunan
    df_aggregated = df_2.groupby(['tahun', 'bps_nama_kabupaten_kota'])['tingkat_inflasi_tahun_ke_tahun'].mean().reset_index()
    
    # Membuat grafik garis dengan Plotly untuk data tahunan yang telah digabungkan
    fig_aggregated = px.line(
        df_aggregated,
        x='tahun',
        y='tingkat_inflasi_tahun_ke_tahun',
        color='bps_nama_kabupaten_kota',
        title='Rata-Rata Inflasi Tahunan Berdasarkan Wilayah (2013-2023)',
        labels={'tahun': 'Tahun', 'tingkat_inflasi_tahun_ke_tahun': 'Tingkat Inflasi (%)'},
        markers=True,
        line_shape='linear',
        color_discrete_sequence=color_sequence  # Terapkan warna kustom
    )

    # Memperbarui tata letak untuk visualisasi yang lebih baik
    fig_aggregated.update_layout(
        xaxis_title='Tahun',
        yaxis_title='Tingkat Inflasi (%)',
        hovermode='x unified',  # Menampilkan nilai semua garis saat hover
        xaxis=dict(tickmode='linear', tick0=2013, dtick=1)  # Menampilkan setiap tahun pada sumbu x
    )

    # Tampilkan grafik di Streamlit
    st.plotly_chart(fig_aggregated)

    # Menampilkan kesimpulan di bawah grafik
    st.write("""
    **Kesimpulan:**
    - Semua wilayah mengalami fluktuasi signifikan dalam tingkat inflasi tahunan dari 2013 hingga 2023.
    - Banda Aceh menunjukkan lonjakan signifikan pada 2014 dan 2022 dengan penurunan besar pada 2017.
    - Lhokseumawe mengikuti tren serupa dengan peningkatan tajam pada 2014 dan 2022.
    - Meulaboh memiliki inflasi yang lebih tinggi pada 2013, dengan tren yang lebih stabil dari 2017 hingga 2020 dibandingkan wilayah lainnya.
    - Puncak inflasi pada 2022 di semua wilayah menunjukkan adanya faktor eksternal yang mempengaruhi inflasi tahun tersebut.
    """)

elif feature == "Visualisasi Inflasi Bulanan":
    st.subheader("Visualisasi Tingkat Inflasi Bulanan")

    # Tampilkan beberapa baris pertama dari DataFrame
    st.write("Beberapa baris pertama dari dataset:")
    st.dataframe(df.head())

    # Memfilter data untuk tahun 2013 hingga 2023
    df_filtered = df[(df['tahun'] >= 2013) & (df['tahun'] <= 2023)]

    # Menghitung rata-rata bergerak untuk DataFrame yang difilter
    df_filtered['moving_avg'] = df_filtered['tingkat_inflasi_bulanan'].rolling(window=3).mean()

    # Membuat kamus untuk menyimpan data setiap tahun
    dfs = {}
    for year in range(2013, 2024):
        dfs[year] = df_filtered[df_filtered['tahun'] == year]

    # Pilih tahun untuk visualisasi
    year = st.selectbox("Pilih Tahun", options=list(range(2014, 2024)))

    # Akses DataFrame tahun yang dipilih
    data_to_plot = dfs[year]
    title = f'Tingkat Inflasi Bulanan di {year} per Provinsi'

    # Membuat grafik garis dengan data yang dipilih
    fig = px.line(
        data_to_plot,
        x='bulan',
        y=['tingkat_inflasi_bulanan', 'moving_avg'],
        title=title,
        labels={'bulan': 'Bulan', 'value': 'Tingkat Inflasi (%)'},
        markers=True,
        line_shape='linear',
    )

    # Kustomisasi warna garis rata-rata bergerak
    fig.update_traces(selector=dict(name='moving_avg'), line=dict(color='red'))

    # Tampilkan grafik di Streamlit
    st.plotly_chart(fig)

    # Menampilkan informasi tambahan di bawah grafik
    st.write(f"Grafik ini menampilkan tingkat inflasi bulanan untuk tahun {year}. Garis merah menunjukkan rata-rata bergerak, yang memberikan gambaran umum tentang tren inflasi selama tiga bulan terakhir. Ini membantu dalam mengidentifikasi pola dan anomali yang mungkin terjadi dalam periode tersebut.")

elif feature == "Prediksi Inflasi":
    st.subheader("Prediksi Inflasi")

    # Pemetaan bulan Indonesia ke bahasa Inggris
    month_map = {
        'Januari': 'January', 'Februari': 'February', 'Maret': 'March', 'April': 'April', 'Mei': 'May',
        'Juni': 'June', 'Juli': 'July', 'Agustus': 'August', 'September': 'September', 'Oktober': 'October',
        'November': 'November', 'Desember': 'December'
    }
    df['bulan'] = df['bulan'].map(month_map)

    # Gabungkan 'tahun' dan 'bulan' untuk membentuk indeks tanggal
    df['Date'] = pd.to_datetime(df['bulan'] + ' ' + df['tahun'].astype(str))
    df.set_index('Date', inplace=True)

    # Opsi untuk menentukan jumlah bulan untuk prediksi
    n_months = st.number_input('Jumlah bulan untuk prediksi', min_value=1, max_value=12, value=5)

    # Fit model ARIMA menggunakan semua data
    model = ARIMA(df['tingkat_inflasi_bulanan'], order=(1, 1, 1))  # Sesuaikan order jika perlu
    model_fit = model.fit()

    # Prediksi inflasi untuk n_months ke depan menggunakan ARIMA
    next_n_months_prediction = model_fit.forecast(steps=n_months)
    st.write(f"Prediksi inflasi untuk {n_months} bulan ke depan (ARIMA):")
    st.write(next_n_months_prediction)

    # Linear Regression model for prediction
    from sklearn.linear_model import LinearRegression
    import numpy as np

    # Prepare data for Linear Regression
    df['Month_Num'] = np.arange(len(df))  # Add a numeric month index
    X = df[['Month_Num']].values
    y = df['tingkat_inflasi_bulanan'].values

    # Fit the Linear Regression model
    lr_model = LinearRegression()
    lr_model.fit(X, y)

    # Predict future inflation using Linear Regression
    future_months = np.arange(len(df), len(df) + n_months).reshape(-1, 1)
    lr_predictions = lr_model.predict(future_months)
    
    st.write(f"Prediksi inflasi untuk {n_months} bulan ke depan (Linear Regression):")
    st.write(lr_predictions)

    # Memfilter data untuk tahun 2023
    df_2023 = df[df['tahun'] == 2023]

    # Membuat rentang tanggal baru untuk n_months ke depan, mulai dari tanggal 1 setiap bulan
    future_dates = pd.date_range(start=df_2023.index[-1] + pd.DateOffset(months=1), periods=n_months, freq='MS')

    # Membuat trace untuk nilai aktual, prediksi ARIMA, dan prediksi Linear Regression
    actual_trace = go.Scatter(x=df_2023.index, y=df_2023['tingkat_inflasi_bulanan'], mode='lines+markers', name='Aktual 2023')
    predicted_trace_arima = go.Scatter(x=future_dates, y=next_n_months_prediction, mode='lines+markers', name='Prediksi ARIMA', marker=dict(color='red'))
    predicted_trace_lr = go.Scatter(x=future_dates, y=lr_predictions, mode='lines+markers', name='Prediksi Linear Regression', marker=dict(color='blue'))

    # Membuat layout
    layout = go.Layout(
        title='Tingkat Inflasi untuk 2023 dan Bulan-Bulan Berikutnya',
        xaxis=dict(title='Bulan'),
        yaxis=dict(title='Tingkat Inflasi (%)')
    )

    # Membuat grafik dan menambahkan trace
    fig = go.Figure(data=[actual_trace, predicted_trace_arima, predicted_trace_lr], layout=layout)

    # Tampilkan grafik di Streamlit
    st.plotly_chart(fig)

    # Menampilkan informasi tambahan di bawah grafik
    st.write(f"Grafik ini menunjukkan tingkat inflasi aktual pada tahun 2023 dan prediksi untuk {n_months} bulan berikutnya menggunakan model ARIMA dan Linear Regression. Prediksi ini membantu memberikan gambaran mengenai kemungkinan tren inflasi di masa depan berdasarkan data historis.")

    # Penjelasan tentang algoritma ARIMA
    st.write("""
        **Tentang Algoritma ARIMA**: 
        Model ARIMA (AutoRegressive Integrated Moving Average) adalah salah satu model statistik yang paling banyak digunakan untuk menganalisis dan memprediksi data deret waktu, seperti tingkat inflasi. 
        ARIMA terdiri dari tiga komponen utama:
        - **AR (AutoRegressive)**: Komponen ini menggunakan hubungan ketergantungan antara pengamatan saat ini dengan pengamatan sebelumnya.
        - **I (Integrated)**: Bagian ini mengindikasikan bahwa data telah melalui proses differencing untuk membuat data menjadi stasioner.
        - **MA (Moving Average)**: Komponen ini memanfaatkan ketergantungan antara pengamatan dan kesalahan residual dari model.
        Dengan memodelkan inflasi menggunakan ARIMA, kita dapat menangkap pola masa lalu untuk memprediksi tingkat inflasi di masa depan.
    """)

    # Penjelasan tentang algoritma Linear Regression
    st.write("""
        **Tentang Algoritma Linear Regression**: 
        Linear Regression adalah model statistik yang digunakan untuk memahami hubungan antara variabel dependen dan satu atau lebih variabel independen. Dalam konteks ini, model ini memprediksi tingkat inflasi masa depan berdasarkan tren linear dari data historis. 
        Linear Regression berasumsi bahwa ada hubungan linier antara waktu dan tingkat inflasi, yang membuatnya efektif dalam situasi di mana inflasi tumbuh atau menurun secara stabil dari waktu ke waktu.
    """)
