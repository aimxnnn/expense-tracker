import { useState } from "react";

function RegisterForm({ onRegister, onBack }) {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [pw, setPw] = useState("");

  return (
    <>
      <h1>Register</h1>
      <p>
        Username: <input value={name} onChange={(e) => setName(e.target.value)} />
      </p>
      <p>
        Email: <input value={email} onChange={(e) => setEmail(e.target.value)} />
      </p>
      <p>
        Password: <input type="password" value={pw} onChange={(e) => setPw(e.target.value)} />
      </p>
      <button onClick={() => onRegister(name, email, pw)}>Register</button>
      <p>
        Already have an account? <button onClick={onBack}>Back to login</button>
      </p>
    </>
  );
}

export default RegisterForm;
