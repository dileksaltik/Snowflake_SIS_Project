# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothiess:cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!
    
  """
)
  
#puts a selectbox onto screen
#option = st.selectbox(
     # "What is your favourite froot?",
    # ("Banana", "Strawberries", "Peaches"),
# )

# st.write("Your favorite froot is:", option)

cnx =st.connection("snowflake")
session = get_active_session()
#session = cnx.session()
#gets all data from the table
#my_dataframe = session.table("smoothies.public.fruit_options")
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

#st.dataframe(data=my_dataframe, use_container_width=True)
name_on_order = st.text_input('Name on Smoothie')

st.write('The name on your smoothie will be: ', name_on_order )

ingredients_list = st.multiselect('Choose up to 5 ingredients:',
                                  my_dataframe, max_selections=5)
if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    ingredients_string = ''
    #st.write(','.join(ingredients_list))
    for ingredient in ingredients_list:
        ingredients_string += ingredient + ' ' 

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    time_to_insert = st.button('Submit Order')
    st.write(my_insert_stmt) 
    
    if time_to_insert:
         
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered,'+ name_on_order+'!', icon="✅")
