from flask import Flask, jsonify, send_file, render_template, request, redirect, url_for, g
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from auth import auth0
# import tensorflow as tf
# import tensorflow_hub as hub
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('AUTH0_SECRET')

# Configure session for Auth0
app.config.update(
    SESSION_COOKIE_SECURE=False,  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
)

@app.before_request
def store_request_response():
    """Make request/response available for Auth0 SDK"""
    g.store_options = {"request": request}

# Load the T5 model from TensorFlow Hub (e.g., for summarization)
# model = hub.load("https://tfhub.dev/google/tf2-preview/t5-base/summarization/1")

# Generate Fake Data
players = ["Player1", "Player2", "Player3", "Player4", "Player5",
           "Player6", "Player7", "Player8", "Player9", "Player10", "Player11"]

np.random.seed(42)
data = {
    "Player": players,
    "Goals": np.random.randint(0, 10, size=len(players)),
    "Assists": np.random.randint(0, 10, size=len(players)),
    "Passes Completed": np.random.randint(20, 100, size=len(players)),
    "Tackles": np.random.randint(0, 15, size=len(players)),
    "Interceptions": np.random.randint(0, 10, size=len(players)),
}

df = pd.DataFrame(data)

# Setup web pages
@app.route('/')
async def homepage():
    """Home page - shows login button or user profile"""
    user = await auth0.get_user(g.store_options)
    return render_template('homepage.html', user=user)

@app.route('/top_scorers', methods=['GET'])
def top_scorers():
    # Get top 5 scorers
    top_five = df.nlargest(5, 'Goals')[['Player', 'Goals']].to_dict(orient='records')
    return render_template('top_scorers.html', scorers=top_five)

@app.route('/top_assists', methods=['GET'])
def top_assists():
    # Get top 5 assists
    top_five_assists = df.nlargest(5, 'Assists')[['Player', 'Assists']].to_dict(orient='records')
    return render_template('top_assists.html', assisters=top_five_assists)

@app.route('/average_passes', methods=['GET'])
def average_passes():
    total_passes = round(df['Passes Completed'].sum())  # Calculate total passes and round it
    return render_template('average_passes.html', total_passes=total_passes)

@app.route('/defensive_contributions', methods=['GET'])
def defensive_contributions():
    # Calculate total defensive contributions
    df['Defensive Contributions'] = df['Tackles'] + df['Interceptions']
    contributions = df.nlargest(5, 'Defensive Contributions')[['Player', 'Defensive Contributions']].to_dict(orient='records')
    return render_template('defensive_contributions.html', contributions=contributions)

@app.route('/plot_goals', methods=['GET'])
def plot_goals():
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Goals', y='Player', data=df, palette='viridis')
    plt.title('Goals Scored by Players')
    plt.xlabel('Goals')
    plt.ylabel('Player')

    # Save the plot to a file
    plot_filename = 'static/goals_plot.png'  # Update the path for static serving
    plt.savefig(plot_filename)
    plt.close()
    
    return render_template('goals.html', plot_filename=plot_filename)

@app.route('/generate', methods=['POST'])
def generate_text():
    user_input = request.json.get('input')
    
    # Prepare the input for the TensorFlow model
    input_text = "summarize: " + user_input
    predictions = model(tf.convert_to_tensor([input_text]))

    # Process the output
    generated_text = predictions.numpy()[0].decode('utf-8')
    return jsonify({'output': generated_text})

@app.route('/login')
async def login():
    """Redirect to Auth0 login"""
    authorization_url = await auth0.start_interactive_login({}, g.store_options)
    return redirect(authorization_url)

@app.route('/callback')
async def callback():
    """Handle Auth0 callback after login"""
    try:
        result = await auth0.complete_interactive_login(str(request.url), g.store_options)
        return redirect(url_for('index'))
    except Exception as e:
        return f"Authentication error: {str(e)}", 400

@app.route('/profile')
async def profile():
    """Protected route - shows user profile"""
    user = await auth0.get_user(g.store_options)
    
    if not user:
        return redirect(url_for('login'))
    
    return render_template('profile.html', user=user)

@app.route('/logout')
async def logout():
    """Logout and redirect to Auth0 logout"""
    logout_url = await auth0.logout(g.store_options)
    return redirect(logout_url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

