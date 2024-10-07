from flask import Flask, render_template

app = Flask(__name__)

@app.route('/quiz')
def quiz():
    # Example parsed quiz data
    parsed_quiz = [
        {
            'question': 'What happens as electrons pass through the electron transport chain?',
            'options': [
                'A stepwise release of energy, which is used to drive the chemiosmotic generation of ATP',
                'A gradual decrease in energy levels',
                'The final oxidation is reversible',
                'No change occurs'
            ],
            'answer': 'A stepwise release of energy, which is used to drive the chemiosmotic generation of ATP'
        },
        {
            'question': 'Where is the electron transport chain found in eukaryotic cells?',
            'options': [
                'Outer membrane of mitochondria',
                'Inner membrane of mitochondria',
                'Plasma membrane',
                'Lysosome'
            ],
            'answer': 'Inner membrane of mitochondria'
        },
        {
            'question': 'What accepts the electrons at the end of the electron transport chain?',
            'options': [
                'NADH',
                'FADH2',
                'Oxygen (O2)',
                'ADP'
            ],
            'answer': 'Oxygen (O2)'
        },
        {
            'question': 'How does the transport protein in the electron transport chain alternate between reduced and oxidized states?',
            'options': [
                'By accepting electrons from higher energy levels',
                'By donating electrons to lower energy levels',
                'As it accepts and donates electrons',
                'Only in the presence of oxygen'
            ],
            'answer': 'As it accepts and donates electrons'
        },
        {
            'question': 'What is created by pumping H+ across the matrix membrane into the intermembrane space?',
            'options': [
                'An electrochemical gradient',
                'A proton-motive force',
                'ATP synthase',
                'Chemiosmosis'
            ],
            'answer': 'An electrochemical gradient'
        },
        {
            'question': 'What converts the flow of protons to ADP -> ATP phosphorylation?',
            'options': [
                'Electron transport chain',
                'Chemiosmosis',
                'ATP synthase',
                'FADH2'
            ],
            'answer': 'ATP synthase'
        },
        {
            'question': 'What is produced in anaerobic respiration?',
            'options': [
                'Much more energy than aerobic respiration',
                'The same amount of energy as aerobic respiration',
                'Much less energy than aerobic respiration',
                'No energy at all'
            ],
            'answer': 'Much less energy than aerobic respiration'
        },
        {
            'question': 'What is the final electron acceptor in anaerobic respiration?',
            'options': [
                'Oxygen (O2)',
                'Sulfate',
                'ADP',
                'NADH'
            ],
            'answer': 'Sulfate'
        },
        {
            'question': 'How does lactic acid fermentation differ from alcohol fermentation?',
            'options': [
                'Lactic acid fermentation produces more ATP than alcohol fermentation',
                'Lactic acid fermentation is used in brewing and winemaking',
                'Lactic acid fermentation converts pyruvate to lactate in one step',
                'Alcohol fermentation converts pyruvate to ethanol in two steps'
            ],
            'answer': 'Lactic acid fermentation converts pyruvate to lactate in one step'
        },
        {
            'question': 'What is the main difference between aerobic and anaerobic respiration?',
            'options': [
                'Aerobic respiration produces more ATP than anaerobic respiration',
                'Anaerobic respiration uses a final electron acceptor other than oxygen (O2)',
                'Both options a and b are correct',
                'Neither option a nor b is correct'
            ],
            'answer': 'Both options a and b are correct'
        }
    ]
    return render_template('quiz.html', questions=parsed_quiz)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
