# app.py
# Import necessary libraries
from flask import Flask, request, jsonify
from flask_cors import CORS
from googletrans import Translator
from PyDictionary import PyDictionary
from deep_translator import GoogleTranslator

# Initialize the Flask application
app = Flask(__name__)
# Enable Cross-Origin Resource Sharing (CORS) to allow the extension to communicate with this server
CORS(app)

# Initialize the translator and dictionary objects
translator = Translator()
dictionary = PyDictionary()

# Define the main endpoint for translation
@app.route('/translate', methods=['POST'])
def translate_word():
    """
    This function is called when the Chrome extension sends a word.
    It translates the word, finds its meaning, and creates related links.
    """
    try:
        # Get the word from the JSON data sent by the extension
        data = request.get_json()
        word_to_translate = data.get('word')

        if not word_to_translate:
            return jsonify({'error': 'No word provided'}), 400

        # --- 1. Translation ---
        # Translate the word from English ('en') to Hindi ('hi')
        hindi_word = GoogleTranslator(source='en', target='hi').translate(word_to_translate)

        # --- 2. Uses/Meanings ---
        # Get the meanings (definitions) of the word
        meanings = dictionary.meaning(word_to_translate)
        # We'll format the meanings for display
        usage_info = ""
        if meanings:
            # Loop through parts of speech (Noun, Verb, etc.)
            for part_of_speech, definitions in meanings.items():
                usage_info += f"<h4>{part_of_speech}</h4>"
                # List the first few definitions
                for i, definition in enumerate(definitions[:3]):
                    usage_info += f"<p>- {definition}</p>"
        else:
            usage_info = "<p>No definition found.</p>"

        # --- 3. Related Links ---
        # Generate links to Google Search and an online dictionary
        google_link = f"https://www.google.com/search?q=define+{word_to_translate}"
        dictionary_link = f"https://www.merriam-webster.com/dictionary/{word_to_translate}"

        # --- 4. Send Response ---
        # Package all the information into a JSON response to send back to the extension
        response_data = {
            'hindi_translation': hindi_word,
            'usage': usage_info,
            'google_link': google_link,
            'dictionary_link': dictionary_link
        }
        return jsonify(response_data)

    except Exception as e:
        # Handle any errors that occur during the process
        print(f"An error occurred: {e}")
        return jsonify({'error': 'Failed to process the word.'}), 500

# This allows you to run the app directly using "python app.py"
if __name__ == '__main__':
    # Runs the app on localhost at port 5000
    app.run(debug=True, port=5000)
