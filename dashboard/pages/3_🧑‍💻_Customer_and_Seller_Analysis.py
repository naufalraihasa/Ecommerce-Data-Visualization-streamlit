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
    page_title="Customer and Seller Analysis",
    page_icon="🧑‍💻",
)

with st.sidebar:
    selected = option_menu(
        menu_title="Customer/Seller Distribution",
        options=["Customer","Seller", "Customer Segmentation"],
    )


all_df = pd.read_csv("../all_data.csv")
datetime_columns = ["order_approved_at", "order_delivered_customer_date"]
all_df.sort_values(by="order_approved_at", inplace=True)
all_df.reset_index(inplace=True)

datetime_columns = ["order_approved_at","order_delivered_carrier_date",'order_delivered_customer_date','order_estimated_delivery_date' ]
 
for column in datetime_columns:
  all_df[column] = pd.to_datetime(all_df[column])
  all_df[column] = all_df[column].dt.date
  all_df[column] = pd.to_datetime(all_df[column])

def bystate_customer_df(df):
    bystate_customer_df = df.groupby(by="customer_city").agg({
        "order_id": "nunique",
        "payment_value": "sum",
        "product_name": pd.Series.mode
    }).nlargest(10, "order_id").reset_index()
    bystate_customer_df.rename(columns={
        "order_id": "customer_count"
    }, inplace=True)

    return bystate_customer_df

def bystate_seller_df(df):
    bystate_seller_df = df.groupby(by="seller_city").agg({
        "order_id": "nunique",
        "payment_value": "sum",
        "product_name": pd.Series.mode
    }).nlargest(10, "order_id").reset_index()
    bystate_seller_df.rename(columns={
        "order_id": "seller_count"
    }, inplace=True)

    return bystate_seller_df

def recency (df):
    frequency_df = df.groupby(by='customer_id',as_index=False)['order_approved_at'].max()
    frequency_df.columns = ['CustomerId', 'LastPurchaseDate']
    recent_date = frequency_df['LastPurchaseDate'].max()
    frequency_df['Recency'] = frequency_df['LastPurchaseDate'].apply(lambda x: (recent_date - x).days)
    return frequency_df

def frequency (df):
    frequency_df = df.drop_duplicates().groupby(
        by=['customer_id'], as_index=False)['order_approved_at'].count()
    frequency_df.columns = ['CustomerId', 'Frequency']
    return frequency_df


def monetary(df):
    monetary_df = df.groupby(by='customer_id', as_index=False)['payment_value'].sum()
    monetary_df.columns = ['CustomerId', 'Monetary']
    return monetary_df

def rfm (recency, frequency, monetary) :
    rf_df = recency.merge(frequency, on='CustomerId')
    rfm_df = rf_df.merge(monetary, on='CustomerId').drop(
        columns='LastPurchaseDate')

    rfm_df['R_rank'] = rfm_df['Recency'].rank(ascending=False)
    rfm_df['F_rank'] = rfm_df['Frequency'].rank(ascending=True)
    rfm_df['M_rank'] = rfm_df['Monetary'].rank(ascending=True)
    
    # normalizing the rank of the customers
    rfm_df['R_rank_norm'] = (rfm_df['R_rank']/rfm_df['R_rank'].max())*100
    rfm_df['F_rank_norm'] = (rfm_df['F_rank']/rfm_df['F_rank'].max())*100
    rfm_df['M_rank_norm'] = (rfm_df['F_rank']/rfm_df['M_rank'].max())*100
    rfm_df.drop(columns=['R_rank', 'F_rank', 'M_rank'], inplace=True)


    rfm_df['RFM_Score'] = 0.15*rfm_df['R_rank_norm']+0.28 * \
        rfm_df['F_rank_norm']+0.57*rfm_df['M_rank_norm']
    rfm_df['RFM_Score'] *= 0.05
    rfm_df = rfm_df.round(2)

    rfm_df["Customer_segment"] = np.where(rfm_df['RFM_Score'] > 4.5, "Top Customers",
                                (np.where(rfm_df['RFM_Score'] > 4,"High value Customer",
                                (np.where(rfm_df['RFM_Score'] > 3,"Medium Value Customer",
                                np.where(rfm_df['RFM_Score'] > 1.6,'Low Value Customers', 'Lost Customers'))))))
    return rfm_df


