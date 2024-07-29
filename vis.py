import io

import streamlit as st
import fridge_based_manu


st.sidebar.write("Upload photo and choose meal time")
st.sidebar.markdown('---')
# # # Uploading photo
uploaded_photo = st.sidebar.file_uploader("Upload fridge image", type=["jpg", 'png'], key="uploaded_photo")

# # # Getting propositions of the meal
chosen_time_of_meal = st.sidebar.selectbox('Choose meal timee', ['Breakfast', 'Dinner', 'Supper'], key="chosen_time")

st.write(st.session_state)

if uploaded_photo:

    # Getting an instance of the class FridgeMenu
    dish = fridge_based_manu.FridgeMenu()

    # Changing uploaded photo to io.BytesIO and decoding to base64 type
    uploaded_photo = uploaded_photo.getvalue()
    image =io.BytesIO(uploaded_photo)
    image = dish.encode_image(image)

    # # # Showing ingredients recognized in the photo
    with st.expander("Ingredients recognized in the photo:"):
        dish.get_ingredients(image)

        st.write(', '.join(dish.ingredients))

    with st.expander('Dishes suggestions for your meal:'):
        dish.get_meal_propositions(chosen_time_of_meal)

        for el in dish.meals_props:
            st.write(el['name'] + ' - ' + el['description'])

    options = [x['name'] for x in dish.meals_props]
    dish.chosen_meal_prop = st.selectbox('What dish did you choose?', options=options, key='chosen_meal_prop')

    dish.get_instructions()
    with st.expander('Show full instruction of the chosen dish'):
        st.write(dish.instruction)

    # st.image(dish.create_meal_picture())
