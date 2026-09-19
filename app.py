from flask import Flask, render_template, request, Response, stream_with_context, jsonify
import ollama
from database import load_all_chats, save_chat_session, get_chat_history
from rag import search_docs, add_document_to_rag  # Import RAG search & add functions
import uuid

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/sessions', methods=['GET'])
def sessions():
    return jsonify(load_all_chats())

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_msg = data.get("message")
    session_id = data.get("session_id") or str(uuid.uuid4())
    
    # 1. Load chat history for the session
    history = get_chat_history(session_id)

    # 2. RAG Step: Search your vector database for relevant context based on user's query
    retrieved_context = search_docs(user_msg, n_results=2)

    # 3. Inject retrieved context into the prompt if available
    if retrieved_context:
        augmented_message = (
            f"Use the following personal context/information to answer the user if relevant:\n\n"
            f"--- Context Start ---\n{retrieved_context}\n--- Context End ---\n\n"
            f"User Question: {user_msg}"
        )
    else:
        augmented_message = user_msg

    # Append the augmented user message to history for the model
    history.append({"role": "user", "content": augmented_message})

    def generate():
        full_reply = ""
        stream = ollama.chat(model="llama3.2", messages=history, stream=True)
        for chunk in stream:
            token = chunk['message']['content']
            full_reply += token
            yield token
        
        # Restore original user message in history before saving so storage stays clean
        history[-1]["content"] = user_msg 
        history.append({"role": "assistant", "content": full_reply})
        save_chat_session(session_id, history)

    return Response(stream_with_context(generate()), headers={"X-Session-ID": session_id})

@app.route('/delete_session/<session_id>', methods=['DELETE'])
def delete_session(session_id):
    from database import delete_chat_session
    success = delete_chat_session(session_id)
    return jsonify({"success": success})

if __name__ == "__main__":
    app.run(debug=True, port=5001)