**🤖 Saksham Jain: AI-Powered Career Chatbot**
An intelligent, interactive career chatbot designed to act as a digital professional persona for Saksham Jain. This application serves as a dynamic resume, capable of answering questions about my background, skills, and projects in a professional and engaging manner.

✨ **Key Features**
Interactive Professional Persona: Acts as a knowledge base for my career, experience, and skills, providing instant and accurate answers to inquiries from recruiters or potential clients.

**Dynamic Data Ingestion:** The chatbot's knowledge is sourced from a collection of documents, including a resume, project summaries, and a comprehensive FAQ guide. This allows for easy updates and ensures all responses are based on factual information.

**Intelligent Tool Use & Lead Capture:** The application is equipped with a powerful lead-capture mechanism. It is designed to subtly and professionally ask for user details (name, email, mobile number) and uses an integrated tool to securely record this information.

**Actionable Feedback Loop:** The bot can identify questions it cannot answer. It automatically uses a tool to record these "unknown" questions, providing valuable data for continuous improvement of the knowledge base.

**Real-time Notifications:** An integrated Push notification system ensures that I am instantly alerted when a potential lead provides their contact information or when the bot encounters a question it cannot answer, enabling immediate follow-up.

**Intuitive Web Interface:** Built with Gradio, the application provides a simple, clean chat interface accessible via a web browser, ensuring a seamless user experience.

🏗️ **Project Architecture**
The core of the application is a Python script that orchestrates communication between the user interface, an advanced LLM (GPT-4o-mini), and a suite of custom tools.

**Data Ingestion:** Upon initialization, the Me class reads and processes data from local files (FAQs.txt, Resume.pdf, Projects.txt). This context is then used to create a detailed system prompt.

**LLM Integration:** The chat function sends the user's message and the detailed system prompt to the OpenAI API. The LLM acts as the core conversational engine, using the provided context to generate professional responses.

**Tooling & Function Calling:** The LLM is empowered with two key functions: record_user_details and record_unknown_question. When the LLM determines a user's intent matches a tool's purpose (e.g., providing an email), it automatically calls the function.

**External Services:** These functions interact with the Pushover API to send real-time, actionable notifications.

**Gradio UI:** A lightweight web application is deployed using Gradio to provide an intuitive and accessible interface for user interaction.

🚀 **Skills Demonstrated**
This project showcases a practical application of a variety of in-demand skills:

**Product Development:** Conceptualizing and building a solution that provides clear user value (instant answers) and business value (lead generation, data collection).

**AI/ML Application:** Leveraging an advanced LLM and prompt engineering to create a professional and domain-specific chatbot persona.

**API Integration:** Seamlessly integrating with multiple third-party APIs (OpenAI, Pushover) to build a sophisticated and feature-rich application.

**Python Development:** Building a robust, modular, and well-structured Python application.

**DevOps & Deployment:** The code is designed for easy local deployment and containerization, with clear instructions for environment setup.

🛠️ **Setup & Installation**
To run this chatbot locally, follow these steps:

Prerequisites
Python 3.9+

pip package manager

1. Set up Pushover
Sign up for an account on Pushover.

Create a new application to get your Application API Token.

Find your User Key in the Pushover dashboard.

2. Set up OpenAI
Sign up for an account and get an API key from OpenAI.

3. Clone the repository and install dependencies
# Clone this repository to your local machine
git clone https://github.com/your-username/your-repo.git
cd your-repo

# Install the required Python libraries
pip install openai python-dotenv pypdf requests gradio


4. Create the necessary files
Create a .env file in the project's root directory with your API keys:

OPENAI_API_KEY="your_openai_api_key"
PUSHOVER_TOKEN="your_pushover_app_token"
PUSHOVER_USER="your_pushover_user_key"

Ensure your data files (FAQs.txt, Resume.pdf, Projects.txt) are located in the 1_foundations/me/ directory as referenced in the code.

5. Run the application
# Start the Gradio server
python your_main_file_name.py


This will launch a local server, and you can access the chatbot at the provided URL in your terminal.
