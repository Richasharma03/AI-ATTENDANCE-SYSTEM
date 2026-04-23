import React, { useState } from "react";
import API from "../api";

const Login = ({ setUser }) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [msg, setMsg] = useState("");

  const login = async () => {
    try {
      const res = await API.post("/auth/login", {
        email,
        password
      });

      // ✅ STORE TOKEN (VERY IMPORTANT)
      localStorage.setItem("token", res.data.access_token);

      // ✅ SET USER (optional)
      setUser({ email });

      setMsg("Login successful ✅");

    } catch (err) {
      console.log(err);
      setMsg("Login failed ❌");
    }
  };

  return (
    <div>
      <h2>Login</h2>

      <input
        placeholder="Email"
        value={email}
        onChange={e => setEmail(e.target.value)}
      />

      <br /><br />

      <input
        placeholder="Password"
        type="password"
        value={password}
        onChange={e => setPassword(e.target.value)}
      />

      <br /><br />

      <button onClick={login}>Login</button>

      <p>{msg}</p>
    </div>
  );
};

export default Login;