if selected == "Customer":
    st.title("Customer Distribution Over 2016 - 2018")
    bystate_customer_df = bystate_customer_df(all_df)

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=bystate_customer_df['customer_count'],
        y=bystate_customer_df['customer_city'],
        orientation='h',
        marker=dict(
            color=["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"],
        ),
        text=bystate_customer_df['customer_count'],  # Menambahkan teks berdasarkan jumlah penjual
        textposition='auto',  # Menyesuaikan posisi teks secara otomatis
    ))

    fig.update_layout(
        title='Number of customer by city',
        xaxis=dict(
            title='customer Count',
            tickfont=dict(
                size=12,
            ),
        ),
        yaxis=dict(
            tickfont=dict(
                size=12,
            ),
            automargin=True,
        ),
        width=800,
        height=500,
    )

    st.plotly_chart(fig)

    with st.expander("Interpretation", expanded=False):

        # Konten expander
        st.write("Jumlah pelanggan berdasarkan wilayah:")
        st.write("- Sao Bernando Campo memiliki pelanggan terendah dari 10 wilayah, dengan jumlah 907 jiwa")
        st.write("- Sao Paulo memiliki pelanggan tertinggi dari 10 wilayah, dengan jumlah 15045 jiwa")

    with st.expander("Saran", expanded=False):

        # Konten expander
        st.write("- Mengembangkan Pasar di Daerah Dengan Pelanggan Yang Tinggi")
        st.write("  Manfaatkan potensi pasar di wilayah seperti Sao Paulo yang memiliki jumlah pelanggan tertinggi. Identifikasi segmentasi pasar yang spesifik di wilayah Sao Paulo dan kembangkan kampanye pemasaran yang relevan untuk menarik minat pelanggan untuk melakukan transaksi.")
        st.write("- Penawaran Promo Khusus Daerah Dengan Pelanggan Yang Rendah:")
        st.write("  Tawarkan diskon khusus untuk pembelian produk tertentu kepada pelanggan di daerah dengan jumlah pelanggan rendah. Misalnya, memberikan diskon 15% untuk semua pelanggan di Guarulhos dalam jangka waktu tertentu.")


if selected == "Seller":
    st.title("Seller Distribution Over 2016 - 2018")
    bystate_seller_df = bystate_seller_df(all_df)
    
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=bystate_seller_df['seller_count'],
        y=bystate_seller_df['seller_city'],
        orientation='h',
        marker=dict(
            color=["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"],
        ),
        text=bystate_seller_df['seller_count'],  # Menambahkan teks berdasarkan jumlah penjual
        textposition='auto',  # Menyesuaikan posisi teks secara otomatis
    ))

    fig.update_layout(
        title='Number of seller by city',
        xaxis=dict(
            title='seller Count',
            tickfont=dict(
                size=12,
            ),
        ),
        yaxis=dict(
            tickfont=dict(
                size=12,
            ),
            automargin=True,
        ),
        width=800,
        height=500,
    )

    st.plotly_chart(fig)

    with st.expander("Interpretasi", expanded=False):

        # Konten expander
        st.write("Jumlah penjual berdasarkan wilayah:")
        st.write("- Guarulhos memiliki penjual terendah dari 10 wilayah, dengan jumlah 1694 penjual")
        st.write("- Sao Paulo memiliki penjual tertinggi dari 10 wilayah, dengan jumlah 24215 penjual")
    
    with st.expander("Saran", expanded=False):

        # Konten expander
        st.write("- Mengembangkan Pasar di Daerah Dengan Seller Yang Tinggi:")
        st.write("Manfaatkan potensi pasar di wilayah seperti Sao Paulo yang memiliki jumlah seller tertinggi untuk menarik pembeli sebanyak - banyaknya. Memberikan promo seperti discount atau lainnya di segmentasi seller yang barangnya memiliki minat yang tinggi dari pembeli.")
        st.write("- Menyelidiki Daerah Yang Memiliki Seller Yang Rendah:")
        st.write("Daerah yang jumlah sellernya edikit bisa dikarenakan daerah tersebut jauh dari kebanyakan tempat pelanggan, sehingga sedikit pelanggan yang membeli dari daerah tersebut dan menyebabkan sedikitnya jumlah seller disana. Karena dapat dilihat dari jumlah customer paling banyak berada di saopaulo. Oleh karena itu mungkin bisa di pertimbangkan untuk membuat promosi seperti memberikan gratis ongkir atau sebagainya.")


