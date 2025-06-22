from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load your main product data (styles.csv)
data = pd.read_csv("styles.csv.zip", on_bad_lines='skip')

# Load image data (images.csv)
df = pd.read_csv("images.csv.zip", on_bad_lines='skip')

# Extract numeric ID from 'filename' to allow merging
df['id'] = df['filename'].str.replace('.jpg', '').astype(int)


# Load your dataset
merged_df = pd.merge(data, df[['id', 'link']], on='id', how='left')

# Clean the 'Name' column (remove leading/trailing spaces)
merged_df['articleType'] = merged_df['articleType'].astype(str).str.strip()

# Recommendation function based on name match
def product_rec(produc_name):
    produc_name = produc_name.strip().lower()
    matches = merged_df[merged_df['articleType'].str.lower().str.contains(produc_name)]

    if matches.empty:
        return []

    result = matches[['articleType', 'subCategory', 'productDisplayName', 'baseColour', 'link', 'gender']].head(10)
    return result.to_dict(orient='records')


# Flask route
@app.route('/', methods=['GET', 'POST'])
def home():
    recommendations = []

    if request.method == 'POST':
        name = request.form.get('produc_name', '').strip()
        if name:
            recommendations = product_rec(name)

    return render_template("index.html", recommendations=recommendations)


# Run the app
if __name__ == '__main__':
    app.run(debug=True)