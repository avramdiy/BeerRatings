from flask import Flask, Response
import pandas as pd
import spacy
import re
import matplotlib.pyplot as plt
import io
import base64

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
    
@app.route('/average_review_chart', methods=['GET'])
def average_review_chart():
    try:
        # Path to the CSV file
        csv_path = r'C:\\Users\\Ev\\Desktop\\TRG Week 10\\beer.csv'

        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv_path)

        # Clean the beer/style column
        allowed_words = {
            "Ale", "Altbier", "Amber", "Barleywine", "Beer", "Berliner", "Bière", "Bock",
            "Braggot", "Brown", "Doppelbock", "Dunkel", "Dunkelweizen", "Eisbock", "Hefeweizen",
            "IPA", "Kölsch", "Lager", "Lambic", "Maibock", "Märzen", "Oatmeal", "Pilsener",
            "Pilsner", "Porter", "Quadrupel", "Rauchbier", "Saison", "Schwarzbier", "Scotch",
            "Stout", "Tripel", "Vienna", "Weissbier", "Weizenbock", "Wheatwine", "Witbier"
        }

        if 'beer/style' in df.columns:
            def clean_style(style):
                words = style.split()
                cleaned = [word for word in words if word in allowed_words]
                # Replace 'Pilsener' with 'Pilsner'
                cleaned = ["Pilsner" if word == "Pilsener" else word for word in cleaned]
                return " ".join(cleaned)

            df['beer/style'] = df['beer/style'].astype(str).apply(clean_style)

        # Calculate average review/overall per beer/style
        if 'beer/style' in df.columns and 'review/overall' in df.columns:
            df['review/overall'] = pd.to_numeric(df['review/overall'], errors='coerce')
            avg_reviews = df.groupby('beer/style')['review/overall'].mean().dropna()

            # Create the bar chart
            plt.figure(figsize=(10, 6))
            avg_reviews.sort_values(ascending=False).plot(kind='bar', color='skyblue')
            plt.title('Average Review/Overall per Beer Style')
            plt.xlabel('Beer Style')
            plt.ylabel('Average Review')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()

            # Save the plot to a BytesIO object
            img = io.BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)

            # Encode the image to base64 to embed in HTML
            plot_url = base64.b64encode(img.getvalue()).decode()
            plt.close()

            # Return the image as HTML
            return f'<img src="data:image/png;base64,{plot_url}" />'

        else:
            return "Required columns are missing in the dataset.", 400

    except FileNotFoundError:
        return "File not found. Please check the file path.", 404
    except Exception as e:
        return f"An error occurred: {e}", 500

@app.route('/average_aroma_chart', methods=['GET'])
def average_aroma_chart():
    try:
        # Path to the CSV file
        csv_path = r'C:\\Users\\Ev\\Desktop\\TRG Week 10\\beer.csv'

        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv_path)

        # Clean the beer/style column
        allowed_words = {
            "Ale", "Altbier", "Amber", "Barleywine", "Beer", "Berliner", "Bière", "Bock",
            "Braggot", "Brown", "Doppelbock", "Dunkel", "Dunkelweizen", "Eisbock", "Hefeweizen",
            "IPA", "Kölsch", "Lager", "Lambic", "Maibock", "Märzen", "Oatmeal", "Pilsener",
            "Pilsner", "Porter", "Quadrupel", "Rauchbier", "Saison", "Schwarzbier", "Scotch",
            "Stout", "Tripel", "Vienna", "Weissbier", "Weizenbock", "Wheatwine", "Witbier"
        }

        if 'beer/style' in df.columns:
            def clean_style(style):
                words = style.split()
                cleaned = [word for word in words if word in allowed_words]
                # Replace 'Pilsener' with 'Pilsner'
                cleaned = ["Pilsner" if word == "Pilsener" else word for word in cleaned]
                return " ".join(cleaned)

            df['beer/style'] = df['beer/style'].astype(str).apply(clean_style)

        # Calculate average review/overall per beer/style
        if 'beer/style' in df.columns and 'review/aroma' in df.columns:
            df['review/aroma'] = pd.to_numeric(df['review/aroma'], errors='coerce')
            avg_reviews = df.groupby('beer/style')['review/aroma'].mean().dropna()

            # Create the bar chart
            plt.figure(figsize=(10, 6))
            avg_reviews.sort_values(ascending=False).plot(kind='bar', color='skyblue')
            plt.title('Average Review/Aroma per Beer Style')
            plt.xlabel('Beer Style')
            plt.ylabel('Average Aroma Review')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()

            # Save the plot to a BytesIO object
            img = io.BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)

            # Encode the image to base64 to embed in HTML
            plot_url = base64.b64encode(img.getvalue()).decode()
            plt.close()

            # Return the image as HTML
            return f'<img src="data:image/png;base64,{plot_url}" />'

        else:
            return "Required columns are missing in the dataset.", 400

    except FileNotFoundError:
        return "File not found. Please check the file path.", 404
    except Exception as e:
        return f"An error occurred: {e}", 500

@app.route('/average_abv_chart', methods=['GET'])
def average_abv_chart():
    try:
        # Path to the CSV file
        csv_path = r'C:\\Users\\Ev\\Desktop\\TRG Week 10\\beer.csv'

        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv_path)

        # Clean the beer/style column
        allowed_words = {
            "Ale", "Altbier", "Amber", "Barleywine", "Beer", "Berliner", "Bière", "Bock",
            "Braggot", "Brown", "Doppelbock", "Dunkel", "Dunkelweizen", "Eisbock", "Hefeweizen",
            "IPA", "Kölsch", "Lager", "Lambic", "Maibock", "Märzen", "Oatmeal", "Pilsener",
            "Pilsner", "Porter", "Quadrupel", "Rauchbier", "Saison", "Schwarzbier", "Scotch",
            "Stout", "Tripel", "Vienna", "Weissbier", "Weizenbock", "Wheatwine", "Witbier"
        }

        if 'beer/style' in df.columns:
            def clean_style(style):
                words = style.split()
                cleaned = [word for word in words if word in allowed_words]
                # Replace 'Pilsener' with 'Pilsner'
                cleaned = ["Pilsner" if word == "Pilsener" else word for word in cleaned]
                return " ".join(cleaned)

            df['beer/style'] = df['beer/style'].astype(str).apply(clean_style)

        # Calculate average beer/abv per beer/style
        if 'beer/style' in df.columns and 'beer/ABV' in df.columns:
            df['beer/ABV'] = pd.to_numeric(df['beer/ABV'], errors='coerce')
            avg_reviews = df.groupby('beer/style')['beer/ABV'].mean().dropna()

            # Create the bar chart
            plt.figure(figsize=(10, 6))
            avg_reviews.sort_values(ascending=False).plot(kind='bar', color='skyblue')
            plt.title('Average ABV per Beer Style')
            plt.xlabel('Beer Style')
            plt.ylabel('ABV')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()

            # Save the plot to a BytesIO object
            img = io.BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)

            # Encode the image to base64 to embed in HTML
            plot_url = base64.b64encode(img.getvalue()).decode()
            plt.close()

            # Return the image as HTML
            return f'<img src="data:image/png;base64,{plot_url}" />'

        else:
            return "Required columns are missing in the dataset.", 400

    except FileNotFoundError:
        return "File not found. Please check the file path.", 404
    except Exception as e:
        return f"An error occurred: {e}", 500

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)
