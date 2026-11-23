import { useState, useEffect } from "react";
import Login from "./components/login";
import RegisterForm from "./components/registerform";
import ExpenseList from "./components/expenselist";

const API_URL = "http://127.0.0.1:8001";

function App() {
  const [page, setPage] = useState("login");
  const [msg, setMsg] = useState("");
  const [token, setToken] = useState(localStorage.getItem("access_token") || "");
  const [exps, setExps] = useState([]);
  const [loaded, setLoaded] = useState(false);

  function showError(data) {
    if (typeof data.detail === "string") {
      setMsg(data.detail);
    } else {
      setMsg(data.detail[0].loc[1] + ": " + data.detail[0].msg);
    }
  }

  function logout() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    setToken("");
    setExps([]);
    setLoaded(false);
    setPage("login");
    setMsg("");
  }

  function refresh() {
    fetch(API_URL + "/refresh", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refresh_token: localStorage.getItem("refresh_token") }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.detail) {
          logout();
          setMsg("Session expired, please log in again");
        } else {
          localStorage.setItem("access_token", data.access_token);
          setToken(data.access_token);
          getExpenses(data.access_token, true);
        }
      })
      .catch(() => setMsg("Cannot reach the server"));
  }

      function getExpenses(tok, tried) {
    fetch(API_URL + "/expenses", {
      headers: { token: tok },
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.detail === "Invalid or expired access token" && tried === false) {
          refresh();
        } else if (data.detail) {
          logout();
          showError(data);
        } else {
          setExps(data.expenses);
          setLoaded(true);
          setMsg("");
        }
      })
      .catch(() => setMsg("Cannot reach the server"));
  }
  
  useEffect(() => {
    if (token !== "") {
      getExpenses(token, false);
    }
  }, []);

  function register(username, email, password) {
    fetch(API_URL + "/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username: username, email: email, password: password }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.detail) {
          showError(data);
        } else {
          setMsg("Registered successfully, please log in");
          setPage("login");
        }
      })
      .catch(() => setMsg("Cannot reach the server"));
  }

  function login(email, password) {
    fetch(API_URL + "/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: email, password: password }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.detail) {
          showError(data);
        } else {
          localStorage.setItem("access_token", data.access_token);
          localStorage.setItem("refresh_token", data.refresh_token);
          setToken(data.access_token);
          setMsg("");
          getExpenses(data.access_token, false);
        }
      })
      .catch(() => setMsg("Cannot reach the server"));
  }

  function goTo(p) {
    setMsg("");
    setPage(p);
  }

  if (token === "") {
    return (
      <>
        <p><b>{msg}</b></p>
        {page === "register" ? (
          <RegisterForm onRegister={register} onBack={() => goTo("login")} />
        ) : (
          <Login onLogin={login} onRegister={() => goTo("register")} />
        )}
      </>
    );
  }

  return (
    <>
      <h1>My Expenses</h1>
      <button onClick={logout}>Log out</button>
      <p><b>{msg}</b></p>
      <ExpenseList exps={exps} loaded={loaded} />
    </>
  );
}

export default App;
