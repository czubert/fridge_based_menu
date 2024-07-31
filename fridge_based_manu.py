import base64
import random
import re
import os

from openai import OpenAI
import json

client = OpenAI()

# OpenAI API Key - environmental variable
api_key = os.environ['api_key']


class FridgeMenu:
    def __init__(self):
        self.ingredients = ''
        self.meals_props = ''
        self.chosen_meal_prop = None
        self.instruction = ''
        self.meal_num = random.randint(0, 2)
        self.dish_image_url = None

    def prepare_meal(self, path):
        fridge_image = FridgeMenu.encode_image_from_path(path)
        self.get_ingredients(fridge_image)
        print("Ingredients: ")
        [print(x) for x in self.ingredients]
        self.get_meal_propositions('dinner')
        print("\nMeals Propositions: ")
        [print(p['name'] + " - " + p['description']) for p in self.meals_props]
        self.chosen_meal_prop = self.meals_props[self.meal_num]['name'] + " - " + self.meals_props[self.meal_num][
            'description']
        self.get_instructions()
        print(self.instruction)
        self.dish_image_url = self.create_meal_picture()

    def get_ingredients(self, fridge_image):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant designed to output JSON."
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "List products in the image."
                                    "There might be some cans and bottles containing alcohol."
                                    "There might be some vegetables in the drowers at the bottom of the fridge."
                                    "List as many products as you can."
                                    "Provide answer output following the given format:"
                                    "{„fridge_content”: [„item1”, „item2”]}",
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{fridge_image}",
                            },
                        },
                    ],
                }
            ],
            max_tokens=900,
        )

        json_txt = response.choices[0].message.content
        self.ingredients = json.loads(json_txt)['fridge_content']

    @staticmethod
    def encode_image_from_path(path):
        with open(path, "rb") as image_file:
            return FridgeMenu.encode_image(image_file)

    @staticmethod
    def encode_image(image_file):
        return base64.b64encode(image_file.read()).decode('utf-8')

    def get_meal_propositions(self, chosen_type_of_meal):
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=
            [
                {
                    "role": "system",
                    "content": "You are a master chef, skilled in preparing fine meals with creative flair."
                               "You are a helpful assistant designed to output JSON."
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"Suggest exactly the names of three possible meals "
                                    f"you can prepare for {chosen_type_of_meal}"
                                    f"using the ingredients from the list: {self.ingredients}. "
                                    f"Combine name with short description in one line."
                                    "Provide answer output following the given format:"
                                    "{'proposals': ["
                                    "{'name': 'Vegetable stir-fry', 'description': 'Vegetable stir-fry with a tangy sauce, served over packaged rice for a quick and colorful meal.'},"
                                    "{'name': 'Cheesy vegetable quesadillas', 'description': 'Cheesy vegetable quesadillas accompanied by a refreshing fruit juice, perfect for a light dinner.'},"
                                    "{'name': 'Savory baked cheese and vegetable fritters', 'description': 'Savory baked cheese and vegetable fritters served with a side of creamy milk dip for extra flavor.'},"
                                    "]"
                                    "}"
                        },
                    ]
                },
            ]
        )
        json_txt = completion.choices[0].message.content
        self.meals_props = json.loads(json_txt)['proposals']

    def get_instructions(self):
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=
            [
                {
                    "role": "system",
                    "content": "You are a master chef, skilled in preparing fine meals with creative flair."
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"Give me the detailed recipe for the following dish: {self.chosen_meal_prop}"
                                    f"using the ingredients from the list: {self.ingredients}."
                                    f"Do not add intro nor outro to the recipe!"
                                    f"Follow the Markdown formatting."
                        },
                    ]
                },
            ]
        )

        self.instruction = completion.choices[0].message.content

    def create_meal_picture(self):
        response = client.images.generate(
            model="dall-e-3",
            prompt=f"Prepare realistic image of the {self.chosen_meal_prop} dish. Do not too many items there."
                   f"which was prepared according to the following recipe: {self.instruction}",
            size="1024x1024",
            quality="standard",
            n=1,
        )

        return response.data[0].url


if __name__ == '__main__':
    image_path = "img/6a91cb43-691d-4a97-a634-4d6692b4e670.jpg"
    dish = FridgeMenu()
    dish.prepare_meal(image_path)
