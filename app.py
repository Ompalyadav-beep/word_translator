from flask import Flask, request, jsonify
from flask_cors import CORS
from googletrans import Translator
from PyDictionary import PyDictionary
from deep_translator import GoogleTranslator
app = Flask(__name__)

CORS(app)
translator = Translator()
dictionary = PyDictionary()
@app.route('/translate', methods=['POST'])
def translate_word():
    """
    This function is called when the Chrome extension sends a word.
    It translates the word, finds its meaning, and creates related links.
    """
    try:
        
        data = request.get_json()
        word_to_translate = data.get('word')

        if not word_to_translate:
            return jsonify({'error': 'No word provided'}), 400
        hindi_word = GoogleTranslator(source='en', target='hi').translate(word_to_translate)
        meanings = dictionary.meaning(word_to_translate)
        usage_info = ""
        if meanings:
            
            for part_of_speech, definitions in meanings.items():
                usage_info += f"<h4>{part_of_speech}</h4>"
                
                for i, definition in enumerate(definitions[:3]):
                    usage_info += f"<p>- {definition}</p>"
        else:
            usage_info = "<p>No definition found.</p>"
        google_link = f"https://www.google.com/search?q=define+{word_to_translate}"
        dictionary_link = f"https://www.merriam-webster.com/dictionary/{word_to_translate}"
        response_data = {
            'hindi_translation': hindi_word,
            'usage': usage_info,
            'google_link': google_link,
            'dictionary_link': dictionary_link
        }
        return jsonify(response_data)

    except Exception as e:
        
        print(f"An error occurred: {e}")
        return jsonify({'error': 'Failed to process the word.'}), 500
if __name__ == '__main__':
    
    app.run(debug=True, port=5000)
