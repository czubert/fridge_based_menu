import base64
import random
import re
import os

from openai import OpenAI
import json

# OpenAI API Key
api_key = os.environ['api_key']


class FridgeMenu:
    def __init__(self):
        self.ingredients = ''
        self.meals_propositions = ''
        self.chosen_meal_proposition = None
        self.instruction = ''

    def prepare_meal(self, path):
        self.get_ingredients(path)
        print(self.ingredients)
        self.get_meal_propositions('dinner')
        print('\n'.join(self.meals_propositions))
        self.get_instructions(self.meals_propositions[random.randint(1, 3)])
        print(self.instruction)

    def get_ingredients(self, path):
        base64_image = self.encode_image(path)

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "List products in the image."
                                    "There might be some cans and bottles containing alcohol."
                                    "There might be some vegetables in the drowers at the bottom of the fridge."
                                    "List as many products as you can.",
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                            },
                        },
                    ],
                }
            ],
            max_tokens=300,
        )
        result = response.json()
        result_dict = json.loads(result)
        self.ingredients = result_dict['choices'][0]['message']['content']

    @staticmethod
    def encode_image(path):
        with open(path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def get_meal_propositions(self, chosen_type_of_meal):
        client = OpenAI()

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
                            "text": f"Suggest exactly the names of three possible meals you can prepare for {chosen_type_of_meal}"
                                    f"using the ingredioents from the list: {self.ingredients}. "
                                    f"Combine name with short description in one line."
                        },
                    ]
                },
            ]
        )
        result = completion.json()
        result_dict = json.loads(result)
        result = result_dict['choices'][0]['message']['content'].replace('\n\n', '\n').split('\n')
        meals_propositions = result

        self.meals_propositions = meals_propositions

    def get_instructions(self, chosen_meal):
        client = OpenAI()

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
                            "text": f"Give me the detailed recipe for the following dish: {chosen_meal}"
                                    f"using the ingredients from the list: {self.ingredients}."
                        },
                    ]
                },
            ]
        )
        result = completion.json()
        result_dict = json.loads(result)
        self.instruction = result_dict['choices'][0]['message']['content']

    def create_meal_picture(self):
        client = OpenAI()

        response = client.images.generate(
            model="dall-e-3",
            prompt=self.instruction,
            size="1024x1024",
            quality="standard",
            n=1,
        )

        return response.data[0].url

if __name__ == '__main__':
    image_path = "img/6a91cb43-691d-4a97-a634-4d6692b4e670.jpg"
    dish = FridgeMenu()
    dish.prepare_meal(image_path)
