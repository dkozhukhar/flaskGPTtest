from flask import Flask, render_template, request, jsonify, session
import openai
import os

app = Flask(__name__)
app.secret_key = 'your secret key'

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
            message = {"role": "system", "content": system_message}
        else:
            message = {"role": "user", "content": user_message}
        # If there is no conversation history in the session, create a new list
        if 'history' not in session:
            session['history'] = []
        # Append the new message to the conversation history
        session['history'].append(message)
        response = openai.ChatCompletion.create(
            model=model_name,
            messages=session['history']
        )
        # Append the assistant's message to the conversation history
        session['history'].append({"role": "assistant", "content": response['choices'][0]['message']['content']})
        return jsonify({
            'message': response['choices'][0]['message']['content'],
            'usage': response['usage']
        })
    # Clear the conversation history when loading the page
    session.pop('history', None)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
