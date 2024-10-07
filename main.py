from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
from werkzeug.utils import secure_filename
import fitz  # PyMuPDF for PDF text extraction
import ollama  # For quiz generation
import random  # Import random to select random questions

app = Flask(__name__)

# Directory for storing uploaded PDFs
UPLOAD_FOLDER = 'uploads/'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Function to extract text from the PDF and chunk it if it's too large
def extract_text_from_pdf(pdf_path, max_chunk_size=2000):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()

    # Split text into chunks of max_chunk_size characters
    chunks = [text[i:i + max_chunk_size] for i in range(0, len(text), max_chunk_size)]
    return chunks


# Function to generate a quiz based on the extracted text
def generate_quiz_from_text(text, num_questions=5):
    prompt = f"""
        Here is the text from which you generate the {num_questions} questions:

        START OF THE TEXT
        {text}
        END OF THE TEXT

        Please generate exactly {num_questions} multiple-choice question/questions based on the following text. 
        Ensure that you create no more and no less than this specified number, do not use text format. Each of the {num_questions} questions must include:

        Format the {num_questions} questions as follows:
        body of question just the question do not format
        a) Option 1
        b) Option 2
        c) Option 3
        d) Option 4
        Correct answer: . 
        Explanation: ."""

    messages = [{"role": "user", "content": prompt}]

    try:
        response = ollama.chat(model="llama3.2", messages=messages)
        quiz_text = response.get('message', {}).get('content', '')
        return quiz_text.strip()
    except Exception as e:
        print("Error generating quiz:", e)
        return ""


# Function to parse the generated quiz text
def parse_quiz_text(quiz_data):
    questions = []
    current_question = None

    lines = quiz_data.strip().split("\n")

    for line in lines:
        if line.strip() == "":
            continue
        # Check if the line contains a question mark
        if "?" in line.strip():  # Updated line
            if current_question:
                questions.append(current_question)
            # Strip whitespace from the line containing the question
            current_question = {"question": line.strip(), "options": [], "answer": "", "explanation": ""}
        elif line.startswith("a)") or line.startswith("b)") or line.startswith("c)") or line.startswith("d)"):
            if current_question:
                current_question["options"].append(line.strip())
        elif line.startswith("Correct answer:"):
            if current_question:
                correct_answer = line.split(":")[-1].strip().lower()
                current_question["answer"] = correct_answer[0]  # Store only the letter
        elif line.startswith("Explanation:"):
            if current_question:
                explanation = line.split(":")[-1].strip()
                current_question["explanation"] = explanation  # Store the explanation

    if current_question:
        questions.append(current_question)

    return questions


@app.route('/', methods=['GET', 'POST'])
def upload_pdf():
    if request.method == 'POST':
        file = request.files.get('pdf')
        if file and file.filename:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            text_chunks = extract_text_from_pdf(file_path)
            num_questions = int(request.form.get('num_questions', 5))

            all_questions = []

            # Generate all possible questions from all chunks
            for chunk in text_chunks:
                quiz_text = generate_quiz_from_text(chunk, num_questions)  # Pass num_questions per chunk
                parsed_quiz = parse_quiz_text(quiz_text)
                all_questions.extend(parsed_quiz)

            # Randomly select the requested number of questions
            if len(all_questions) > num_questions:
                selected_questions = random.sample(all_questions, num_questions)
            else:
                selected_questions = all_questions

            # Print questions in a readable way
            print("\nGenerated Questions:")
            for i, question in enumerate(all_questions, start=1):
                print(f"\nQuestion {i}: {question['question']}")
                for option in question['options']:
                    print(f"   {option}")
                print(f"Correct answer: {question['answer']}")
                print(f"Explanation: {question['explanation']}")
                print("-" * 50)  # Add a separator for readability

            return render_template('quiz.html', questions=selected_questions)

    return render_template('upload.html')


# Route to handle the submission of answers for a single question
@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    selected_option = request.form.get('selected_option')
    question_text = request.form.get('question')
    correct_answer = request.form.get('correct_answer')

    is_correct = selected_option.lower() == correct_answer.lower()

    response = {
        'is_correct': is_correct,
        'correct_answer': correct_answer
    }
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
