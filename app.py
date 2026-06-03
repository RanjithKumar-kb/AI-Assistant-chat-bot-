from flask import Flask, render_template, request, Response, stream_with_context, jsonify
import ollama
from database import load_all_chats, save_chat_session, get_chat_history
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
    
    history = get_chat_history(session_id)
    history.append({"role": "user", "content": user_msg})

    def generate():
        full_reply = ""
        stream = ollama.chat(model="llama3.2", messages=history, stream=True)
        for chunk in stream:
            token = chunk['message']['content']
            full_reply += token
            yield token
        
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