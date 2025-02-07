from flask import Flask, Response
import pandas as pd
import spacy

app = Flask(__name__)

@app.route('/load_csv', methods=['GET'])
def load_csv():
    try:
        # Path to the CSV file
        csv_path = r'C:\\\\Users\\\\Ev\\\\Desktop\\\\TRG Week 10\\\\beer.csv'
        
        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv_path)

        # Drop unwanted columns
        columns_to_remove = [
            "index", "beer/beerId", "beer/brewerId", "beer/name",
            "user/ageInSeconds", "user/birthdayRaw", "user/birthdayUnix",
            "user/gender", "userprofileName", "review/text",
            "review/timeStruct", "review/timeUnix", "user/profileName"
        ]
        df_filtered = df.drop(columns=columns_to_remove, errors='ignore')

        # Define the allowed words for beer styles
        allowed_words = {
            "Ale", "Altbier", "Amber", "Barleywine", "Beer", "Berliner", "Bière", "Bock",
            "Braggot", "Brown", "Doppelbock", "Dunkel", "Dunkelweizen", "Eisbock", "Hefeweizen",
            "IPA", "Kölsch", "Lager", "Lambic", "Maibock", "Märzen", "Oatmeal", "Pilsener",
            "Pilsner", "Porter", "Quadrupel", "Rauchbier", "Saison", "Schwarzbier", "Scotch",
            "Stout", "Tripel", "Vienna", "Weissbier", "Weizenbock", "Wheatwine", "Witbier"
        }

        # Clean the beer/style column
        if 'beer/style' in df_filtered.columns:
            def clean_style(style):
                words = style.split()
                cleaned = [word for word in words if word in allowed_words]
                cleaned = ["Pilsner" if word == "Pilsener" else word for word in cleaned]
                return " ".join(cleaned)

            df_filtered['beer/style'] = df_filtered['beer/style'].astype(str).apply(clean_style)

        # Extract unique words from the `beer/style` column
        unique_words = set()
        if 'beer/style' in df_filtered.columns:
            for style in df_filtered['beer/style']:
                words = style.split()
                unique_words.update(words)

        # Convert unique words to a sorted list
        unique_words_list = sorted(unique_words)

        # Extract the header and first 10 rows
        df_head = df_filtered.head(10)

        # Convert the DataFrame to HTML
        html_data = df_head.to_html(index=False, escape=False)

        # Combine the HTML table and unique words list
        unique_words_html = "<ul>" + "".join(f"<li>{word}</li>" for word in unique_words_list) + "</ul>"
        full_html = html_data + "<h2>Unique Words in beer/style</h2>" + unique_words_html

        # Return the HTML as a response
        return Response(full_html, content_type='text/html')

    except FileNotFoundError:
        return "File not found. Please check the file path.", 404
    except Exception as e:
        return f"An error occurred: {e}", 500

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)
