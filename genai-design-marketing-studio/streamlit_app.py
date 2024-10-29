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

from generative import generate_llm, generate_lmm, create_chat_session, generate_images

from google.cloud import storage
import vertexai

from pathlib import Path
import streamlit as st
import mimetypes
import json
import math
import os

# mimetypes init
mimetypes.init()


# ENGINE
##########################################################

@st.cache_resource()
def load_prompts() -> dict:
    """
    Load the prompts library in the Streamlite session state"
    :return: prompts as a dict
    ""
    with open("./prompts/prompts.json") as f:
        return json.load(f)


def librarian_assistant(query: str) -> str:
    """
    Wrapper on Gemini for answering questions as a librarian assistant.
    :param query: user query as string
    :return: generated output as string
    """

    # system instructions
    persona = st.session_state['prompts']['librarian_assistant_persona']

    # prompt
    prompt = st.session_state['prompts']['librarian_assistant'].format(query=query)

    # model name
    model_name = "gemini-1.5-flash-001"

    return (generate_llm(model_name, persona, query))


def image_captioning(uploaded_metadata: tuple, prompt:str) -> str:
    """
    Wrapper on Gemini for answering questions as an image caption generator
    :param uploaded_metadata: (content_type, gs:// uri of the created blob)
    :param prompt: prompt
    :return: generated caption as string
    """

    # system instructions
    persona = st.session_state['prompts']['image_captioning_persona']

    # model name
    model_name = "gemini-1.5-flash-001"

    return (generate_lmm(model_name, persona, prompt, uploaded_metadata))


def upload_object_on_gcs(content: str, bucket_name: str, prefix_blob_name: str) -> str:
    """
    Upload the given content to the GCS in the given bucket and given prefixed name
    :param content: content to be uploaded as a string
    :param bucket_name: name of the bucket where the content has to be uploaded
    :param prefix_blob_name: prefixed (folder(s)) name of the blob to create
    :return: (content_type, gs:// uri of the created blob)
    """
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(prefix_blob_name)

    mime_type = mimetypes.guess_type(prefix_blob_name)
    blob.upload_from_string(content, content_type=mime_type[0])
    return (mime_type[0], f"gs://{bucket_name}/{prefix_blob_name}")


def writing_assistant(key: str, persona: str) -> None:
    """
    Manage the conversation for the writing assistant.
    :param key: streamlit key to identify the UI element
    :param persona: the personal of the chatbot.
    :return: None
    """

    # model name
    model_name = "gemini-1.5-flash-001"

    # Init the conversation
    with st.container():
        message = st.chat_input("👋 Hello, How can I help you today?", key=f"{key}_input")
    with st.container(height=400):
        if message and message != "👋 Hello, How can I help you today?":
            # init the chat history in the session state
            if f'{key}_text_chat_history' not in st.session_state:
                chat_session = create_chat_session(model_name, persona)
                st.session_state[f'{key}_text_chat_history'] = []
                st.session_state[f'{key}_text_chat_session'] = chat_session

            # Display chat messages from history on app rerun
            for m in st.session_state[f'{key}_text_chat_history']:
                with st.chat_message(m["role"]):
                    st.markdown(m["content"])

            # Add user message to chat history
            st.session_state[f'{key}_text_chat_history'].append({"role": "user", "content": message})

            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(message)
            with st.chat_message("assistant"):
                current_chat_session = st.session_state[f'{key}_text_chat_session']
                responses = st.session_state[f'{key}_text_chat_session'].send_message(message, stream=True)
                texts = [r.text for r in responses]
                full_response = ""
                for t in texts:
                    full_response += ' ' + t
                st.write_stream(texts)
                st.session_state[f'{key}_text_chat_history'].append(
                    {"role": "assistant", "content": full_response}
                )


def image_assistant(
    prompt: str,
    number_of_images: int=1,
    aspect_ratio: str="1:1",
    person_safety: str="dont_allow",
    watermarking: bool=False,
    model_name: str="imagen-3.0-generate-001"
) -> None:
    """
    Wrapper around Imagen3 Image generation
    :param prompt: prompt instructions as string
    :param number_of_images: number of images to be generated
    :param aspect_ratio: aspect ratio of the generated images
    :param person_safety: allowing adults or not in the images
    :param watermarking: watermark the generated images
    :param model_name: name of the Imagen3 model to be used
    :return: None
    """

    return (generate_images(
        model_name,
        prompt,
        number_of_images,
        aspect_ratio,
        person_safety,
        watermarking
    ))


def image_generation_cols(nb_image: bool=True, allow_kids: bool=False) -> None:
    """
    Image generation parameters columns
    :param nb_image: add a column for choosing how many images are generated if True
    :param allow_kids: add the allow_all option if True
    :return: None
    """

    nb_columns = 4 if nb_image else 3
    cols = st.columns(nb_columns)
    i = 0

    if nb_image:
        with cols[i]:
            number_of_images = st.number_input(
                "Number of images",
                min_value=1,
                max_value=4
            )
        i += 1
    else:
        number_of_images = 1

    with cols[i]:
        aspect_ratio = st.selectbox(
            "Aspect Ratio",
            options=["1:1", "4:3", "3:4", "9:16", "16:9"],
            index=0
        )
    i += 1

    with cols[i]:
        options = ["allow_adult", "dont_allow"]
        if allow_kids:
            options.prepend("allow_all")
        person_safety = st.selectbox(
            "Allow Person",
            options=options,
            index=0
        )
    i += 1

    with cols[i]:
        watermarking = st.checkbox("Watermark")

    return number_of_images, aspect_ratio, person_safety, watermarking


def image_generation_ui(
    prompt: str,
    bucket_name: str,
    folder_name: str=None,
    prefix_blob_name: str=None,
    nb_image: bool=True, allow_kids: bool=False,
    model_choice: bool=False,
    checkbox_label: str="Save generated images",
    button_label :str="Generate images..."
) -> None:
    """
    UI for Image generation with GCS saving capacity
    :param prompt: prompt instructions as string
    :param bucket_name: name of the bucket where the images will be saved
    :param folder_name: name of the folder where the images will be saved
    :param prefix_blob_name: prefixed (folder(s)) name of the blob to create
    :param nb_image: add a column for choosing how many images generated if True
    :param allow_kids: add the allow_all option if True
    :param model_choice: add the model choice option if True
    :param checkbox_label: label of the saving checkbox as String
    :param button_label: label of the button as String
    :return None
    """

    # nb of images, aspect ratio, allowing person and watermark
    number_of_images, aspect_ratio, person_safety, watermarking = image_generation_cols(nb_image=nb_image)

    # model name
    model_name = "imagen-3.0-generate-001"
    if model_choice:
        model_name = st.selectbox(
            "Model", options=["imagen-3.0-fast-generate-001", "imagen-3.0-generate-001"]
        )

    # Generation and Display of images
    gen_col, display_col = st.columns([4, 6])

    # generating/saving
    with gen_col:
        save_generated_images = st.checkbox(checkbox_label)
        if not folder_name:
            folder_name = st.text_input("Image(s) Folder")
            folder_name = f"{prefix_blob_name}/{folder_name}"
        generate_images_submitted = st.form_submit_button(button_label)

    # display the generated images
    gen_images = None
    with display_col:
        if generate_images_submitted:
            gen_images = image_assistant(
                prompt, number_of_images, aspect_ratio,
                person_safety, watermarking, model_name
            )
            if gen_images and len(list(gen_images)) > 0:
                for gen_image in gen_images:
                    st.image(gen_image._pil_image)
            else:
                st.error("No images generated. Please retry.")

    # saving the generated images on GCS
    if save_generated_images and gen_images:
        upload_object_on_gcs(prompt, bucket_name, f"{folder_name}/latest_prompt.txt")
        counter_start = len(list(storage_client.list_blobs(bucket_name, prefix=f"{folder_name}")))
        for i, gen_image in enumerate(gen_images):
            upload_object_on_gcs(gen_image._image_bytes, bucket_name, f"{folder_name}/{counter_start+i}.png")


##########################################################
# APPLICATION USER INTERFACE AND BACKBONE

# load the prompts from the resource files
# and store them in the session state
st.session_state['prompts'] = load_prompts()

st.title(":dizzy: GenAI Creative Assistant")

st.markdown("""
Welcome to the Generative AI Creative Assistant Platform.
Here you will find a GenAI toolbox to help you with the:
- Moodboards Creation
- Documentation (External Resources Search)
- ChatBot Ideation
- Image Content Ideation
- Patrimonial Search (Internal Resources Search)
- Marketing Ideation
"""
)

st.warning("But first, let's setup the application in your Google Cloud environment.")

with st.expander("Project Settings"):
    with st.form("Settings"):
        # init project id and quota project id
        project_id = st.text_input("Project Id", "")
        os.environ["GOOGLE_CLOUD_QUOTA_PROJECT"] = project_id

        # init region
        region = st.text_input("Region", "us-central1")
        location = region.split("-")[0]

        bucket_name = st.text_input("Bucket name", f"{project_id}-genai-design-studio")
        storage_client = storage.Client(project=project_id)

        submitted = st.form_submit_button("Save settings")

    if submitted:
         # init vertex ai
        vertexai.init(project=project_id, location=region)

        # bucket creation if the bucket does not exist
        try:
            storage_client.create_bucket(bucket_name, location=location)
        except:
            st.warning("The bucket already exists...")


st.info("Navigate though the different tabs to find the tools that you need.")

# load the prompts library
load_prompts()

# Multi-tab UI
tab_doc_assistant, tab_mood_gen, tab_text_gen, tab_img_gen, tab_market_gen = st.tabs(
    [
        'Documentation Assistant', 'Moodboards',  'Ideation Assistant', 'Image Assistant', 
         'Marketing Assistant'
    ]
)

# Documentation Assistant
with tab_doc_assistant:

    st.markdown("""
        In this section, you can:
        - Ask the Documentation Assistant any question you may have.
    """)

    # Library
    st.subheader("Documentation Assistant")
    with st.form(key="library_k"):

        # question sent to Gemini
        librarian_query = st.text_input("Question:")

        submitted = st.form_submit_button("Answer...")
        if submitted:
            # output generated by Gemini
            output, grounding = librarian_assistant(librarian_query)
            st.markdown(output)
            st.markdown(grounding, unsafe_allow_html=True)


# Moodboard Assistant
with tab_mood_gen:
    st.markdown("""
    In this section, you can create moodboards.
    Just describe vaguely or precisely the thematics of the moodboard and\
    let the Assistant draft something for you.
    """)

    st.subheader("Moodboards Creation Assistant")

    st.info("The draft moodboard is saved in a folder named from its title. Several moodboards can be saved with the same title.")

    # instruction
    with st.form(key="Mood_k"):

        # moodboard parameters
        title = st.text_input("Title")
        keywords = st.text_input("Keywords/Vibes", "use commas between keywords")
        target_audience = st.text_input("Target audience")

        # moodboard prompt
        with st.expander("Moodboard Assistant Prompt (can be modified if needed)"):
            prompt = st.text_area("Moodboard Assistant Prompt", st.session_state['prompts']['moodboard'], height=150)

        # use the moodboard details example loaded with the prompts
        content_notes_example = st.session_state['prompts']['moodboard_details']
        content_notes = st.text_area("Content intructions (can be modified if needed)", f"{content_notes_example}", height=300)

        # prompt
        prompt = st.session_state['prompts']['moodboard'].format(
            title=title,
            keywords=keywords,
            target_audience=target_audience,
            layout_notes=content_notes
        )

        # image generation ui
        image_generation_ui(
            prompt=prompt,
            bucket_name=bucket_name,
            folder_name=f"generated_moodboards/{title}",
            nb_image=True, 
            allow_kids=False,
            model_choice=True,
            checkbox_label="Save generated moodboard",
            button_label="Draft a moodboard..."
        )

# Writing Assistant
with tab_text_gen:

    st.markdown("""
        In this section, you can:
        - Run text ideation with the Assistant,
        - Ask the Assistant to analyze pictures and illustrations
    """)

    # bot interface
    st.subheader("Ideation Co-Writing")

    st.info("You can save the conversation in a named folder. Do not forget to specific this name before resting the chatbot")

    # Persona
    with st.expander("Writing Assistant Persona (can be modified if needed)"):
        writing_assistant_persona = st.text_area(
            "Writing Assistant Persona",
            st.session_state['prompts']['writing_assistant_persona'],
            height=150
        )

    key_writing = "writing"
    writing_assistant(key=key_writing, persona=writing_assistant_persona)

    writing_col1, writing_col2 = st.columns([6, 4])

    with writing_col1:
        conversation_name = st.text_input("Conversation name")

    with writing_col2:

        # save conversation button
        save_writing_chat_button = st.button(
            "Save Ideation conversation", 
            disabled=not f'{key_writing}_text_chat_history' in st.session_state.keys()
        )
        if save_writing_chat_button and f'{key_writing}_text_chat_history' in st.session_state.keys():
            saved_conversation_string = ""
            for m in st.session_state[f'{key_writing}_text_chat_history']:
                saved_conversation_string += f"{m['role']}: {m['content']}\n"
            upload_object_on_gcs(
                saved_conversation_string,
                bucket_name,
                f"ideation_conversations/{conversation_name}.txt",
            )

        # reset conversation button
        reset_chat_button = st.button(
            "Reset conversation", key=f"{key_writing}_reset",
            disabled=not f'{key_writing}_text_chat_history' in st.session_state.keys()
        )
        if reset_chat_button and f'{key_writing}_text_chat_history' in st.session_state.keys():
            del st.session_state[f'{key_writing}_text_chat_history']

    # Image Captioning
    st.subheader("Products Analysis")

    st.info("You can save the generated caption using the filename of the image that you have uploaded.")

    # upload the file and save it in GSC bucket
    uploaded_file = st.file_uploader(label="Import an image", type=['png', 'jpeg', 'jpg'])
    if uploaded_file is not None:
        image = uploaded_file
        uploaded_metadata = upload_object_on_gcs(image.getvalue(), bucket_name, f"uploaded_pictures/{uploaded_file.name}")
        st.image(image)

    # generate a caption and save it in GCS bucket
    with st.form(key="Captioning_k"):

        with st.expander("Product Analysis Prompt (can be modified if needed)"):
            captioning_prompt = st.text_area(
                "Product Analysis Prompt",
                st.session_state['prompts']['image_captioning'],
                height=200
            )

        col_img_captioning_1, col_img_captioning_2 = st.columns([8,2])

        # button
        with col_img_captioning_1:
            caption_submitted = st.form_submit_button("Caption the image...")
            if caption_submitted:
                output = image_captioning(uploaded_metadata, captioning_prompt)
                st.markdown(output)

        # saving checkbox
        with col_img_captioning_2:
            save_caption = st.checkbox("Save caption")

        # saving the captions on GCS
        if save_caption and caption_submitted:
            text_filename = Path(uploaded_file.name).stem
            upload_object_on_gcs(output, bucket_name, f"uploaded_pictures_captions/{text_filename}_caption.txt")


# Image Assistant
with tab_img_gen:
    st.markdown("""
    In this section, you can:
    - Sketch ideas and prototypes
    - Generate photorealistic images

    Just describe precisely what you want the Image Assistant\
    to generate, and it will be done.
    """)

    st.subheader("Design Visual Assistant")

    st.info("The draft images are saved in a named folder. Do not forget to specific this name before generating the images if you want to save the images.")

    # instruction
    with st.form(key="ImageGen_k"):

        prompt = st.text_area("Instructions", height=170)

        # image generation ui
        image_generation_ui(
            prompt=prompt,
            bucket_name=bucket_name,
            prefix_blob_name=f"generated_pictures",
            nb_image=True,
            allow_kids=False,
            model_choice=True
        )

# Marketing Assistant
with tab_market_gen:

    st.markdown("""
        In this section, you can:
        - Interact with a Marketing Assistant to brainstorm about your next campaign,
        - Ask the Assistant to create pictures and illustrations from your conversation
    """)

    # bot interface
    st.subheader("Marketing Co-Writing")

    st.info("You can save the conversation in a named folder. Do not forget to specific this name before resting the chatbot")

    # Persona
    with st.expander("Marketing Assistant Persona (can be modified if needed)"):
        marketing_assistant_persona = st.text_area(
            "Marketing Assistant Persona",
            st.session_state['prompts']['marketing_assistant_persona'],
            height=150
        )

    key_marketing = "marketing"
    writing_assistant(key=key_marketing, persona=marketing_assistant_persona)

    mark_writing_col1, mark_writing_col2 = st.columns([6, 4])

    with mark_writing_col1:
        conversation_name = st.text_input("Conversation name", key="mark_conversation_name")

    with mark_writing_col2:

        # save conversation button
        save_mark_chat_button = st.button(
            "Save Marketing conversation",
            disabled=not f'{key_marketing}_text_chat_history' in st.session_state.keys()
        )
        if save_mark_chat_button and f'{key_marketing}_text_chat_history' in st.session_state.keys():
            saved_conversation_string = ""
            for m in st.session_state[f'{key_marketing}_text_chat_history']:
                saved_conversation_string += f"{m['role']}: {m['content']}\n"
            upload_object_on_gcs(
                saved_conversation_string, 
                bucket_name, 
                f"marketing_conversations/{conversation_name}.txt",
            )

        # reset conversation button
        reset_chat_button = st.button(
            "Reset conversation", key=f"{key_marketing}_reset",
            disabled=not f'{key_marketing}_text_chat_history' in st.session_state.keys()
        )
        if reset_chat_button and f'{key_marketing}_text_chat_history' in st.session_state.keys():
            del st.session_state[f'{key_marketing}_text_chat_history']

    # Marketing Visual generator
    st.subheader("Marketing Visual Assistant")

    st.info("You can save the draft images in a named folder. \
        Do not forget to specify this name before generating the \
            images if you want to save the images."
    )

    # retrieve the marketing assistant chat history
    if f'{key_marketing}_text_chat_history' in st.session_state.keys():
        marketing_chat_history = st.session_state[f'{key_marketing}_text_chat_history']
    else:
        marketing_chat_history = ""

    with st.form(key="MarkGen_k"):

        prompt = st.text_area("Instructions", height=170)

        # enrich the prompt with the marketing chatbot history
        enriched_prompt = st.session_state['prompts']['markgeting_assitant_visual_prompt'].format(
            prompt=prompt,
            marketing_chat_history=marketing_chat_history
        )

        # image generation ui
        image_generation_ui(
            prompt=enriched_prompt,
            bucket_name=bucket_name,
            prefix_blob_name=f"generated_marketing_pictures",
            nb_image=True,
            allow_kids=False,
            model_choice=True
        )
