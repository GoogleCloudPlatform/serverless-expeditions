# Copyright 2024 Google, LLC. This software is provided as-is,
# without warranty or representation for any use or purpose. Your
# use of it is subject to your agreement with Google.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Google genai API for Gemini
from google.genai.types import (
    HttpOptions, GoogleSearch, GenerateContentConfig, SafetySetting, Tool, HarmCategory, HarmBlockThreshold
)
from google.genai import types
from google import genai

# Google Vertex AI API for Imagen
from vertexai.preview.vision_models import ImageGenerationModel
import vertexai

import streamlit as st
import base64

# safety setting
safety_settings = [
    SafetySetting(
        category=HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    ),
    SafetySetting(
        category=HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    ),
    SafetySetting(
        category=HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    ),
    SafetySetting(
        category=HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    ),
]


def generate_llm(model_name: str, system_instruction: str, prompt: str) -> tuple:
    """
    Generic interface for LLM applications
    :param model_name: name of the model to be used as string
    :param system_instruction: system instruction as string
    :param prompt: instructions as string
    :return: (generated output as string, grounding information)
    """

    # Create the VertexAI client
    client = None
    if 'project_id' in st.session_state.keys() and st.session_state['project_id'] != "":
        client = genai.Client(
            vertexai=True, 
            project=st.session_state['project_id'], 
            location=st.session_state['location'],
            http_options=HttpOptions(api_version="v1")
        )

    if not client:
        return ("Impossible to reach Gemini, did you choose the GCP project in the setting?", "")

    # Get the response
    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
        config=GenerateContentConfig(
            tools=[Tool(google_search=GoogleSearch())],
            temperature=1.0,
            max_output_tokens=2048,
            safety_settings=safety_settings
        )
    )

    if response.text:
        text = response.text
        grounding_content = response.candidates[0].grounding_metadata.search_entry_point.rendered_content
    else:
        text = "I was not able to answer your question, please retry or modify slightly your question..."
        grounding_content = ""

    return (text, grounding_content)


def generate_lmm(model_name: str, system_instruction: str, prompt: str, uploaded_metadata: tuple) -> str:
    """
    Generic interface for LMM applications
    :param model_name: name of the model to be used as string
    :param system_instruction: system instruction as string
    :param prompt: instructions as string
    :param uploaded_metadata: (mime-type, image gcs uri)
    :return: generated output as string
    """

    # Create the VertexAI client
    client = None
    if 'project_id' in st.session_state.keys() and st.session_state['project_id'] != "":
        client = genai.Client(
            vertexai=True, 
            project=st.session_state['project_id'], 
            location=st.session_state['location'],
            http_options=HttpOptions(api_version="v1")
        )

    if not client:
        return ("Impossible to reach Gemini, did you choose the GCP project in the setting?", "")

    mime_type, uri = uploaded_metadata

    # Encode the image content
    image = types.Part.from_uri(
        mime_type=mime_type,
        file_uri=uri
    )

    # Get the response
    contents = [
    types.Content(
      role="user",
      parts=[
        image,
        types.Part.from_text(text=prompt)
      ]
    ),
  ]

    # Generation Config
    generate_content_config = types.GenerateContentConfig(
        temperature = 1,
        top_p = 1,
        seed = 0,
        max_output_tokens = 2048,
        safety_settings = safety_settings,
        system_instruction=[types.Part.from_text(text=system_instruction)],
        thinking_config=types.ThinkingConfig(
            thinking_budget=0
        )
    )

    response = client.models.generate_content(
        model = model_name,
        contents = contents,
        config = generate_content_config
    )

    return (response.text)


def create_chat_session(model_name: str, system_instruction: str):
    """
    Create a new chat session
    :param model_name: model name as string
    :param system_instruction: system instruction as string
    :return: chat session
    """

    # Create the VertexAI client
    client = None
    if 'project_id' in st.session_state.keys() and st.session_state['project_id'] != "":
        client = genai.Client(
            vertexai=True, 
            project=st.session_state['project_id'], 
            location=st.session_state['location'],
            http_options=HttpOptions(api_version="v1")
        )

    if not client:
        return ("Impossible to reach Gemini, did you choose the GCP project in the setting?", "")

    # Generation Config
    generate_content_config = types.GenerateContentConfig(
        temperature = 1,
        top_p = 1,
        seed = 0,
        safety_settings = safety_settings,
        system_instruction=[types.Part.from_text(text=system_instruction)],
        thinking_config=types.ThinkingConfig(thinking_budget=0)
    )

    # create the chat session
    chat_session = client.chats.create(
        model=model_name,
        config=generate_content_config,
        history=[]
    )

    return chat_session


def generate_images(
    model_name: str, 
    prompt: str, 
    number_of_images: int=1, 
    aspect_ratio: str = "1:1",
    person_generation="allow_all",
    watermarking: bool=False
):
    """
    Generate Images following prompt.
    :param model_name: name of the generative model
    :param prompt: instructions
    :param number_of_images: number of images to be generated
    :param aspect_ratio: aspect ratio of the generated images
    :param person_generation: authorization for person generation
    :param watermarking: add watermark if True
    :return: list of images
    """

    # setup of the safety filter
    safety_filter="block_some"

    imagen_model = ImageGenerationModel.from_pretrained(
        model_name
    )

    # generate the images
    images = imagen_model.generate_images(
        prompt=prompt,
        number_of_images=number_of_images,
        aspect_ratio=aspect_ratio,
        safety_filter_level=safety_filter,
        person_generation=person_generation,
        add_watermark=watermarking
    )

    return images
