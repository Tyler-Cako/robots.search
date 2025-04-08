from flask import Flask, render_template, request

app = Flask(__name__)

@app.get("/")
def search_page():
    results = [
        {'name': 'Generative Ghosts: Anticipating Benefits and Risks of AI Afterlives', 'url': 'https://deepmind.google/research/publications/65827/', 'description': 'As AI systems quickly improve in both breadth and depth of performance, they lend themselves to creating increasingly powerful and realistic agents, including potentially agents modeled on specific people. We anticipate that within our lifetimes it may become common practice for people to create a custom AI agent to interact with loved ones and/or the broader world after death; we call such embodiments generative ghosts since such agents will be capable of generating novel content rather than merely parroting content produced by their creator while living. In this position paper, we first discuss the design space of potential implementations of generative ghosts. We then discuss the practical and ethical implications of generative ghosts, including potential positive and negative impacts on individuals and society. Based on these considerations, we lay out a research agenda for the AI and HCI research communities to empower people to create and interact with AI afterlives in a safe and beneficial manner.', 'tags': ['AI', 'HCI', 'GenAI']},

        {'name': 'Effective Kernel Fuzzing with Learned White-box Test Mutators', 'url': 'https://deepmind.google/research/publications/127036/', 'description': 'Kernel fuzzers rely heavily on program mutation to automatically generate new test programs based on existing ones. In particular, program mutation can alter the test’s control and data flow inside the kernel by inserting new system calls, changing the values of call arguments, or performing other program mutations. However, due to the complexity of the kernel code and its user-space interface, finding the effective mutation that can lead to the desired outcome such as increasing the coverage and reaching a target code location is extremely difficult, even with the widespread use of manually-crafted heuristics.', 'tags': ['AI', 'Kernel']},
    ]
    return render_template("index.html", results=results)

@app.post('/results')
def search_results():
    search_query = request.form['search_query']
    return render_template("results.html", search_query=search_query)

if __name__ == "__main__":
    app.run(debug=True)