from flask import Flask, render_template, request, jsonify
from rag_engine import process_pdf, ask_question
import os

app = Flask(__name__)
UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER", "/tmp/uploads")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        if "pdf" in request.files:
            pdf_file = request.files["pdf"]
            if pdf_file.filename != "":
                safe_name = os.path.basename(pdf_file.filename)
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], safe_name)
                pdf_file.save(filepath)
                num_chunks = process_pdf(filepath)
                return jsonify({"status": "success", "chunks": num_chunks})

        elif "question" in request.form:
            question = request.form["question"]
            result = ask_question(question)
            return jsonify(result)

    return render_template("index.html")

application = app

if __name__ == "__main__":
    print("🚀 Starting PDF RAG Chat...")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)