from flask import Flask, jsonify, send_file, render_template
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

app = Flask(__name__)

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

@app.route('/')
def homepage():
    return render_template('homepage.html')

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

# @app.route('/top_scorers', methods=['GET'])
# def top_scorers():
#     return jsonify(df.nlargest(5, 'Goals')[['Player', 'Goals']].to_dict(orient='records'))

# @app.route('/top_assists', methods=['GET'])
# def top_assists():
#     return jsonify(df.nlargest(5, 'Assists')[['Player', 'Assists']].to_dict(orient='records'))

# @app.route('/average_passes', methods=['GET'])
# def average_passes():
#     return jsonify({'average_passes': df['Passes Completed'].mean()})

# @app.route('/defensive_contributions', methods=['GET'])
# def defensive_contributions():
#     df['Defensive Contributions'] = df['Tackles'] + df['Interceptions']
#     return jsonify(df.nlargest(5, 'Defensive Contributions')[['Player', 'Defensive Contributions']].to_dict(orient='records'))

# @app.route('/plot_goals', methods=['GET'])
# def plot_goals():
#     plt.figure(figsize=(10, 6))
#     sns.barplot(x='Goals', y='Player', data=df, palette='viridis')
#     plt.title('Goals Scored by Players')
#     plt.xlabel('Goals')
#     plt.ylabel('Player')
#     plot_filename = 'goals_plot.png'
#     plt.savefig(plot_filename)
#     plt.close()
#     return send_file(plot_filename, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

