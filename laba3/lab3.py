import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from code1 import *
from code2 import *
from change import *

st.title("Створення веб-додатоку із використанням модуля Streamlit")

defaults = {
    "index": "VCI",
    "region": 1,
    "weeks": (1, 52),
    "years": (1982, 2024),
    "sort_up": False,
    "sort_down": False
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

if st.button("Скинути всі фільтри"):
    for key, value in defaults.items():
        st.session_state[key] = value
    st.rerun()

folder = "D:/зпад/foranakonda/forlab2"
data = read_data(folder)
data = replace_function(data)

regions_dict = {
    1: 'Вінницька', 2: 'Волинська', 3: 'Дніпропетровська', 4: 'Донецька', 5: 'Житомирська',
    6: 'Закарпатська', 7: 'Запорізька', 8: 'Івано-Франківська', 9: 'Київська', 10: 'Кіровоградська',
    11: 'Луганська', 12: 'Львівська', 13: 'Миколаївська', 14: 'Одеська', 15: 'Полтавська',
    16: 'Рівенська', 17: 'Сумська', 18: 'Тернопільська', 19: 'Харківська', 20: 'Херсонська',
    21: 'Хмельницька', 22: 'Черкаська', 23: 'Чернівецька', 24: 'Чернігівська', 25: 'Республіка Крим'
}
chosen_index = st.selectbox("Оберіть тип індексу", ["VCI", "TCI", "VHI"], index=["VCI", "TCI", "VHI"].index(st.session_state["index"]), key="index")
chosen_region = st.selectbox("Оберіть область", list(regions_dict.keys()),format_func=lambda x: regions_dict[x], index=list(regions_dict.keys()).index(st.session_state["region"]), key="region")
weeks = st.slider("Оберіть тижні", 1, 52, st.session_state["weeks"], key="weeks")
years = st.slider("Оберіть роки", 1982, 2024, st.session_state["years"], key="years")
sort_up = st.checkbox("Сортувати ↑", value=st.session_state["sort_up"], key="sort_up")
sort_down = st.checkbox("Сортувати ↓", value=st.session_state["sort_down"], key="sort_down")
df = data[
    (data["PROVINCE_ID"] == chosen_region) &
    (data["Week"] >= weeks[0]) & (data["Week"] <= weeks[1]) &
    (data["Year"] >= years[0]) & (data["Year"] <= years[1])
]
df = df[["PROVINCE_ID", "Year", "Week", chosen_index]]
df["PROVINCE_NAME"] = regions_dict[chosen_region]
if sort_up and not sort_down:
    df = df.sort_values(by=chosen_index, ascending=True)
elif sort_down and not sort_up:
    df = df.sort_values(by=chosen_index, ascending=False)
elif sort_up and sort_down:
    st.warning("Вибрано обидва сортування. Використано сортування ↑")
    df = df.sort_values(by=chosen_index)

tab1, tab2, tab3 = st.tabs(["Таблиця", "Графік", "Порівняння"])
with tab1:
    st.write("Відфільтровані дані:")
    st.dataframe(df)

with tab2:
    st.write("Графік по тижнях:")
    fig, ax = plt.subplots()
    sns.lineplot(data=df, x="Week", y=chosen_index, marker="o", ax=ax, color="red")
    ax.set_title("Графік по " + chosen_index)
    ax.grid(True)
    st.pyplot(fig)

with tab3:
    st.write("Порівняння з іншими регіонами:")
    df_all = data[
        (data["Week"] >= weeks[0]) & (data["Week"] <= weeks[1]) &
        (data["Year"] >= years[0]) & (data["Year"] <= years[1])
    ]
    df_avg = df_all.groupby("PROVINCE_ID")[chosen_index].mean().reset_index()
    df_avg["Region"] = df_avg["PROVINCE_ID"].map(regions_dict)

    fig2, ax2 = plt.subplots(figsize=(12, 5))
    sns.barplot(data=df_avg, x="Region", y=chosen_index, ax=ax2)
    ax2.set_title("Середнє по регіонах")
    plt.xticks(rotation=90)
    st.pyplot(fig2)
