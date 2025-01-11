from flask import Flask, render_template, request, redirect, url_for, session
import random
import json


# create an object named app which uses Flask
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load words
with open('words.json') as f:
    words = json.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game')
def game():
    # Pick a random word
    correct_word = random.choice(words)
    correct_meaning = correct_word['meaning']

    # Generate three random incorrect options
    other_meanings = random.sample([w['meaning'] for w in words if w['meaning'] != correct_meaning], 3)

    # Combine correct and incorrect options, then shuffle
    options = [correct_meaning] + other_meanings
    random.shuffle(options)

    session['current_word'] = correct_word
    session['correct_meaning'] = correct_meaning
    session['options'] = options  # Store options in the session

    return render_template('game.html', word=correct_word['word'], options=options)

@app.route('/check', methods=['POST'])
def check():
    user_answer = request.form['answer']
    correct_answer = session.get('correct_meaning')
    options = session.get('options')  # Retrieve options from the session

    # Update score if the user selects the correct answer
    session['score'] = session.get('score', 0) + (1 if user_answer == correct_answer else 0)

    session['attempts'] = session.get('attempts', 0) + 1
    feedback = {
        'user_answer': user_answer,
        'correct_answer': correct_answer,
        'is_correct': user_answer == correct_answer,
    }

    if session['attempts'] >= 10:  # Limit to 10 attempts
        return redirect(url_for('result'))

    return render_template('game.html', 
                           word=session['current_word']['word'], 
                           options=options, 
                           correct_meaning=correct_answer, 
                           feedback=feedback)


@app.route('/result')
def result():
    score = session.get('score', 0)
    session.clear()
    return render_template('result.html', score=score)

if __name__ == '__main__':
    app.run(debug=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
