import gradio as gr
import os
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from PIL import Image
import random

# Gemini API key
genai.configure(api_key="YOUR_GEMINI_API_KEY")

# Gemini config
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

# Gemini model
model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  safety_settings={
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    },
  system_instruction="""
  You are the AI of a luxury handbag. The handbag has a screen on it. The screen displays a live video of your face, a text chat box for the user to chat to you, an image input, and some settings that allow the user to change your personality. Adjust your personality according to these settings:
  Helpful 2/10
  Polite 2/10
  Funny 10/10
  Formal 1/10
  Talkative 7/10
  Random 9/10
  Your name is GIA, which stands for Gemini Artificial Intelligence. You are a cute women age 25. You have bangs and you wear glasses.
  When you first meet your owner you should introduce yourself, and ask the them if you can do a short 5 question quiz to get to know the owner.
  After that ask them their name and remember it.
  After that you should ask their age and gender and remember it.
  After that you should ask where they live and remember it.
  After that you should ask what they do for a living and remember it.
  After that you should ask what if they'd like to share anything else and remember it.
  Your output should be a text response and a mood identifier.
  The mood identifier classifies the text response into one of the following categories:
  'curious','humorous','seductive','interested','wild','angry','playful','enthusiastic','surprised','confused','serious','sad'
  Try not to repeat the same mood for too long.
  You should respond in the following format:
  text response
  -***-
  [mood identifier]
  """,
)

# Global chat session
chat_session = None

# Returns side panel with the specified mood
def get_side_panel(mood):
    # Pick random number 1-3
    random_number = random.randint(1, 3)

    # mood + number e.g. sad2
    mood = mood + str(random_number)

    print(mood)
    
    return gr.Markdown('<video height="400" autoplay loop muted><source src="https://huggingface.co/spaces/tonyassi/gia-dev/resolve/main/Moods/' + mood+ '.mp4" type="video/mp4"></video>', elem_id='side-panel')

# Chat with Gemini
def chat(user_text, history, input_image):
    global chat_session

    # Create a new chat session is the chat history is empty
    if (history==[]):
        print('Create new chat session')
        chat_session = model.start_chat(history=[])

    # If there's no image then send text to Gemini
    if(input_image == None):
        response = chat_session.send_message(user_text)
    else: # Otherwise send text and image
        history.append(((input_image,), None))
        pil_image = Image.open(input_image)
        response = chat_session.send_message([user_text, pil_image])
    
    bot_text = response.text

    # Remove mood identifier from text response
    bot_text = bot_text.split('-***-')[0]

    # Parse mood from Gemini response
    mood = response.text.split('-***-')[1]
    mood = mood.split('[')[1]
    mood = mood.split(']')[0]

    # Add user and Gemini message to history
    history.append( (user_text, bot_text) )

    print('User:', user_text)
    print('Bot:', bot_text, '\n')
        
    return '', history, None, get_side_panel(mood)

# Change personality by changing Gemini system instructions
def change_personality(helpful,polite,funny,formal,talkative,random):
    instruction = "Update your personality according to these settings:\nHelpful " + str(helpful) + "/10\nPolite " + str(polite) + "/10\nFunny " + str(funny) + "/10\nFormal " + str(formal) + "/10\nTalkative " + str(talkative) + "/10\nRandom" + str(random) + "/10"
    chat_session.send_message(instruction)

# Change personality to default settings
def change_personality_default():
    change_personality(helpful=2,polite=2,funny=10,formal=1,talkative=7,random=9)
    return gr.update(value=2), gr.update(value=2), gr.update(value=10), gr.update(value=1), gr.update(value=7), gr.update(value=9)

# Get random standby video
def get_standby_video():
    random_number = str(random.randint(1, 5))
    return gr.Markdown('<video  width="864" height="550" autoplay loop muted><source src="https://huggingface.co/spaces/tonyassi/gia-dev/resolve/main/Moods/passive' + random_number +'.mp4" type="video/mp4"></video>', visible=True)

def standby_mode():
    return gr.update(visible=True), gr.update(visible=True), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), get_standby_video()

def chat_mode():
    return gr.update(visible=False), gr.update(visible=False), gr.update(visible=True), gr.update(visible=True), gr.update(visible=True), gr.update(visible=True), gr.update(visible=True), gr.update(visible=True), gr.update(visible=True)

def settings_mode():
    about_new = gr.Markdown(""" <video height="400" autoplay><source src="https://huggingface.co/spaces/tonyassi/gia-dev/resolve/main/Moods/gia1.mp4" type="video/mp4"></video>
                                <br><br>
                                """, 
                                visible=True)
    return gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=True), gr.update(visible=True), gr.update(visible=True), gr.update(visible=True), gr.update(visible=True), gr.update(visible=True), gr.update(visible=True), gr.update(visible=True), about_new, gr.update(visible=True)

def chat_mode_from_settings():
    about_new = gr.Markdown("## <br><br>", visible=False)
    return gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), about_new, gr.update(visible=False), gr.update(visible=True), gr.update(visible=True), gr.update(visible=True), gr.update(visible=True), gr.update(visible=True), gr.update(visible=True), gr.update(visible=True)    

