Social-media-content-analyzer
---

**Social Media Content Analyzer** is an intuitive web application that allows users to analyze their social media posts. The tool provides actionable insights and suggestions to enhance engagement by evaluating sentiment, readability, and overall effectiveness of the content. It supports various file formats, including images, PDFs, and text files, using OCR and advanced text analysis techniques.

---

## **Features**
- **OCR (Optical Character Recognition):** Extract text from images and PDFs.
- **Sentiment Analysis:** Identify positive, neutral, or negative tones in the text.
- **Readability Check:** Evaluate content structure and provide readability suggestions.
- **Hashtag Recommendations:** Suggest hashtags for better reach.
- **Grammar and Spelling Checks:** Offer corrections to improve quality.
- **Emoji Usage Suggestions:** Enhance posts with creative emojis for better user engagement.
- **Word Complexity Analysis:** Simplify vocabulary to cater to a wider audience.

---

## **Tech Stack**
- **Backend:** Flask, Python
- **Frontend:** HTML, CSS, JavaScript, Dropzone.js
- **Libraries & Tools:** pytesseract, spaCy, TextBlob, NLTK, VADER Sentiment Analysis, pdf2image, PIL

---

## **Setup Instructions**
1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/social-media-content-analyzer.git
   cd social-media-content-analyzer
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Flask server:**
   ```bash
   python app.py
   ```

4. **Access the application:**
   Open `http://127.0.0.1:5000` in your web browser.

5. **Upload a file:**
   Drag and drop an image, PDF, or text file to analyze its content.

---

## **How It Works**

### **File Upload**
- Users can upload files through a user-friendly drag-and-drop interface powered by Dropzone.js.
- The app accepts `.jpg`, `.jpeg`, `.png`, `.pdf`, and `.txt` files.

### **OCR Processing**
- **Image/PDF Files:** Text is extracted using `pytesseract`. PDF files are converted into images using `pdf2image`.
- **Text Files:** The content is read directly.

### **Content Analysis**
1. **Sentiment Analysis:**
   - The app evaluates the overall tone of the content using VADER Sentiment Analyzer and provides suggestions for improvement.
   
2. **Readability:**
   - It calculates average sentence length and offers insights to make the text more digestible.

3. **Grammar and Spelling:**
   - The TextBlob library checks for errors and provides corrections.

4. **Hashtag Recommendations:**
   - Based on the text content, relevant hashtags are suggested to boost visibility.

5. **Word Complexity:**
   - Identifies complex words and suggests simpler alternatives.

6. **Emoji Usage:**
   - Analyzes text for emojis and recommends adding them to make posts more engaging.

### **Dynamic Frontend**
- Suggestions and results are displayed with interactive animations.
- Real-time updates ensure seamless user experience.

---

## **Future Enhancements**
- Multilingual text analysis.
- AI-generated content suggestions.
- Integration with social media platforms for direct posting.

---
