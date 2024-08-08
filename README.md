# Gia
by [Tony Assi](https://www.tonyassi.com/)

Gia is an AI handbag with expressive emotion powered by [Google Gemini API](https://ai.google.dev/gemini-api), designed to bring artificial intelligence out of the cloud and into everyday life.

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
Launch Gradio app
```bash
python app.py
```