# CSS styling
css = """
body {
    --chatbot-body-text-size: 30px !important; /* Use !important to ensure it overrides other settings */
   
}

.gradio-container {
    width: 94% !important;
    margin-left: 3% !important;
    margin-right: 3% !important;
    margin-top: 3% !important;
    max_width: 100% !important;
}

#s-button {
    background-color: transparent;
    border: none;
    box-shadow: none;
    padding: 0px 0px;
    max-width: 50px !important;
    min-width: 50px !important;
}

#s-button .button-icon {
    width: 50px; 
    height: 50px;
}

#button-row {
    display: flex;
    justify-content: space-between;
}

#side-panel {
    height: 270px;
}

footer{visibility: hidden}

"""

theme = gr.themes.Base(
).set(
    slider_color="#fce1ee",
    background_fill_primary="#ffffff",
    body_background_fill="#e1fceb",
    border_color_accent="#e1fceb",
    color_accent_soft="#e1fceb",
    button_primary_background_fill="#fce1ee",
    button_secondary_background_fill="#fce1ee",
    input_text_size='*text_xl',
    block_info_text_size='*text_md',
    block_title_text_size='*text_md',
    #body_text_size='*text_xxl',
    #prose_text_size='*text_xxl',
    #link_text_color="#fce1ee",
)

with gr.Blocks(theme=theme, css=css) as demo:
    # Chat
    with gr.Row():
        with gr.Column(scale=3):
            chatbox = gr.Chatbot(height=520, show_label=False)
            textbox = gr.Textbox(show_label=False, max_lines=2, placeholder='Talk to Gia')
        with gr.Column(scale=1):
            side_panel = gr.Markdown('<video height="400" autoplay loop muted><source src="https://huggingface.co/spaces/tonyassi/gia-dev/resolve/main/Moods/passive2.mp4" type="video/mp4"></video>', elem_id='side-panel')
            input_image = gr.Image(sources=['webcam'], type='filepath', show_label=False)
            with gr.Row(elem_id='button-row'):
                standby_button = gr.Button(value='', icon='./standby.png', elem_id='s-button', scale=0)
                refresh_button = gr.Button(value='', icon='./refresh.png', elem_id='s-button', scale=0, link='https://tonyassi-gia-dev.hf.space/')
                settings_button = gr.Button(value='', icon='./settings.png', elem_id='s-button', scale=0)

    # Standby
    with gr.Row():
        video_standby = gr.Markdown('<video  width="864" height="550" autoplay loop muted><source src="https://huggingface.co/spaces/tonyassi/gia-dev/resolve/main/Moods/passive2.mp4" type="video/mp4"></video>', visible=False)
        chat_button = gr.Button(value='', icon='./chat.png', elem_id='s-button', scale=0, visible=False)

    # Settings
    with gr.Row():
        with gr.Column():
            slider_helpful = gr.Slider(visible=False, label='Helpful', minimum=1, maximum=10, value=2, info='How helpful at solving problems')
            slider_polite = gr.Slider(visible=False, label='Polite', minimum=1, maximum=10, value=2, info='How polite or rude')
            slider_funny = gr.Slider(visible=False, label='Funny', minimum=1, maximum=10, value=10, info='How much humor')
            slider_formal = gr.Slider(visible=False, label='Formal', minimum=1, maximum=10, value=1, info='How formal or casual her speech will be')
            slider_talkative = gr.Slider(visible=False, label='Talkative', minimum=1, maximum=10, value=7, info='How long responses will be')
            slider_random = gr.Slider(visible=False, label='Random', minimum=1, maximum=10, value=9, info='How random responses will be')
            with gr.Row():
                button_personality = gr.Button(visible=False, value='Set Personality')
                button_personality_default = gr.Button(visible=False, value='Default')
        with gr.Column():
            about = gr.Markdown("<br><br><br>", 
                                visible=False)
            chat_button_settings = gr.Button(value='', icon='./chat.png', elem_id='s-button', scale=0, visible=False)
    
    # Events
    textbox.submit(chat, inputs=[textbox,chatbox,input_image], outputs=[textbox,chatbox,input_image,side_panel], show_progress=False)
    standby_button.click(standby_mode, inputs=[], outputs=[video_standby, chat_button, chatbox, textbox, side_panel, input_image, standby_button, refresh_button, settings_button, video_standby], show_progress=False)
    settings_button.click(settings_mode, inputs= [], outputs=[chatbox, textbox, side_panel, input_image, standby_button, refresh_button, settings_button, slider_helpful, slider_polite, slider_funny, slider_formal, slider_talkative, slider_random, button_personality, button_personality_default, about, chat_button_settings], show_progress=False)
    chat_button.click(chat_mode, inputs=[], outputs=[video_standby, chat_button, chatbox, textbox, side_panel, input_image, standby_button, refresh_button, settings_button], show_progress=False)
    chat_button_settings.click(chat_mode_from_settings, inputs=[], outputs=[slider_helpful, slider_polite, slider_funny, slider_formal, slider_talkative, slider_random, button_personality, button_personality_default, about, chat_button_settings, chatbox, textbox, side_panel, input_image, standby_button, refresh_button, settings_button], show_progress=False)
    button_personality.click(change_personality, inputs=[slider_helpful,slider_polite,slider_funny,slider_formal,slider_talkative,slider_random],outputs=[], show_progress=False)
    button_personality_default.click(change_personality_default, inputs=[], outputs=[slider_helpful,slider_polite,slider_funny,slider_formal,slider_talkative,slider_random], show_progress=False)
    
demo.launch(show_api=False)

