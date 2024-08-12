# Gia

![gia-360-sam-5 3](https://github.com/user-attachments/assets/e6e5de3c-6ebf-4e29-b449-e6a9eeb4786c)

by [Tony Assi](https://www.tonyassi.com/)

Gia is an AI handbag with expressive emotion powered by [Google Gemini API](https://ai.google.dev/gemini-api), designed to bring artificial intelligence out of the cloud and into everyday life.

Web demo: [![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)]([https://huggingface.co/spaces/tonyassi/fashion-try-on](https://huggingface.co/spaces/tonyassi/gia))

Project website: [tonyassi.com/gia](https://www.tonyassi.com/gia)

## Download Files
Download ZIP or use the following command
```bash
git clone https://github.com/TonyAssi/gia.git
```

## Installation
Install required libraries
```bash
pip install -r requirements.txt
```

## Gemini API Key
First you'll need a Gemini API key, [get one here](https://aistudio.google.com/app/u/1/apikey).

Open the [app.py](https://github.com/TonyAssi/gia/blob/e02901c6689ab80d7851cb0587c6efa601b97ed7/app.py#L9) file and input your key
```python
genai.configure(api_key="YOUR_GEMINI_API_KEY")
```

## Usage
Please note the app is designed for Desktop and works best with Chrome.

Launch Gradio app
```bash
python app.py
```

It'll print out the local and public URLs running the app. It should looking something like this
```
Running on local URL:  http://127.0.0.1:7860
Running on public URL: https://ded9ba42c916bded4f.gradio.live
```
