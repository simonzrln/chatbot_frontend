# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Flask modules
from flask import render_template, request, jsonify

# App modules
from apps import app
import openai

# Set your OpenAI API key
openai.api_key = "xxxx-xxxx-xxxx"

# App main route + generic routing
@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path>')
def index(path):
    try:
        return render_template('home/' + path)
    except Exception as e:
        return render_template('home/page-404.html'), 404

def get_segment(request):
    segment = request.path.split('/')[-1] or 'index'
    return segment

# GPT-3.5 Turbo Chat route
@app.route('/chatbot', methods=['POST'])
def chatgpt():
    try:
        # Extract the message from the form
        message = request.json['prompt']

        # Generate a response using OpenAI's GPT-3.5 Turbo
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0.7,
            messages=[
                {"role": "system", "content": "You are a chatbot designed to assist with inquiries."},
                {"role": "user", "content": message}
            ]
        )

        generated_text = completion.choices[0].message['content']
        return jsonify({'result': generated_text})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Additional configurations or utility functions can be added below
