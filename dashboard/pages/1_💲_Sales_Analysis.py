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
    page_title="Sales Analysis",
    page_icon="💲",
)

st.title("E-commerce sales performance")

all_df = pd.read_csv("../all_data.csv")
datetime_columns = ["order_approved_at", "order_delivered_customer_date"]
all_df.sort_values(by="order_approved_at", inplace=True)
all_df.reset_index(inplace=True)


def tingkat_penjualan_2016(df):
    df_tingkat_penjualan_2016 = all_df[all_df.order_year == 2016]

    tingkat_penjualan_2016 = df_tingkat_penjualan_2016.groupby(by='order_month').agg({
        "order_id": "nunique",
        "order_month_name" : pd.Series.mode,
        "payment_value" : "sum"
    }).sort_values(by="order_month").reset_index()
    
    return tingkat_penjualan_2016

def tingkat_penjualan_2017(df):
    df_tingkat_penjualan_2017 = all_df[all_df.order_year == 2017]

    tingkat_penjualan_2017 = df_tingkat_penjualan_2017.groupby(by='order_month').agg({
        "order_id": "nunique",
        "order_month_name" : pd.Series.mode,
        "payment_value" : "sum"
    }).sort_values(by="order_month").reset_index()
    
    return tingkat_penjualan_2017

def tingkat_penjualan_2018(df):
    df_tingkat_penjualan_2018 = all_df[all_df.order_year == 2018]

    tingkat_penjualan_2018 = df_tingkat_penjualan_2018.groupby(by='order_month').agg({
        "order_id": "nunique",
        "order_month_name" : pd.Series.mode,
        "payment_value" : "sum"
    }).sort_values(by="order_month").reset_index()
    
    return tingkat_penjualan_2018


with st.sidebar:
    selected = option_menu(
        menu_title="Year",
        options=["2016","2017","2018"],
    )

if selected == "2016":
    tingkat_penjualan_2016 = tingkat_penjualan_2016(all_df)
    col1, col2 = st.columns(2)

    with col1:
        total_orders = tingkat_penjualan_2016.order_id.sum()
        st.metric("Total orders", value=total_orders)
    
    with col2:
        total_revenue = format_currency(tingkat_penjualan_2016.payment_value.sum(), "AUD", locale='es_CO') 
        st.metric("Total Revenue", value=total_revenue)

    with st.container():

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=tingkat_penjualan_2016["order_month_name"],
            y=tingkat_penjualan_2016["order_id"],
            mode='lines+markers',
            marker=dict(
                color='red',
                size=8,
            ),
            line=dict(
                width=3,
            ),
        ))

        for x, y in zip(tingkat_penjualan_2016["order_month_name"], tingkat_penjualan_2016["order_id"]):
            fig.add_annotation(
                x=x,
                y=y+15,
                text=str(y),
                font=dict(
                    size=12,
                ),
                showarrow=False,
                textangle=0,
            )

        fig.update_layout(
            title="Sales Performance 2016",
            xaxis=dict(
                title="Order Month",
                titlefont=dict(
                    size=14,
                ),
                tickfont=dict(
                    size=14,
                ),
            ),
            yaxis=dict(
                title="Number of orders",
                titlefont=dict(
                    size=14,
                ),
                tickfont=dict(
                    size=14,
                ),
            ),
            width=650,
            height=400,
        )

        st.plotly_chart(fig)

        with st.expander("Interpretasi", expanded=False):

            # Konten expander
            st.write("Tingkat penjualan di tahun 2016 tidak dapat diamati dengan baik dikarenakan ketidaklengkapan data yang ada. Yaitu hanya terdapat 1 transaksi pada bulan Desember 2016.")
        
        with st.expander("Saran", expanded=False):

            # Konten expander
            st.write("Mengumpulkan data yang Lebih Komprehensif: Sebaiknya dipastikan untuk mengumpulkan data penjualan yang lebih lengkap dan komprehensif di masa mendatang. Hal ini dapat dilakukan dengan merekam setiap transaksi penjualan dengan lebih baik. Dengan data yang lengkap, maka dapat dilakukan identifikasi produk yang memiliki tingkat penjualan secara lebih akurat.")