if selected == "Customer Segmentation":
    st.title("Customer Segmentation Over 2016 - 2018")

    tab1, tab2 = st.tabs(["RFM Analysis", "Customer Segmentation Analysis"])

    with tab1:
        # Count the occurrences of each segment
        recency = recency(all_df)
        frequency = frequency(all_df)
        monetary = monetary(all_df)
        rfm_df = rfm(recency, frequency, monetary)
        displayed_df = rfm_df[['CustomerId','Recency','Frequency','Monetary','RFM_Score','Customer_segment']].head(5)
        segment_counts = rfm_df['Customer_segment'].value_counts()

        st.write("**Customer RFM Analysis**")
        st.table(displayed_df)

    with tab2:
        # Define a pastel color palette
        color_palette = ['#B7D7D8', '#F3B1B3', '#B5B8C3', '#F9D9B4']

        # Create a Pie chart trace
        pie_trace = go.Pie(
            labels=segment_counts.index,
            values=segment_counts.values,
            hovertemplate='Segment: %{label}<br>Count: %{value}<br>Percentage: %{percent}',
            textinfo='percent',
            textposition='inside',  # Set the label position to 'inside'
            textfont=dict(size=12),
            marker=dict(
                colors=color_palette,
                line=dict(color='#000000', width=1)
            )
        )

        # Create the layout
        layout = go.Layout(
            title='Customer Segmentation',
            width=600,  # Adjust the width of the chart
            height=400  # Adjust the height of the chart
        )

        # Create the figure
        fig = go.Figure(data=[pie_trace], layout=layout)
        st.plotly_chart(fig)

    with st.expander("Interpretasi", expanded=False):

        # Konten expander
        st.write("Segmentasi Pelanggan :")
        st.write("- Sebagian besar pelanggan adalah pelanggan dengan indeks 'Low Value Customer' yang berarti ia memiliki nilai RFM score dibawah 1.6 yang bisa dibilang sangat rendah. Hal tersebut disebabkan kaarena banyak sekali customer yang hanya melakukan transaksi sebanyak 1 kali dan tidak pernah melakukan transaksi lagi selama rentang tahun 2016 - 2018. ")
        st.write("- Hanya 3.52% dari keseluruhan pelanggan yang termasuk kedalam 'Top customer' dan hanya sebesar 8.14% yang termasuk kedalam 'High Value Customer'. ")
    
    with st.expander("Saran", expanded=False):

        # Konten expander
        st.write("- Fokus Meminimalkan Tingkat Retensi Pelanggan:")
        st.write("Mengurangi jumlah pelanggan dengan nilai RFM yang rendah dengan memberikan penawaran khusus, diskon, atau program loyalitas seperti membership agar pelanggan menjadi lebih tertarik untuk berbelanja dan melakukan lebih dari satu transaksi. ")
        st.write("- Memberikan Reward Kepada 'High Value Customer' dan 'Top Customer' ")
        st.write("Memberikan reward kepada pelanggan tersebut yang dapat meningkatkan 'customer experience' mereka seperti harga khusus, pelayanan yang lebih diutamakan, fasilitas eksklusif seperti fitur khusus. Sehingga pelanggan tersebut tetap menjadi pelanggan dengan statis 'High value' atau 'Top'.")

