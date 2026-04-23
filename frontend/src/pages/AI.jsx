const askAI = async () => {
  try {
    if (!query.trim()) {
      setAnswer("Please enter a question");
      return;
    }

    const res = await API.post("/ai/query", {
      query: query
    });

    console.log("AI RESPONSE:", res.data);

    // ✅ Handle all possible backend responses
    if (res.data.answer) {
      setAnswer(res.data.answer);
    } else if (res.data.response) {
      setAnswer(res.data.response);
    } else if (res.data.error) {
      setAnswer("Error: " + res.data.error);
    } else {
      setAnswer("No valid response from AI");
    }

  } catch (err) {
    console.error("AI ERROR:", err);

    // ✅ Show actual backend error if exists
    if (err.response?.data?.detail) {
      setAnswer("Error: " + err.response.data.detail);
    } else {
      setAnswer("AI error, try again");
    }
  }
};