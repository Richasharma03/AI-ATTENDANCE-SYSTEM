import React, { useState } from "react";
import API from "../api";

const AI = () => {
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState("");

  const askAI = async () => {
    try {
      const res = await API.post("/ai/query", null, {
        params: { query }
      });

      setAnswer(res.data.answer);
    } catch (err) {
      setAnswer("Error");
    }
  };

  return (
    <div style={{ textAlign: "center" }}>
      <h2>AI Assistant</h2>

      <input
        type="text"
        placeholder="Ask something..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />

      <br /><br />

      <button onClick={askAI}>Ask</button>

      <p>{answer}</p>
    </div>
  );
};

export default AI;