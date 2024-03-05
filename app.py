# Copyright 2024 Sandra Calvo
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
import json
import csv
import pandas as pd 
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part

def generate_descriptions(product_data, prompt, temperature, image_url=None):
    model = GenerativeModel("gemini-pro-vision")

    # Incorporate product data into the prompt
    prompt = f"""{json.dumps(product_data)}{prompt}""" 

    responses = model.generate_content(
        prompt,
        generation_config={
            "max_output_tokens": 2048,
            "temperature": temperature,
            "top_p": 1,
            "top_k": 32
        },
        safety_settings=[],
        stream=True
    )

    output = {
        "product_data": product_data,  # Add product data
        "prompt": prompt,              # Add the prompt
        "description": []
    }

    for response in responses:
         output["description"].append(response.text)

    return output

def main():
    st.title("Product Description Generator")

    # Prompt input
    prompt = st.text_area("Write a prompt to send to the AI model", height=200)  

    # Upload product data file
    uploaded_file = st.file_uploader("Upload product data file (JSON or CSV)")
    
    # Temperature slider
    temperature = st.slider("Temperature", 0.0, 1.0, 0.4)

    # Add text above the temperature slider
    st.markdown("The temperature parameter controls the randomness of the generated descriptions. A higher temperature value will result in more random descriptions, while a lower temperature value will result in more structured descriptions.")

    # Image URL input
    image_url = st.text_input("[Optional]Enter the URL of the image", value="")

    # Generate descriptions button
    if st.button("Generate descriptions"):

        if uploaded_file is not None:
            if uploaded_file.name.lower().endswith('.json'):  # Check file extension
                product_data = json.load(uploaded_file)
            elif uploaded_file.name.lower().endswith('.csv'):
                product_data = pd.read_csv(uploaded_file).to_dict(orient='records')  # Use pandas to read CSV
            else:
                st.error("Please upload a JSON or CSV file.")
                return

            # Generate descriptions
            output = generate_descriptions(product_data, prompt, temperature, image_url)
            for description in output['description']:
                st.write(description)

    # Add CSS for word-wrapping
    st.markdown("""
        <style>
        .stText { 
            word-break: break-word; /* Force word-wrapping */
        }
        </style>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
