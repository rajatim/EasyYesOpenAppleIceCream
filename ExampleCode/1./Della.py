import requests
import json
from PIL import Image
from io import BytesIO
import base64

# Replace 'your_api_key' with your actual API key
api_key = ''

# Set up headers for the API request
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json',
}

# Define the prompt you want to generate images for
# prompt = 'A futuristic city skyline'
prompt = 'a white siamese cat'

# Set up the API request data
data = json.dumps({
    'model': 'image-alpha-001',
    # 'model': 'text-davinci-003',
    'prompt': prompt,
    'num_images': 1,
    # 'size': '256x256',
    'size': '1024x1024',

})

# Send the API request
response = requests.post('https://api.openai.com/v1/images/generations', headers=headers, data=data)

# Check if the request was successful
if response.status_code == 200:
    # Parse the response
    response_json = response.json()

    # Get the generated image URL
    image_url = response_json['data'][0]['url']

    # Download the image
    image_response = requests.get(image_url)

    # Display the image
    if image_response.status_code == 200:
        image = Image.open(BytesIO(image_response.content))
        image.show()
    else:
        print(f'Error downloading image: {image_response.status_code}, {image_response.text}')
else:
    print(f'Error: {response.status_code}, {response.text}')
