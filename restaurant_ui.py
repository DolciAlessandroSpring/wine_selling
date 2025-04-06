import pandas as pd
import streamlit as st

# Set wide layout
st.set_page_config(layout="wide")

# Load the data
csv_path = '/Users/adolci/OneDrive - Axel Springer SE/Python/private/wine_selling/restaurants_in_schwabing_west_app.csv'
df = pd.read_csv(csv_path)

# Initialize client status in session state if not already set
if 'client_status' not in st.session_state:
    if 'is_already_a_client' in df.columns:
        st.session_state.client_status = {
            row['placeId']: bool(row['is_already_a_client']) for _, row in df.iterrows()
        }
    else:
        st.session_state.client_status = {
            row['placeId']: False for _, row in df.iterrows()
        }

# # Page title with wine glass emoji
# st.title("🍷 Italian Restaurants 🍷")

# Create columns for the title and button layout
col1, col2 = st.columns([4, 1])
with col1:
    st.title("🍷 Italian Restaurants 🍷")
with col2:
    if st.button("Save", key="save_button"):
        df['is_already_a_client'] = df['placeId'].map(st.session_state.client_status)
        output_csv_path = '/Users/adolci/OneDrive - Axel Springer SE/Python/private/wine_selling/restaurants_in_schwabing_west_app.csv'
        df.to_csv(output_csv_path, index=False)
        st.success(f"File saved successfully to: {output_csv_path}")

# Initialize sorting state
if 'sort_column' not in st.session_state:
    st.session_state.sort_column = 'name'  # Default sort by 'name'
    st.session_state.sort_order = 'ascending'

# Sort function based on clicked column
def sort_df(df, column_name, sort_order='ascending'):
    ascending = sort_order == 'ascending'
    return df.sort_values(by=column_name, ascending=ascending)

# Filter for "Is it already a client?"
def filter_client_status(df):
    status_filter = st.radio(
        "Filter by client status:",
        ("All", "My clients", "Not my clients"),
        index=0  # Default to "Both"
    )
    if status_filter == "My clients":
        return df[df['placeId'].isin([place_id for place_id, status in st.session_state.client_status.items() if status])]
    elif status_filter == "Not my clients":
        return df[~df['placeId'].isin([place_id for place_id, status in st.session_state.client_status.items() if status])]
    return df

# Display column headers and handle sorting by column click
def display_column_headers():
    col1, col2, col3, col4, col5, col6 = st.columns([3, 3, 2, 2, 2, 2])

    # Clickable columns (Sort columns when clicked)
    with col1:
        if st.button("Name", key="sort_name"):
            st.session_state.sort_column = 'name'
            st.session_state.sort_order = 'ascending' if st.session_state.sort_order == 'descending' else 'descending'
    with col2:
        if st.button("Address", key="sort_address"):
            st.session_state.sort_column = 'address'
            st.session_state.sort_order = 'ascending' if st.session_state.sort_order == 'descending' else 'descending'
    with col3:
        if st.button("Area", key="sort_area"):
            st.session_state.sort_column = 'area'
            st.session_state.sort_order = 'ascending' if st.session_state.sort_order == 'descending' else 'descending'
    with col4:
        if st.button("Number of Reviews", key="sort_reviews"):
            st.session_state.sort_column = 'userRatingCount'
            st.session_state.sort_order = 'ascending' if st.session_state.sort_order == 'descending' else 'descending'
    with col5:
        # "Is it already a client?" will be a filter, not a sort option
        st.markdown("**Is it already a client?**")

# Display restaurant data
def display_restaurant_data(row):
    col1, col2, col3, col4, col5, col6 = st.columns([3, 3, 2, 2, 2, 2])

    with col1:
        st.markdown(f"**{row['name']}**")
    with col2:
        st.markdown(row['address'])
    with col3:
        st.markdown(row['area'])
    with col4:
        st.markdown(f"{row['userRatingCount']}")
    with col5:
        # Checkbox to mark if restaurant is already a client
        checked = st.checkbox("", value=st.session_state.client_status.get(row['placeId'], False), key=row['placeId'])
        st.session_state.client_status[row['placeId']] = checked
    with col6:
        st.markdown(f"[View on Google Maps](https://www.google.com/maps/place/?q=place_id:{row['placeId']})", unsafe_allow_html=True)

# Apply filter for "Is it already a client?" column
df_filtered = filter_client_status(df)

# Display the column headers and handle sorting
display_column_headers()

# Sort DataFrame based on selected column and order
df_sorted = sort_df(df_filtered, st.session_state.sort_column, st.session_state.sort_order)

# Display each restaurant in sorted order
for i, row in df_sorted.iterrows():
    st.markdown("---")  # horizontal divider between rows
    display_restaurant_data(row)
