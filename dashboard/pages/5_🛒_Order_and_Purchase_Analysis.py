import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import os
from folium.plugins import HeatMap
from streamlit_folium import folium_static
from streamlit_option_menu import option_menu
from babel.numbers import format_currency

st.set_page_config(
    page_title="Order and Purchase",
    page_icon="🛒",
)

path = os.path.dirname(__file__)
my_file = path+'/../all_data.csv'
all_df = pd.read_csv(my_file)
datetime_columns = ["order_approved_at", "order_delivered_customer_date"]
all_df.sort_values(by="order_approved_at", inplace=True)
all_df.reset_index(inplace=True)

def df_delivery_Status(df):
    df_delivery_Status = df.groupby(by="delivery_status").agg({
        "order_id": "count"
    }).sort_values(by="order_id",ascending=False).reset_index()
    
    return df_delivery_Status

def df_payment_type(df):
    df_payment_type = df.groupby(by="payment_type").agg({
        "customer_id": "count",
    }).reset_index()
    
    return df_payment_type

def df_product_sales(df):

    df_product_sales = all_df.groupby(by="order_purchase_time").agg({
        "customer_id": "count"
    }).sort_values(by="customer_id",ascending=False).reset_index()
    
    return df_product_sales

with st.sidebar:
    selected = option_menu(
        menu_title="Order and Purchase",
        options=["Order Delivery Status","Payment Type","Purchase Time"],
    )

if selected == "Order Delivery Status":
    st.title("Order Delivery Status")

    df_delivery_Status = df_delivery_Status(all_df)

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df_delivery_Status['delivery_status'],
        y=df_delivery_Status['order_id'],
        text=df_delivery_Status['order_id'],  # Menambahkan label di setiap bar
        textposition='outside',  # Menampilkan label di luar bar
        textfont=dict(
            color='white',  # Mengatur warna teks menjadi putih
        ),
        marker=dict(
            color='rgb(173, 216, 230)',  # Set color here
        ),
    ))

    fig.update_layout(
        title='Order Delivery Status Over 2016 - 2018',
        xaxis=dict(title='Product Name', tickangle=45),
        yaxis=dict(title='Total Sales'),
        showlegend=False,
        width=700,
        height=500,
    )

    st.plotly_chart(fig)

    with st.expander("Interpretasi", expanded=False):
        # Konten expander
        st.write("- Hampir ebagian besar produk yaitu sejumlah 106893 produk yang terjual berhasil sampai ke pelanggan dengan tepat waktu.")
        st.write("- Masih ada sebesar 8715 barang yang masih terlambat untuk sampai ke pelanggan.")

    with st.expander("Saran", expanded=False):
        # Konten expander
        st.write("- Karena perbandingan antara pengiriman yang tepat waktu jauh lebih banyak daripada pengiriman terlambat maka secara keseluruhan sudah baik dari segi pelayanan. Untuk pengiriman yang terlambat dapat di evaluasi lagi apakah itu karena kurir atau kesalahan sistem, ")



if selected == "Payment Type":
    
    st.title("Customer Payment Type")
    df_payment_type = df_payment_type(all_df)
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df_payment_type['payment_type'],
        y=df_payment_type['customer_id'],
        text=df_payment_type['customer_id'],  # Menambahkan label di setiap bar
        textposition='outside',  # Menampilkan label di luar bar
        textfont=dict(
            color='white',  # Mengatur warna teks menjadi putih
        ),
        marker=dict(
            color='rgb(173, 216, 230)',  # Set color here
        ),
    ))

    fig.update_layout(
        title='Customer Payment Type Over 2016 - 2018',
        xaxis=dict(title='Product Name', tickangle=45),
        yaxis=dict(title='Total Sales'),
        showlegend=False,
        width=700,
        height=500,
    )

    st.plotly_chart(fig)

    with st.expander("Interpretasi", expanded=False):

            # Konten expander
            st.write("- Jenis pembayaran yang paling banyak digunakan pelanggan adalah credit card dan juga boleto dengan jumlah transaksi sebanyak 85277 dan 22510 transaksi pada masing - masing jenis pembayaran tersbut.")
            st.write("- Jenis pembayaran yang paling sedikit digunakan pelanggan adalah debit card dan voucher yaitu hanya sebesar 1659 dan 6162 transaksi pada masing - masing jenis pembayaran tersbut.")
    
    with st.expander("Saran", expanded=False):

            # Konten expander
            st.write("Promosi dan Insentif : ")
            st.write("- Untuk mendorong penggunaan jenis pembayaran yang paling sedikit digunakan, Dapat dibuat promosi atau memberikan insentif khusus. Misalnya, memberikan diskon tambahan atau penawaran eksklusif bagi pelanggan yang menggunakan debit card. ")


if selected == "Purchase Time":
    st.title("Customer Purchase Time")
    df_product_sales = df_product_sales(all_df)

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df_product_sales['order_purchase_time'],
        y=df_product_sales['customer_id'],
        text=df_product_sales['customer_id'],  # Menambahkan label di setiap bar
        textposition='outside',  # Menampilkan label di luar bar
        textfont=dict(
            color='white',  # Mengatur warna teks menjadi putih
        ),
        marker=dict(
            color='rgb(173, 216, 230)',  # Set color here
        ),
    ))

    fig.update_layout(
        title='Customer Purchase Time Over 2016 - 2018',
        xaxis=dict(title='Product Name', tickangle=45),
        yaxis=dict(title='Total Sales'),
        showlegend=False,
        width=700,
        height=500,
    )

    st.plotly_chart(fig)

    with st.expander("Interpretasi", expanded=False):

            # Konten expander
            st.write("- Waktu transaksi pelanggan paling banyak dilakukan pada pagi hari yaitu sebesar 44871 transaksi.")
            st.write("- Waktu transaksi pelanggan paling sedikit adalah pada malam hari yaitu hanya sebesar 10112 transaksi.")
    
    
    with st.expander("Saran", expanded=False):

            # Konten expander
            st.write("Penawaran di Waktu Yang Ramai Pelanggan :")
            st.write("- Perhatikan waktu yang paling populer untuk transaksi, yaitu pagi hari. Kirimkan pemberitahuan atau promosi yang relevan kepada pelanggan pada waktu-waktu tersebut. Misalnya, mengirimkan pesan atau penawaran khusus yang dikirim tepat sebelum atau selama jam transaksi yang paling di pagi hari. Hal ini akan memaksimalkan kesempatan Anda untuk menarik perhatian pelanggan dan mendorong mereka untuk melakukan pembelian.")
            st.write(" ")
            st.write("Promosi sesuai dengan waktu aktif pelanggan :")
            st.write("- Mengirimkan promosi yang lebih disesuaikan dan relevan kepada pelanggan pada waktu preferensi pelanggan. Misalnya, jika Ada  pelanggan yang lebih aktif pada siang hari, Maka dapat dikirimkan penawaran eksklusif atau informasi produk terbaru saat siang hari. Sehingga, terjadi kemungkinan interaksi dan konversi transaksi pada pelanggan lebih tinggi.")