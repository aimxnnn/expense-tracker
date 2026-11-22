import { useState } from "react";

function Login({ onLogin, onRegister }) {
  const [email, setEmail] = useState("");
  const [pw, setPw] = useState("");

  return (
    <>
      <h1>Login</h1>
      <p>
        Email: <input value={email} onChange={(e) => setEmail(e.target.value)} />
      </p>
      <p>
        Password: <input type="password" value={pw} onChange={(e) => setPw(e.target.value)} />
      </p>
      <button onClick={() => onLogin(email, pw)}>Log in</button>
      <p>
        No account yet? <button onClick={onRegister}>Register</button>
      </p>
    </>
  );
}

export default Login;
