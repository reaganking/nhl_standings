from flask import Flask, render_template
import os

app = Flask(__name__)

# Define a route to display the images
@app.route('/')
def display_images():
    # Get the list of GIF files in the 'static/gifs' folder
    gif_files = [f for f in os.listdir('static/gifs') if f.endswith('.gif')]
    
    # Render the HTML template and pass the list of GIF files to it
    return render_template('index.html', gif_files=gif_files)

if __name__ == '__main__':
    app.run(debug=True)
