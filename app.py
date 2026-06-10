"""
Gradio web interface for The Unofficial Guide RAG system.
Run:  python app.py
Then open http://localhost:7860
"""

import gradio as gr
from query import ask

EXAMPLES = [
    "Do I need a Master's degree to get an ML engineering role at a top company?",
    "What kinds of projects actually impress ML interviewers compared to tutorial notebooks?",
    "How long does it typically take a new grad to land their first ML role after graduating?",
    "Should I put Kaggle competitions on my resume when applying to AI/ML roles?",
    "What should my GitHub profile look like when applying for AI/ML internships?",
]


def handle_query(question: str) -> tuple[str, str, str]:
    question = question.strip()
    if not question:
        return "Please enter a question.", "", ""

    result = ask(question)
    answer = result["answer"]

    sources_md = "\n".join(f"• {s}" for s in result["sources"])

    chunks_detail = ""
    for i, c in enumerate(result["chunks"], 1):
        preview = c["text"][:300].replace("\n", " ")
        chunks_detail += (
            f"**[{i}] {c['source_desc'][:70]}**  "
            f"*(distance: {c['distance']:.4f})*\n"
            f"{preview}…\n\n"
        )

    return answer, sources_md, chunks_detail.strip()


with gr.Blocks(
    title="The Unofficial Guide — AI/ML Career Advisor",
    theme=gr.themes.Soft(),
) as demo:
    gr.Markdown(
        """
# The Unofficial Guide
### AI/ML Career Advice from Real Student Experiences

Ask any question about breaking into AI/ML roles as a student or new grad.
Answers are grounded in collected articles, Reddit threads, and career guides —
not general AI knowledge.
        """
    )

    with gr.Row():
        with gr.Column(scale=3):
            question_box = gr.Textbox(
                label="Your question",
                placeholder="e.g. Do I need a Master's degree to break into ML?",
                lines=2,
            )
            with gr.Row():
                submit_btn = gr.Button("Ask", variant="primary", scale=2)
                clear_btn = gr.Button("Clear", scale=1)

    gr.Examples(examples=EXAMPLES, inputs=question_box, label="Try one of these:")

    with gr.Row():
        with gr.Column(scale=2):
            answer_box = gr.Textbox(
                label="Answer (grounded in your documents)",
                lines=12,
                interactive=False,
            )
        with gr.Column(scale=1):
            sources_box = gr.Textbox(
                label="Retrieved from",
                lines=8,
                interactive=False,
            )

    with gr.Accordion("Retrieved chunks (debug)", open=False):
        chunks_box = gr.Markdown()

    submit_btn.click(
        handle_query,
        inputs=question_box,
        outputs=[answer_box, sources_box, chunks_box],
    )
    question_box.submit(
        handle_query,
        inputs=question_box,
        outputs=[answer_box, sources_box, chunks_box],
    )
    clear_btn.click(
        lambda: ("", "", "", ""),
        outputs=[question_box, answer_box, sources_box, chunks_box],
    )

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860, share=False)
