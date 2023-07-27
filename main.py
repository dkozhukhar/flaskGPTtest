from flask import Flask, render_template, request, jsonify
import openai
import os

app = Flask(__name__)

try:
    openai.api_key = os.environ['OPENAI_API_KEY']
except KeyError:
    print("You need to set your OPENAI_API_KEY environment variable.")
    exit(1)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        model_name = request.form['model']
        role = request.form['role']
        system_message = request.form['system']
        user_message = request.form['message']
        if role == 'system':
            messages = [
                {"role": "system", "content": system_message}
            ]
        else:
            messages = [
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ]
        response = openai.ChatCompletion.create(
            model=model_name,
            messages=messages
        )
        return jsonify({
            'message': response['choices'][0]['message']['content'],
            'usage': response['usage']
        })
    return render_template('index.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
