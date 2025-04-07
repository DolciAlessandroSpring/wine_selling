import pandas as pd
import streamlit as st

# ---------- Page Setup ----------
st.set_page_config(layout="wide")

# ---------- Load Data ----------
csv_path = '/Users/adolci/OneDrive - Axel Springer SE/Python/private/wine_selling/restaurants_in_schwabing_west.csv'
df = pd.read_csv(csv_path)

# ---------- Session State Init ----------
if 'client_status' not in st.session_state:
    st.session_state.client_status = {
        row['placeId']: bool(row.get('is_already_a_client', False))
        for _, row in df.iterrows()
    }

if 'interest_status' not in st.session_state:
    st.session_state.interest_status = {
        row['placeId']: bool(row.get('is_an_interesting_client', False))
        for _, row in df.iterrows()
    }
if 'sort_column' not in st.session_state:
    st.session_state.sort_column = 'name'
    st.session_state.sort_order = 'ascending'

# ---------- Header with Save Button ----------
col_title, col_button = st.columns([4, 1])
with col_title:
    st.title("🍷 Italian Restaurants 🍷")

with col_button:
    if st.button("Save", key="save_button"):
        df['is_already_a_client'] = df['placeId'].map(st.session_state.client_status)
        df.to_csv(csv_path, index=False)
        st.success("✅ File saved successfully!")

# ---------- Client Filter ----------
def filter_client_status(df):
    status = st.radio(
        "Filter by client status:",
        ("All", "My clients", "Not my clients"),
        horizontal=True
    )
    if status == "My clients":
        return df[df['placeId'].map(st.session_state.client_status)]
    elif status == "Not my clients":
        return df[~df['placeId'].map(st.session_state.client_status)]
    return df

# ---------- Interest Filter ----------
def filter_interest_status(df):
    status = st.radio(
        "Filter by interest status:",
        ("All", "Interested in"),
        horizontal=True
    )
    if status == "Interested in":
        return df[df['placeId'].map(st.session_state.interest_status)]
    return df

# ---------- Sorting ----------
def sort_df(df, column):
    ascending = st.session_state.sort_order == 'ascending'
    return df.sort_values(by=column, ascending=ascending)

def update_sort(column_name):
    if st.session_state.sort_column == column_name:
        st.session_state.sort_order = 'ascending' if st.session_state.sort_order == 'descending' else 'descending'
    else:
        st.session_state.sort_column = column_name
        st.session_state.sort_order = 'ascending'

# ---------- Searching ----------
def search_df(df): 
    search_query = st.text_input("🔍 Search restaurants typing a name, address or area:")

    if search_query:
        df = df[
            df['name'].str.contains(search_query, case=False, na=False) |
            df['address'].str.contains(search_query, case=False, na=False) |
            df['area'].str.contains(search_query, case=False, na=False)
        ]
    return df

# ---------- Column Headers ----------
def display_headers():
    cols = st.columns([3, 3, 2, 2, 2, 2, 2])
    headers = [
        ("Name", "name"),
        ("Address", None),
        ("Area", None),
        ("Number of Reviews", "userRatingCount"),
        ("Is it already a client?", None),
        ("Is it an interesting client?", None),
        ("Google Maps Link", None)
    ]
    for col, (label, field) in zip(cols, headers):
        with col:
            if field:
                if st.button(label, key=f"sort_{field}"):
                    update_sort(field)
            else:
                st.markdown(f"**{label}**")

# ---------- Display Row ----------
def display_row(row):
    cols = st.columns([3, 3, 2, 2, 2, 2, 2])
    with cols[0]:
        st.markdown(f"**{row['name']}**")
    with cols[1]:
        st.markdown(row['address'])
    with cols[2]:
        st.markdown(row['area'])
    with cols[3]:
        st.markdown(str(row['userRatingCount']))
    with cols[4]:
        checked = st.checkbox(
            "", value=st.session_state.client_status.get(row['placeId'], False),
            key=f"{row['placeId']}_client"
        )
        st.session_state.client_status[row['placeId']] = checked
    with cols[5]:
        checked = st.checkbox(
            "", value=st.session_state.interest_status.get(row['placeId'], False),
            key=f"{row['placeId']}_interest"
        )
        st.session_state.interest_status[row['placeId']] = checked
    with cols[6]:
        st.markdown(
            f"[View on Google Maps](https://www.google.com/maps/place/?q=place_id:{row['placeId']})",
            unsafe_allow_html=True
        )

# ---------- Main Display ----------
df_filtered = filter_client_status(df)
df_filtered = filter_interest_status(df_filtered)
df_filtered = search_df(df_filtered)
display_headers()
df_sorted = sort_df(df_filtered, st.session_state.sort_column)

for _, row in df_sorted.iterrows():
    st.markdown("---")
    display_row(row)
