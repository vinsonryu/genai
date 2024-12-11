from flask import Flask, request, jsonify, render_template
import openai
from flask_cors import CORS

app = Flask(__name__)

CORS(app)
# Set OpenAI API Key
client = openai.OpenAI(
    api_key = "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", 
)

# Dynamic prompt generation based on request type
def generate_prompt(request_type, user_input):
    prompts = {
        "Blog": (
            f"Write a detailed, SEO-optimized, and engaging blog post about '{user_input}'. "
            "The blog should have the following structure: Introduction, Main Content with proper subheadings, "
            "and a conclusion. Write in a professional yet conversational tone."
        ),
        "Tweet": (
            f"Create a concise, engaging tweet about '{user_input}'. "
            "Include relevant hashtags and keep it under 280 characters."
        ),
        "Instagram": (
            f"Create a concept for an Instagram infographic based on the topic '{user_input}'. "
            "The content should be visually appealing and focused on storytelling with key insights."
        ),
        "Infographic": (
            f"Generate text content suitable for an infographic about '{user_input}'. "
            "Focus on key points, steps, and actionable insights."
        ),
        "Project Plan": (
            f"Create a detailed software project plan for '{user_input}'. Write a clean and efficient Python code snippet demonstrating how to solve the problem"
            "Include phases, tools, time estimates, cost breakdowns, and implementation steps."
        ),
 
    }
    return prompts.get(request_type, f"Write a comprehensive explanation about: '{user_input}'.")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        user_input = request.form.get("user_input", "General Query")
        request_type = request.form.get("request_type", "General Info")
        
        # Generate prompt
        prompt = generate_prompt(request_type, user_input)

        # # Call OpenAI API

        
            # Handle text content generation (non-code)
        response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert content writer and python coder"},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=2000,
            )
        
        generated_content = response.choices[0].message.content
        # print(generated_content)
        
        # If image is part of request type, generate image URL
        image_url = None
        if request_type in ["Blog", "Instagram", "Infographic", "tweet"]:
            prompt = generate_prompt("image", user_input)
            model = "dall-e-3"
            image_response = openai.images.generate(prompt=prompt, model=model)
            print(image_response)
            image_url = image_response.data[0].url
        print(image_url)
        # Render the frontend with both content and image if applicable
        return render_template(
            'index.html',
            output=generated_content,
            user_input=user_input,
            request_type=request_type,
            image_url=image_url
        )
    except Exception as e:
        print(e)
        return render_template('index.html', error=str(e))


if __name__ == "__main__":
    app.run(debug=True)

