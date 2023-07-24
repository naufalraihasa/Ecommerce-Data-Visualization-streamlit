import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from folium.plugins import HeatMap
from streamlit_folium import folium_static
from streamlit_option_menu import option_menu
from babel.numbers import format_currency

st.set_page_config(
    page_title="Product Analysis",
    page_icon="🛍️",
)

with st.sidebar:
    selected = option_menu(
        menu_title="Product",
        options=["Top-selling product","Worst-selling product",],
    )


all_df = pd.read_csv("../all_data.csv")
datetime_columns = ["order_approved_at", "order_delivered_customer_date"]
all_df.sort_values(by="order_approved_at", inplace=True)
all_df.reset_index(inplace=True)


def df_large_product_sales(df):

    df_large_product_sales = all_df.groupby(by="product_name").agg({
        "payment_value": "sum",
    }).nlargest(10, "payment_value").round().reset_index()

    return df_large_product_sales

def df_samall_product_sales(df):

    df_samall_product_sales = all_df.groupby(by="product_name").agg({
        "payment_value": "sum",
    }).nsmallest(10, "payment_value").round().reset_index()

    return df_samall_product_sales


if selected == "Top-selling product":

    st.title("Top-selling Product Over 2016 - 2018")

    df_product_sales = df_large_product_sales(all_df)


    with st.container():
        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=df_product_sales['product_name'],
            y=df_product_sales['payment_value'],
            marker=dict(
                color='rgb(173, 216, 230)',  # Set color here
            ),
        ))

        for i, v in enumerate(df_product_sales['payment_value']):
            fig.add_annotation(
                x=df_product_sales['product_name'][i],
                y=v,
                text=str(v),
                font=dict(
                    size=10,
                    color='white',  # Set text color here
                ),
                showarrow=False,
                textangle=0,
                align='center',
                yshift=10
            )

        fig.update_layout(
            title='Top 10 Best Selling Products',
            xaxis=dict(
                title='Product Name',
                tickangle=45,
                tickfont=dict(
                    size=12,
                ),
                automargin=True,
            ),
            yaxis=dict(
                title='Total Sales',
                tickformat='plain',
                tickfont=dict(
                    size=12,
                ),
            ),
            width=700,
            height=500,
            showlegend=False,
        )

        st.plotly_chart(fig)

        with st.expander("Interpretasi", expanded=False):

            # Konten expander
            st.write("10 Produk Terlaris Tahun 2016-2018:")
            st.write("- 10 produk yang memiliki banyak peminat yaitu bed bath table, health beauty, computers accesories, furniture decor, watches gifts, sports leisure, housewares, garden tools, auto, dan cool stuff.")
            st.write("- Produk dengan penjualan tertinggi adalah bed bath beauty dengan jumlah penjualan 1725466 barang.")

        with st.expander("Saran", expanded=False):

            # Konten expander
            st.write("- Fokus pada Produk yang Populer :")
            st.write("  Menganalisis produk 'bed bath table' yang memiliki penjualan tertinggi. Identifikasi faktor-faktor yang membuat produk ini diminati oleh pelanggan, seperti kualitas, fitur, harga, atau manfaat yang ditawarkan. Fokus pada pengembangan dan pemasaran produk-produk yang populer dapat membantu meningkatkan penjualan secara keseluruhan")
            st.write("- Memperluas Segmentasi Produk :")
            st.write("  Memperluas segmentasi produk atau menambah layanan baru yang relevan dengan trend yang ada. Sehingga dapat menjangkau segmen pasar yang lebih luas dan mengurangi ketergantungan pada produk atau layanan tunggal.")

if selected == "Worst-selling product":
    st.title("Worst-selling Product Over 2016 - 2018")
    df_product_sales = df_samall_product_sales(all_df)
    with st.container():

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=df_product_sales['product_name'],
            y=df_product_sales['payment_value'],
            marker=dict(
                color='rgb(173, 216, 230)',  # Set color here
            ),
        ))

        for i, v in enumerate(df_product_sales['payment_value']):
            fig.add_annotation(
                x=df_product_sales['product_name'][i],
                y=v+5,
                text=str(v),
                font=dict(
                    size=10,
                    color='white',  # Set text color here
                ),
                showarrow=False,
                textangle=0,
                align='center',
                yshift=10
            )

        fig.update_layout(
            title='Top 10 Worst Selling Products',
            xaxis=dict(
                title='Product Name',
                tickangle=45,
                tickfont=dict(
                    size=12,
                ),
                automargin=True,
            ),
            yaxis=dict(
                title='Total Sales',
                tickformat='plain',
                tickfont=dict(
                    size=12,
                ),
            ),
            width=750,
            height=500,
            showlegend=False,
        )

        st.plotly_chart(fig)

        with st.expander("Interpretasi", expanded=False):

            # Konten expander
            st.write("10 Produk Paling Tidak Diminati  Tahun 2016-2018")
            st.write("- 10 produk yang memiliki sedikit peminat yaitu security and service, fashion childrens clothes, cds dvds musicals, home comfort, flowers, art and craftmanship, la cuisine, fashion sport, diapers and hygiene, fashion female clothing.")
            st.write("- Produk dengan penjualan terendah adalah security and service dengan jumlah penjualan 325 barang.")
        
        with st.expander("Saran", expanded=False):

            # Konten expander
            st.write("- Penawaran Promosi Khusus: ")
            st.write("  Untuk produk yang kurang diminati, dapat dipertimbangkan untuk membuat penawaran promosi khusus guna menarik minat pelanggan. Misalnya memberikan diskon, paket bundel, hadiah gratis, atau insentif lainnya. ")
