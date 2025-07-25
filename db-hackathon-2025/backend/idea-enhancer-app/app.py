import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part

# Initialize Flask app
app = Flask(__name__)
# Enable CORS for all origins, adjust in production for specific origins
CORS(app)

# When using Vertex AI, it's recommended to use Application Default Credentials (ADC)

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "hack-team-bank-the-unbanked")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

# Configure the Gemini API to use Vertex AI
# and use Google Cloud's authentication mechanisms (like ADC).
try:
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    model = GenerativeModel("gemini-2.5-pro")
    print(f"Successfully configured Vertex AI for project: {PROJECT_ID}, location: {LOCATION}")
    # genai.configure(
    #     project=PROJECT_ID,
    #     location=LOCATION,
    #     vertexai=True
    # )
    # Initialize the Generative Model
    # model = genai.GenerativeModel('gemini-2.0-flash')
    # print(f"Successfully configured Gemini model via Vertex AI for project: {PROJECT_ID}, location: {LOCATION}")
except Exception as e:
    print(f"Error configuring Gemini with Vertex AI: {e}")
    print("Please ensure your GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_LOCATION environment variables are set correctly,")
    print("and that you have authenticated to Google Cloud (e.g., 'gcloud auth application-default login').")
    # In a real application, you might want to exit or handle this more gracefully
    # For now, we'll let the app run but API calls will fail.

@app.route('/enhance_idea', methods=['POST','GET'])
def enhance_idea():
    """
    API endpoint to enhance a user's idea using the Gemini API via Vertex AI.
    Expects a JSON payload with 'idea_text'.
    """
    try:
        data = request.get_json()
        if not data or 'idea_text' not in data:
            return jsonify({"error": "Invalid request. 'idea_text' is required in the JSON payload."}), 400

        idea_text = data['idea_text']

        # Construct the prompt for idea enhancement
        prompt = f"""
        You are an expert business strategist and innovation consultant.
        Your task is to take a raw idea and enhance it to maximize its business potential, market viability, and overall impact.
        Consider aspects like:
        - Target audience refinement
        - Unique selling propositions (USPs)
        - Potential revenue streams
        - Scalability
        - Competitive advantages
        - Implementation challenges and solutions

        Please provide a crips enhanced idea for below raw idea:

        Idea: "{idea_text}"

        Enhanced Idea:
        """


        # Generate content using the Gemini model
        # Ensure the model was successfully initialized
        if 'model' not in globals() or model is None:
            return jsonify({"error": "AI model not initialized. Check server logs for configuration errors."}), 500

        response = model.generate_content(prompt)

        # Extract the enhanced text from the response
        if response.candidates and response.candidates[0].content.parts:
            enhanced_idea = response.candidates[0].content.parts[0].text
        else:
            print(f"Gemini API response structure unexpected: {response}")
            return jsonify({"error": "Failed to get a valid response from the AI model. Please try again."}), 500

        return jsonify({"original_idea": idea_text, "enhanced_idea": enhanced_idea}), 200

    except Exception as e:
        print(f"An error occurred during idea enhancement: {e}")
        return jsonify({"error": f"An internal server error occurred: {str(e)}"}), 500

@app.route('/')
def index():
    """
    Basic route to confirm the server is running.
    """
    return "Idea Enhancement Microservice is running!"

if __name__ == '__main__':
    # Run the Flask app
    # In a production environment, use a production-ready WSGI server like Gunicorn
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, host='0.0.0.0', port=port)
