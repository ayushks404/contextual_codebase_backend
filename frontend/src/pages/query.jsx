
import { useState, useEffect, useRef } from "react";
import { useParams } from "react-router-dom";
import API from "../api";
import { Send, Loader2, FileText, Sparkles } from "lucide-react";

export default function Query() {
  const { projectId } = useParams();   // real project id from URL
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [projectName, setProjectName] = useState("");
  const boxRef = useRef();

  // Load project info
  useEffect(() => {
    const loadProject = async () => {
      try {
        const res = await API.get(`/project/${projectId}`);
        setProjectName(res.data.name);
      } catch (err) {
        console.error("Failed to load project", err);
      }
    };

    if (projectId) loadProject();
  }, [projectId]);

  // Auto scroll
  useEffect(() => {
    if (boxRef.current) {
      boxRef.current.scrollTop = boxRef.current.scrollHeight;
    }
  }, [messages]);

  const send = async () => {
    if (!question.trim() || loading) return;

    const userMsg = { role: "user", text: question };
    setMessages((m) => [...m, userMsg]);
    setQuestion("");
    setLoading(true);

    try {
      const res = await API.post("/query", { project_id: projectId, question });

      const ans =
        res.data?.res?.ans ||
        res.data?.answer ||
        res.data?.answer_text ||
        "No answer";

      const sources = res.data?.res?.sources || res.data?.sources || [];

      const aiMsg = { role: "ai", text: ans, sources };
      setMessages((m) => [...m, aiMsg]);
    } catch (e) {
      setMessages((m) => [
        ...m,
        { role: "ai", text: "Query failed. Please try again.", sources: [] },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-black">
      <div className="max-w-5xl mx-auto p-6">

        {/* Header */}
        <div className="flex items-center justify-between mb-6 bg-gray-900 border border-gray-800 rounded-xl p-4">
          <div className="flex items-center gap-3">
            <Sparkles className="text-blue-500" size={24} />
            <div>
              <h1 className="text-xl font-bold text-white">Project Query</h1>
              <p className="text-xs text-gray-500">Ask questions about your codebase</p>
            </div>
          </div>
          <div className="text-sm text-gray-400">
            Project: <span className="text-white font-medium">{projectName || "Loading..."}</span>
          </div>
        </div>

        {/* Messages */}
        <div
          ref={boxRef}
          className="h-[65vh] overflow-y-auto bg-gray-900 border border-gray-800 rounded-xl p-6 mb-4 space-y-4"
        >
          {messages.map((m, i) => (
            <div key={i} className={m.role === "user" ? "text-right" : "text-left"}>
              <div
                className={`inline-block max-w-3xl px-4 py-3 rounded-xl ${
                  m.role === "user"
                    ? "bg-blue-600 text-white"
                    : "bg-gray-800 text-gray-300 border border-gray-700"
                }`}
              >
                {m.text}

                {m.sources?.length > 0 && (
                  <div className="mt-3 pt-3 border-t border-gray-700 text-xs text-gray-400">
                    Sources:
                    {m.sources.map((s, idx) => (
                      <div key={idx}>• {s.file || s}</div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}

          {loading && (
            <div className="flex justify-start">
              <Loader2 className="animate-spin text-blue-500" />
            </div>
          )}
        </div>

        {/* Input */}
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-4">
          <textarea
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask a question..."
            className="w-full bg-black border border-gray-700 text-white rounded-lg p-3"
            onKeyDown={(e) => {
              if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) send();
            }}
          />

          <div className="mt-3 flex justify-end">
            <button
              onClick={send}
              disabled={loading}
              className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg text-white flex items-center gap-2"
            >
              {loading ? "Thinking..." : "Send"}
              <Send size={16} />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
