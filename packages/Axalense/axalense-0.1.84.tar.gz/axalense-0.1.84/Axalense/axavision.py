import base64
import io
from groq import Groq
import requests
from PIL import Image


def encode_image(image):
    image = Image.open(image)
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')
def analyze_image(image, prompt, api_key, is_url=False):
    # image = Image.open(image)
    client = Groq(api_key=api_key)

    if is_url:
        image_content = {"type": "image_url", "image_url": {"url": image}}
    else:
        base64_image = encode_image(image)
        image_content = {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        image_content,
                    ],
                }
            ],
            model="meta-llama/llama-4-scout-17b-16e-instruct",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"
