import os
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import pytesseract
from PIL import Image
from pdf2image import convert_from_path  # Ensure this import is present
import spacy
from textblob import TextBlob
import random
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import json
import re
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

# Download the necessary NLTK data
nltk.download('punkt_tab')

# Initialize the stemmer
stemmer = PorterStemmer()


# Initialize the VADER SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()

# Initialize the Flask app
app = Flask(__name__)

# Set the upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf', 'txt'}

# Initialize spaCy for text analysis
nlp = spacy.load("en_core_web_sm")

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route to render the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle file upload and OCR
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        # Process the file based on type (OCR for images, PDF, etc.)
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            # OCR processing for image files
            ocr_text = pytesseract.image_to_string(Image.open(file_path))

        elif filename.lower().endswith('.pdf'):
            # PDF processing: Convert PDF to images and then apply OCR
            images = convert_from_path(file_path, 300)  # 300 DPI for good quality

            # Extract text from each page
            ocr_text = ""
            for page_num, image in enumerate(images):
                text = pytesseract.image_to_string(image)
                ocr_text += f"--- Page {page_num + 1} ---\n"
                ocr_text += text + "\n\n"

        elif filename.lower().endswith('.txt'):
            # If it's a text file, simply read it
            with open(file_path, 'r') as f:
                ocr_text = f.read()

        # Analyze the text using spaCy (you can add other analyses like sentiment, readability, etc.)
        doc = nlp(ocr_text)
        analysis_result = analyze_text(ocr_text)

        return jsonify({
            'ocr_text': ocr_text,
            'suggestions': analysis_result
        })

    return jsonify({'error': 'Invalid file type'})

# Function to analyze text
def analyze_text(text):
    suggestions = []

    # 1. Sentence Length Analysis (Social Media Engagement)
    sentence_length = len(text.split())
    if sentence_length > 100:
        suggestions.append("🌟 Consider shortening the content. Social media users engage more with concise, to-the-point posts. Short sentences often increase readability and engagement! 💬\n\n")

    # 2. Sentiment Analysis (Positive/Negative/Neutral Sentiment)
    sentiment_scores = analyzer.polarity_scores(text)
    compound_score = sentiment_scores['compound']  # The compound score is the overall sentiment score

    # Now, use the compound score for suggestions
    if compound_score <= -0.5:
        suggestions.append("🚨 The sentiment seems negative. Consider rephrasing to sound more positive or neutral. A positive tone is key for building brand loyalty and engaging followers! 😊✨\n\n")
    elif compound_score >= 0.5:
        suggestions.append("💡 The sentiment is very positive! Keep it up! Positive content is often more shareable and can boost engagement significantly. 🎉🔥\n\n")
    else:
        suggestions.append("🤔 The sentiment seems neutral. Adding a bit more emotional appeal or a clear opinion can increase engagement. Try asking a question or sharing an opinion. 📣\n\n")
    
    
    # 3. Readability Analysis (Average Sentence Length & Simplicity)
    doc = nlp(text)
    sentence_count = len([sent for sent in doc.sents])
    average_sentence_length = sentence_length / sentence_count if sentence_count > 0 else 0

    if average_sentence_length > 20:
        suggestions.append("📝 Your sentences might be a bit long. Social media users prefer content that's easy to digest. Break down long sentences and keep things crisp and clear! 🔍\n\n")

    # 4. Grammar and Spelling Check 
    blob = TextBlob(text)
    corrected_text = blob.correct()
    if str(corrected_text) != text:
        suggestions.append(f"⚠️ Correction: \n We found some grammar/spelling mistakes. Here's a corrected version:\n\n{str(corrected_text)}🖋️✅\n\n")

    # 5. Hashtags Recommendation (Improve Reach)
    hashtags = get_relevant_hashtags(text)
    if hashtags:
        suggestions.append(f"📈 Hashtags Tip: Use these relevant hashtags to increase your content's reach: \n{', '.join(hashtags)}. 📊\n\n")


    # 6. Word Complexity (Simplifying Vocabulary)
    # complex_words = [token.text for token in doc if len(token.text) > 10]

    # if complex_words:
    #     suggestions.append(f"🧐 Some words are quite complex. Simplify them to make the content accessible to a broader audience. For example, consider replacing words like {', '.join(complex_words)} with simpler alternatives. 🧠\n\n")


    # 6. Word Complexity (Simplifying Vocabulary)
    # Tokenize the text into words
    words = word_tokenize(text)

    # Find complex words based on stemming
    complex_words = [stemmer.stem(word) for word in words if len(stemmer.stem(word)) > 10 and word.isalpha()]

    if complex_words:
        suggestions.append(f"🧐 Some words are quite complex. Simplify them to make the content accessible to a broader audience. For example, consider replacing words like {', '.join(complex_words)} with simpler alternatives. 🧠\n\n")


    # 7. Emoji Usage (Add personality to posts)
    if not contains_emoji(text):
        suggestions.append("🎉 Fun Tip: Using emojis or exclamation marks can make your posts feel more lively and relatable. Don't overdo it, but a well-placed emoji can boost engagement! 😎👍")

    # Returning all the suggestions in a formatted way
    if not suggestions:
        suggestions.append("✨ Your content is well-crafted and ready for social media. Keep up the great work! 🚀")

    #return "\n\n".join(suggestions)
    return "\n".join(suggestions)

def get_relevant_hashtags(text):
    """Get relevant hashtags based on the content of the text."""
    
    # Corrected the file path using raw string
    with open(r'static/hashtags.json', 'r') as file:
        sample_hashtags = json.load(file)

    # Convert the text to lowercase
    text_lower = text.lower()

    # Dictionary to store match counts for each category
    match_counts = {}

    # Iterate over categories and check for any keyword matches from the hashtags
    for category, hashtags in sample_hashtags.items():
        # Count the number of matches in each category
        match_count = 0
        for hashtag in hashtags:
            if hashtag[1:].lower() in text_lower:  # Remove '#' and match the word
                match_count += 1
        
        # Store the match count for the category
        match_counts[category] = match_count

    # Find the category with the highest number of matches
    max_category = max(match_counts, key=match_counts.get, default=None)

    # If no relevant matches were found, return default hashtags
    if max_category is None or match_counts[max_category] == 0:
        return ['#socialmedia', '#content', '#engagement', '#marketing']

    # Return the hashtags associated with the category with the most matches
    return sample_hashtags.get(max_category, ['#socialmedia', '#content', '#engagement', '#marketing'])


def contains_emoji(text):
    # Emoji regex pattern
    emoji_pattern = re.compile(
        "[\U0001F600-\U0001F64F"
        "\U0001F300-\U0001F5FF"
        "\U0001F680-\U0001F6FF"
        "\U0001F700-\U0001F77F"
        "\U0001F780-\U0001F7FF"
        "\U0001F800-\U0001F8FF"
        "\U0001F900-\U0001F9FF"
        "\U0001FA00-\U0001FA6F"
        "\U0001FA70-\U0001FAFF"
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251]+", flags=re.UNICODE)

    # Check if there's a match for emojis
    return bool(emoji_pattern.search(text))



if __name__ == '__main__':
    app.run(debug=True)
