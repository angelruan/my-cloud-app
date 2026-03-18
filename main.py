from flask import Flask, request
import psycopg2

app = Flask(__name__)

# This is the HTML for our simple web page
HTML_FORM = """
<html>
    <body>
        <h2>Welcome to the Data Collector!</h2>
        <form method="POST" action="/submit">
            <label>Enter a value:</label>
            <input type="text" name="user_value" required>
            <input type="submit" value="Save to Cloud SQL">
        </form>
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
    DB_HOST = "YOUR_DATABASE_IP" 
    DB_USER = "postgres"
    DB_PASS = "YOUR_DATABASE_PASSWORD"
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