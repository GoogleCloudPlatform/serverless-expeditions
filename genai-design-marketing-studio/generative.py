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

from vertexai.generative_models import GenerativeModel, Part, SafetySetting, FinishReason, Tool
from vertexai.preview.vision_models import ImageGenerationModel
import vertexai.generative_models as generative_models
import vertexai
import base64


# configuration parameters
generation_config = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
}

# safety setting
safety_settings = [
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_ONLY_HIGH
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_ONLY_HIGH
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_ONLY_HIGH
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_ONLY_HIGH
    ),
]

# tool for answers grounding
tools = [
    Tool.from_google_search_retrieval(
        google_search_retrieval=generative_models.grounding.GoogleSearchRetrieval()
    )
]


def generate_llm(model_name: str, system_instruction: str, prompt: str) -> str:
    """
    Generic interface for LLM applications
    :param model_name: name of the model to be used as string
    :param system_instruction: system instruction as string
    :param prompt: instructions as string
    :return: generated output as string
    """
  
    # Init the model
    model = GenerativeModel(
        model_name,
        system_instruction=[system_instruction],
        tools=tools
    )

    # Get the response
    response = model.generate_content(
        [prompt],
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=False
    )

    return (response.text)


def generate_lmm(model_name: str, system_instruction: str, prompt: str, uploaded_metadata: tuple) -> str:
    """
    Generic interface for LMM applications
    :param model_name: name of the model to be used as string
    :param system_instruction: system instruction as string
    :param prompt: instructions as string
    :param uploaded_metadata: (mime-type, image gcs uri)
    :return: generated output as string
    """

    # Init the model
    model = GenerativeModel(
        model_name,
        system_instruction=[system_instruction]
    )

    mime_type, uri = uploaded_metadata

    # Encode the image content
    image = Part.from_uri(
        mime_type=mime_type,
        uri=uri
    )

    # Get the response
    response = model.generate_content(
        [image, prompt],
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=False
    )

    return (response.text)


def create_chat_session(model_name: str, system_instruction: str):
    """
    Create a new chat session
    :param model_name: model name as string
    :param system_instruction: system instruction as string
    :return: chat session
    """

    model = GenerativeModel(
        model_name=model_name,
        generation_config=generation_config,
        safety_settings=safety_settings,
        system_instruction=[system_instruction]
    )

    return model.start_chat(history=[])


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
