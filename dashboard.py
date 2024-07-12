import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Facebook Data Analysis", page_icon=":bar_chart:", layout="wide")

st.title(" :bar_chart: Facebook Data Analysis")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

fl = st.file_uploader(":file_folder: Upload a file", type=(["csv", "txt", "xlsx", "xls"]))
if fl is not None:
    filename = fl.name
    st.write(filename)
    df = pd.read_csv(filename, encoding="ISO-8859-1")
else:
    df = pd.read_csv("pseudo_facebook.csv", encoding="ISO-8859-1")

# Data Pre-processing
df['gender'].fillna('Unknown', inplace=True)
df['tenure'].fillna(df['tenure'].median(), inplace=True)

# Feature Engineering
df['dob'] = pd.to_datetime(df[['dob_year', 'dob_month', 'dob_day']].astype(str).agg('-'.join, axis=1), errors='coerce')
df['engagement_rate'] = df['likes_received'] / (df['friend_count'] + 1)
df['click_through_rate'] = df['mobile_likes'] / (df['likes'] + 1)

col1, col2 = st.columns((2))
startDate = df['dob'].min()
endDate = df['dob'].max()

with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))

with col2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))

df = df[(pd.to_datetime(df['dob']) >= date1) & (pd.to_datetime(df['dob']) <= date2)].copy()

st.sidebar.header("Choose your filter: ")
# Create filter for Gender
gender = st.sidebar.multiselect("Pick your Gender", df["gender"].unique())
if not gender:
    df2 = df.copy()
else:
    df2 = df[df["gender"].isin(gender)]

# Create filter for Age
age = st.sidebar.slider("Pick the Age range", int(df2["age"].min()), int(df2["age"].max()), (int(df2["age"].min()), int(df2["age"].max())))
df2 = df2[(df2["age"] >= age[0]) & (df2["age"] <= age[1])]

filtered_df = df2.copy()

category_df = filtered_df.groupby(by=["gender"], as_index=False)["friend_count"].sum()

with col1:
    st.subheader("Gender wise Friend Count")
    fig = px.bar(category_df, x="gender", y="friend_count", text=['{:,.2f}'.format(x) for x in category_df["friend_count"]],
                 template="seaborn")
    st.plotly_chart(fig, use_container_width=True, height=200)

with col2:
    st.subheader("Age Distribution")
    fig = px.histogram(filtered_df, x="age", nbins=30)
    st.plotly_chart(fig, use_container_width=True)

cl1, cl2 = st.columns((2))
with cl1:
    with st.expander("Gender_ViewData"):
        st.write(category_df.style.background_gradient(cmap="Blues"))
        csv = category_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Data", data=csv, file_name="Gender.csv", mime="text/csv",
                           help='Click here to download the data as a CSV file')

with cl2:
    with st.expander("Age_ViewData"):
        age_df = filtered_df.groupby(by="age", as_index=False)["friend_count"].sum()
        st.write(age_df.style.background_gradient(cmap="Oranges"))
        csv = age_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Data", data=csv, file_name="Age.csv", mime="text/csv",
                           help='Click here to download the data as a CSV file')

filtered_df["month_year"] = pd.to_datetime(filtered_df["dob"]).dt.to_period("M")
st.subheader('Time Series Analysis')

linechart = pd.DataFrame(filtered_df.groupby(filtered_df["month_year"].dt.strftime("%Y-%m"))["friend_count"].sum()).reset_index()
fig2 = px.line(linechart, x="month_year", y="friend_count", labels={"friend_count": "Friend Count"}, height=500, width=1000, template="gridon")
st.plotly_chart(fig2, use_container_width=True)

with st.expander("View Data of TimeSeries:"):
    st.write(linechart.T.style.background_gradient(cmap="Blues"))
    csv = linechart.to_csv(index=False).encode("utf-8")
    st.download_button('Download Data', data=csv, file_name="TimeSeries.csv", mime='text/csv')

st.subheader("Hierarchical view of Friend Count using TreeMap")
fig3 = px.treemap(filtered_df, path=["gender", "age"], values="friend_count", hover_data=["friend_count"],
                  color="age")
fig3.update_layout(width=800, height=650)
st.plotly_chart(fig3, use_container_width=True)

chart1, chart2 = st.columns((2))
with chart1:
    st.subheader('Engagement Rate Distribution')
    fig = px.histogram(filtered_df, x="engagement_rate", nbins=30)
    st.plotly_chart(fig, use_container_width=True)

with chart2:
    st.subheader('Click Through Rate Distribution')
    fig = px.histogram(filtered_df, x="click_through_rate", nbins=30)
    st.plotly_chart(fig, use_container_width=True)

import plotly.figure_factory as ff
st.subheader(":point_right: Month wise Friend Count Summary")
with st.expander("Summary_Table"):
    df_sample = df[0:5][["gender", "age", "friend_count", "likes", "likes_received", "tenure"]]
    fig = ff.create_table(df_sample, colorscale="Cividis")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("Month wise Friend Count Table")
    filtered_df["month"] = pd.to_datetime(filtered_df["dob"]).dt.month_name()
    friend_count_Year = pd.pivot_table(data=filtered_df, values="friend_count", index=["age"], columns="month")
    st.write(friend_count_Year.style.background_gradient(cmap="Blues"))

# Create a scatter plot
data1 = px.scatter(filtered_df, x="likes", y="likes_received", size="friend_count")
data1['layout'].update(title="Relationship between Likes and Likes Received using Scatter Plot.",
                       titlefont=dict(size=20), xaxis=dict(title="Likes", titlefont=dict(size=19)),
                       yaxis=dict(title="Likes Received", titlefont=dict(size=19)))
st.plotly_chart(data1, use_container_width=True)

with st.expander("View Data"):
    st.write(filtered_df.iloc[:500, 1:20:2].style.background_gradient(cmap="Oranges"))

# Download original DataSet
csv = df.to_csv(index=False).encode('utf-8')
st.download_button('Download Data', data=csv, file_name="Data.csv", mime="text/csv")