if selected == "2017":
    tingkat_penjualan_2017 = tingkat_penjualan_2017(all_df)
    col1, col2 = st.columns(2)

    with col1:
        total_orders = tingkat_penjualan_2017.order_id.sum()
        st.metric("Total orders", value=total_orders)
    
    with col2:
        total_revenue = format_currency(tingkat_penjualan_2017.payment_value.sum(), "AUD", locale='es_CO') 
        st.metric("Total Revenue", value=total_revenue)

    fig = go.Figure()

    with st.container():
        fig.add_trace(go.Scatter(
            x=tingkat_penjualan_2017["order_month_name"],
            y=tingkat_penjualan_2017["order_id"],
            mode='lines+markers',
            marker=dict(
                color='red',
                size=8,
            ),
            line=dict(
                width=3,
            ),
        ))

        for x, y in zip(tingkat_penjualan_2017["order_month_name"], tingkat_penjualan_2017["order_id"]):
            fig.add_annotation(
                x=x,
                y=y+150,
                text=str(y),
                font=dict(
                    size=12,
                ),
                showarrow=False,
                textangle=0,
            )

        fig.update_layout(
            title="Sales Performance 2017",
            xaxis=dict(
                title="Order Month",
                titlefont=dict(
                    size=14,
                ),
                tickfont=dict(
                    size=14,
                ),
            ),
            yaxis=dict(
                title="Number of orders",
                titlefont=dict(
                    size=14,
                ),
                tickfont=dict(
                    size=14,
                ),
            ),
            width=650,
            height=400,
        )

        st.plotly_chart(fig)

        with st.expander("Interpretasi", expanded=False):

            # Konten expander
            st.write("Tingkat penjualan pada tahun 2017 menunjukan tren pertumbuhan yang baik hingga akhir tahun. Bulan november merupakan bulan yang memiliki jumlah transaksi tertinggi yaitu sebesar 7146 transaksi dengan total penjualan selama 1 tahun sebesar 43352 dan total pemasukan dari keseluruhan transaksi sebesar 8 juta USD atau sekitar 121 milyar rupiah.")

        with st.expander("Saran", expanded=False):

            st.write("- Memanfaatkan Tren Pertumbuhan:")
            st.write("  Memanfaatkan adanya tren pertumbuhan yang baik pada tahun 2017 untuk meningkatkan penjualan di tahun-tahun berikutnya dengan mengidentifikasi faktor-faktor yang berkontribusi terhadap peningkatan penjualan pada bulan November, seperti promosi khusus, produk yang populer, atau strategi pemasaran yang efektif.")
            st.write("- Analisis Bulan November:")
            st.write("  meneliti dengan lebih mendalam mengapa bulan November memiliki jumlah transaksi tertinggi. Apakah ada peristiwa khusus, seperti liburan atau acara penjualan besar, yang mendorong pertumbuhan tersebut. Analisis ini dapat membantu untuk merencanakan kegiatan promosi atau penjualan yang serupa di masa depan.")

if selected == "2018":
    tingkat_penjualan_2018 = tingkat_penjualan_2018(all_df)
    col1, col2 = st.columns(2)

    with col1:
        total_orders = tingkat_penjualan_2018.order_id.sum()
        st.metric("Total orders", value=total_orders)
    
    with col2:
        total_revenue = format_currency(tingkat_penjualan_2018.payment_value.sum(), "AUD", locale='es_CO') 
        st.metric("Total Revenue", value=total_revenue)

    fig = go.Figure()

    with st.container():
        fig.add_trace(go.Scatter(
            x=tingkat_penjualan_2018["order_month_name"],
            y=tingkat_penjualan_2018["order_id"],
            mode='lines+markers',
            marker=dict(
                color='red',
                size=8,
            ),
            line=dict(
                width=3,
            ),
        ))

        for x, y in zip(tingkat_penjualan_2018["order_month_name"], tingkat_penjualan_2018["order_id"]):
            fig.add_annotation(
                x=x,
                y=y+150,
                text=str(y),
                font=dict(
                    size=12,
                ),
                showarrow=False,
                textangle=0,
            )

        fig.update_layout(
            title="Sales Performance 2018",
            xaxis=dict(
                title="Order Month",
                titlefont=dict(
                    size=14,
                ),
                tickfont=dict(
                    size=14,
                ),
            ),
            yaxis=dict(
                title="Number of orders",
                titlefont=dict(
                    size=14,
                ),
                tickfont=dict(
                    size=14,
                ),
            ),
            width=650,
            height=400,
        )

        st.plotly_chart(fig)

        with st.expander("Interpretasi", expanded=False):

            # Konten expander
            st.write("Tingkat penjualan pada tahun 2018 menujukan tren yang cukup stagnan dan cenderung turun dengan bulan maret menjadi bulan yang memiliki jumlah transaksi tertinggi yaitu sebesar 7085 transaksi.dengan total penjualan selama 1 tahun sebesar 52859 dan total pemasukan dari keseluruhan transaksi sebesar 10 juta USD atau sekitar 151 milyar rupiah.")
        
        with st.expander("Saran", expanded=False):

            # Konten expander
            st.write("- Identifikasi Penyebab Stagnansi dan Penurunan: ")
            st.write("  Meneliti dengan lebih mendalam untuk mengidentifikasi faktor-faktor yang menyebabkan penurunan dan stagnannya tingkat penjualan. Meninjau faktor-faktor internal dan eksternal yang mungkin berperan, seperti perubahan preferensi pelanggan, persaingan yang meningkat, perubahan tren pasar, atau perubahan dalam strategi pemasaran.")