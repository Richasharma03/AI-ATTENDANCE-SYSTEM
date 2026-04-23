import React, { useState } from "react";
import API from "../api";

const AI = () => {
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState("");

  const askAI = async () => {
    try {
      // ✅ correct GET request with query param
      const res = await API.get(`/ai/query?query=${query}`);

      console.log(res.data);

      // ✅ handle different response formats
      setAnswer(
        res.data.response ||
        res.data.answer ||
        JSON.stringify(res.data)
      );

    } catch (err) {
      console.error(err);
      setAnswer("AI error, try again");
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