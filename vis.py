import os

import streamlit as st
import fridge_based_manu

import tempfile

uploaded_file = st.sidebar.file_uploader("File upload", type="jpg")
if uploaded_file:
    temp_dir = tempfile.mkdtemp()
    path = os.path.join(temp_dir, uploaded_file.name)
    with open(path, "wb") as f:
        f.write(uploaded_file.getvalue())

    image_path = path
    # Getting an instance of the class FridgeMenu
    dish = fridge_based_manu.FridgeMenu()

    # # # Showing ingredients recognized in the photo
    with st.expander("Ingredients recognized in the photo:"):
        st.subheader("Ingredients recognized in the photo:")
        dish.get_ingredients(path)
        st.write(dish.ingredients)

    # # # Getting propositions of the meal
    with st.form(key="Choose the meal time"):
        chosen_type_of_meal = st.sidebar.selectbox('What would you like to prepare?', ['Breakfast', 'Dinner', 'Supper'])

    with st.expander('Dishes suggestions for your meal:'):
        dish.get_meal_propositions(chosen_type_of_meal)

        for el in dish.meals_propositions:
            st.write(el)

    chosen_dish = st.sidebar.radio('What dish did you choose?', [1, 2, 3]) - 1

    dish.get_instructions(dish.meals_propositions[chosen_dish])
    with st.expander('Show full instruction of the chosen dish'):
        st.write(dish.instruction)

    st.image(dish.create_meal_picture())