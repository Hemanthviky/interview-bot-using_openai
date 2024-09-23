
# Interview Bot using OpenAI

This repository contains a conversational AI-based Interview Bot built using OpenAI's powerful language model API. The bot is designed to simulate an interview experience, where users can interact with it by answering job-specific questions or general interview questions. It leverages the OpenAI GPT model to generate dynamic and relevant interview questions while responding intelligently to user input.

## Features

- **Dynamic Interview Simulation**: The bot generates interview questions in real-time based on the job role or category selected by the user.
- **Conversational Flow**: Interactive question and answer format that mimics a real-world interview experience.
- **User Feedback**: The bot provides feedback based on the user’s responses, helping to improve performance.
- **Customizable**: The bot can be tailored to different roles and domains by modifying the question sets and conversation flows.
- **AI-powered Responses**: Uses OpenAI's GPT API to understand and evaluate user input intelligently.

## Technologies Used

- **Python**: Core programming language for the bot logic.
- **OpenAI API**: Used to generate dynamic and context-aware responses.
- **Git**: Version control system used to manage the project.

## Setup Instructions

### Prerequisites

Before running this project, ensure you have the following installed:

- Python 3.7 or higher
- An OpenAI API key (you can get it by signing up at [OpenAI](https://beta.openai.com/))
- Git

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Hemanthviky/interview-bot-using_openai.git
    cd interview-bot-using_openai
    ```

2. Create a virtual environment (optional but recommended):
    ```bashA
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up your OpenAI API key:
    - Create a `.env` file in the root of your project directory and add the following:
    ```bash
    OPENAI_API_KEY=your_openai_api_key
    ```

5. Run the application:
    ```bash
    python app.py
    ```

## Future Enhancements

- **Role-specific Modules**: Create different modules for various job roles (e.g., software developer, data analyst) with tailored questions.
- **Scoring Mechanism**: Implement a scoring system to evaluate the user's performance.
- **Real-time Feedback**: Improve the feedback mechanism to provide more insightful tips during the interview.
- **Multilingual Support**: Add support for multiple languages for global use.

