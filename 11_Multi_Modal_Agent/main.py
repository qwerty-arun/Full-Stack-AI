from google import genai
from PIL import Image

# Initialize client
client = genai.Client(
    api_key=''
)

image = Image.open("D:/Kali_SF/Demo.png")

# Call the multimodal Gemini model
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[image, "Describe the contents of this image"],
)

# Print text output only
print(response.text)
