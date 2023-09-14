import streamlit as st
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

st.title('My Parents New Healthy Dinner')

st.header('Breakfast menu')

st.text('🥣 Omega 3 & Blueberry Oatmeal')
st.text('🥗 Kale, Spinach & Rocket Smoothie')
st.text('🐔 Hard-Boiled Free-Range Egg')
st.text('🥑🍞 Avocado')

st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

# choose the fruit name column as the index
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include

# st.multiselect("Pick some fruits:", list(my_fruit_list.index))
#st.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# display the table on the page
st.dataframe(fruits_to_show)

# create the repeatable code block (called a function)
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

# new section to display fruityvice api response
st.header("Fruityvice Fruit Advice!")

try:
  fruit_choice = st.text_input('What fruit would you like information about?')
  if not fruit_choice:
        st.error("Please select a fruit to get information.")
  else:
        back_from_function = get_fruityvice_data(fruit_choice)
        #output it the screen as a table
        st.dataframe(back_from_function)
    
except URLError as e:
  # don't run anythig past here while we troubleshoot
  st.error()

my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM fruit_load_list")
my_data_rows = my_cur.fetchall()
st.header("The fruit load list contains:")
st.dataframe(my_data_rows)

# Allow the end user to add a fruit to the list
add_my_fruit = st.text_input('What fruit would you like to add?')
st.write('Thanks for adding', add_my_fruit)

# This will not work correctly, but just go with it for now
my_cur.execute("insert into fruit_load_list values ('from streamlit')")
