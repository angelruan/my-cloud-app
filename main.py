from flask import Flask, request
import psycopg2

app = Flask(__name__)

# This is the HTML for our simple web page
HTML_FORM = """
<html>
    <head>
        <title>Catpedia</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7f6; display: flex; justify-content: center; padding-top: 50px; }
            .card { background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); max-width: 500px; text-align: center; }
            img { width: 100%; border-radius: 10px; margin: 15px 0; }
            h1 { color: #2c3e50; margin-bottom: 5px; }
            p { color: #7f8c8d; margin-bottom: 20px; }
            input[type="text"] { width: 80%; padding: 10px; border: 2px solid #ddd; border-radius: 5px; margin-bottom: 10px; }
            input[type="submit"] { background-color: #ff6b6b; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-weight: bold; transition: 0.3s; }
            input[type="submit"]:hover { background-color: #ee5253; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Catpedia</h1>
            <p>Ask any question about cats!</p>
            
            <img src="https://i.ytimg.com/vi/SQJrYw1QvSQ/maxresdefault.jpg" alt="Cute Cat">

            <form method="POST" action="/submit">
                <input type="text" name="user_value" placeholder="Type your question here..." required>
                <br>
                <input type="submit" value="Meow-it!">
            </form>
        </div>
    </body>
</html>
"""

@app.route('/')
def home():
    # Show the web page when someone visits the main URL
    return HTML_FORM

@app.route('/submit', methods=['POST'])
def submit():
    # Grab the value the user typed into the form
    user_value = request.form['user_value']

    # --- DATABASE CONNECTION SETTINGS ---
    # We will replace these placeholder words in the next step!
    DB_HOST = "34.28.139.87" 
    DB_USER = "postgres"
    DB_PASS = "RAQuanni2015."
    DB_NAME = "postgres"

    try:
        # 1. Open the connection to the filing cabinet
        conn = psycopg2.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, dbname=DB_NAME)
        cursor = conn.cursor()

        # 2. Run the SQL query to insert the data safely
        cursor.execute("INSERT INTO user_answers (answer) VALUES (%s)", (user_value,))
        conn.commit()

        # 3. Close the drawer
        cursor.close()
        conn.close()
        
        return f"Success! Saved '{user_value}' to the database! <br><br> <a href='/'>Go back</a>"
    
    except Exception as e:
        return f"Oh no, an error occurred: {e}"

if __name__ == '__main__':
    # Run on 0.0.0.0 so the firewall can let the outside world in
    app.run(host='0.0.0.0', port=8080)