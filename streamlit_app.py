# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col, when_matched

# Page title and description
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)

# Session config
cnx = st.connection("snowflake")
session = cnx.session()

# Name on order input
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

# Load fruit options from Snowflake to a df
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

# Multiselect widget limited to 5 ingredients
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe,
    max_selections=5
)

# Build ingredients string from selected fruits
if ingredients_list:
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

  # Build INSERT statement
    my_insert_stmt = """ insert into smoothies.public.orders
                (INGREDIENTS, NAME_ON_ORDER)
                values ('""" + ingredients_string + """','""" + name_on_order + """')"""

  # Submit order button
    time_to_insert = st.button ('Submit Order')

   # Execute INSERT when button is clicked
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        
        st.success('Your Smoothie is ordered!', icon="✅")

# Display Smoothiefroot nutrition information
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
#st.text(smoothiefroot_response.json())
sf_df = st.dataframe(data=smoothiefroot_response.json(), use container_width=True)
