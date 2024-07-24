import base64
import os

def encode_image(image_path):
    """Encode image to base64."""
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            return f"data:image/jpeg;base64,{encoded_string}"
    except FileNotFoundError:
        print(f"File not found: {image_path}")
        return ""
    
# Chemins des images
base_dir = os.path.dirname(__file__)
bot_image_path = os.path.join(base_dir, "static", "bot.jpeg")
user_image_path = os.path.join(base_dir, "static", "user.jpeg")

# Encoder les images
bot_image_base64 = encode_image(bot_image_path)
user_image_base64 = encode_image(user_image_path)

css = '''
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #2b313e
}
.chat-message.bot {
    background-color: #475063
}
.chat-message .avatar {
  width: 20%;
}
.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #fff;
}
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="{bot_image_base64}">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="{user_image_base64}">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''