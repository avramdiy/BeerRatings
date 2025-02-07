from flask import Flask, Response
import pandas as pd

app = Flask(__name__)

@app.route('/load_csv', methods=['GET'])
def load_csv():
    try:
        # Path to the CSV file
        csv_path = r'C:\\Users\\Ev\\Desktop\\TRG Week 10\\beer.csv'
        
        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv_path)

        # Convert the DataFrame to HTML
        html_data = df.to_html(index=False, escape=False)

        # Return the HTML as a response
        return Response(html_data, content_type='text/html')

    except FileNotFoundError:
        return "File not found. Please check the file path.", 404
    except Exception as e:
        return f"An error occurred: {e}", 500

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)
