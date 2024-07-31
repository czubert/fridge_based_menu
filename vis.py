import io

import streamlit as st
import fridge_based_manu

# # Initialize session state variables if they do not exist
if 'uploaded_photo' not in st.session_state:
    st.session_state.uploaded_photo = None
if 'ingredients' not in st.session_state:
    st.session_state.ingredients = None
if 'meals_props' not in st.session_state:
    st.session_state.meals_props = None
if 'chosen_meal_prop' not in st.session_state:
    st.session_state.chosen_meal_prop = None
    

def uploaded_photo_act():
    for key in st.session_state.keys():
        if key != 'uploaded_photo':
            del st.session_state[key]


def meal_time_act():
    for key in st.session_state.keys():
        if key != 'ingredients' and key != 'uploaded_photo':
            del st.session_state[key]


st.sidebar.write("Upload photo and choose meal time")
st.sidebar.markdown('---')
# # # Uploading photo
uploaded_photo = st.sidebar.file_uploader("Upload fridge image", type=["jpg", 'png'], on_change=uploaded_photo_act)
st.session_state.uploaded_photo = uploaded_photo

# # # Getting propositions of the meal
meal_time = ['Breakfast', 'Dinner', 'Supper']
chosen_time_of_meal = st.sidebar.selectbox('Choose meal timee', meal_time, on_change=meal_time_act)
st.session_state.chosen_time_of_meal = chosen_time_of_meal

if uploaded_photo:
    # Getting an instance of the class FridgeMenu
    dish = fridge_based_manu.FridgeMenu()

    # Changing uploaded photo to io.BytesIO and decoding to base64 type
    uploaded_photo = uploaded_photo.getvalue()
    image = io.BytesIO(uploaded_photo)
    image = dish.encode_image(image)

    # # # Showing ingredients recognized in the photo
    with st.expander("Ingredients recognized in the photo:"):
        if st.session_state.ingredients is None:
            dish.get_ingredients(image)
            st.session_state.ingredients = dish.ingredients

        st.write(', '.join(st.session_state.ingredients))

    # # # Showing propositions of the dishes
    with st.expander('Dishes suggestions for your meal:'):
        if st.session_state.meals_props is None:
            dish.get_meal_propositions(chosen_time_of_meal)
            st.session_state.meals_props = dish.meals_props

        for el in st.session_state.meals_props:
            st.write(el['name'] + ' - ' + el['description'])

    # # # Choosing one dish from propositions
    options = [x['name'] for x in st.session_state.meals_props]  # preparing list of dishes for select box
    dish.chosen_meal_prop = st.selectbox('What dish you choose?', options=options)
    st.session_state.chosen_meal_prop = dish.chosen_meal_prop

    # # # Generating chosen dish from your ingredients from the fridge

    if st.button('Generate recip!'):
        if st.button('Generate picture of your meal!'):
            st.image(dish.create_meal_picture())

        with st.expander('Show full instruction of the chosen dish'):
            dish.get_instructions()
            st.write(dish.instruction)



