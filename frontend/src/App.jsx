import { useState } from "react";
import Attendance from "./pages/attendance";
import AI from "./pages/AI";
import Login from "./pages/Login";

function App() {
  const [user, setUser] = useState(null);
  const [page, setPage] = useState("attendance");

  if (!user) return <Login setUser={setUser} />;

  return (
    <div>
      <h1>AI Attendance System</h1>

      <p>Logged in as: {user.email} ({user.role})</p>

      <button onClick={() => setPage("attendance")}>Attendance</button>
      <button onClick={() => setPage("ai")}>AI</button>

      {user.role === "admin" && (
        <button onClick={() => setPage("admin")}>Admin</button>
      )}

      {page === "attendance" && <Attendance />}
      {page === "ai" && <AI />}
    </div>
  );
}

export default App;