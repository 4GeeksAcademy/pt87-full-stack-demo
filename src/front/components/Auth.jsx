import { useState } from "react";

const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const onSubmit = async (ev) => {
    ev.preventDefault();

    const resp = await fetch(
      `${import.meta.env.VITE_BACKEND_URL}/api/login`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          username, password
        })
      }
    )

    if (resp.ok) {
      const data = await resp.json();
      // We can do things with that data, like add it to the store.
    }
  }

  return <div className="card">
    <form onSubmit={onSubmit} className="card-body">
      <div className="mb-2">
        <label htmlFor="signupUser" className="form-label">
          Username:
        </label>
        <input
          id="signupUser"
          className="form-control"
          autoComplete="username"
          value={username}
          onChange={(ev) => setUsername(ev.target.value)}
          required
        />
      </div>
      <div className="mb-2">
        <label htmlFor="signupPass" className="form-label">
          Password:
        </label>
        <input
          id="signupPass"
          type="password"
          autoComplete="current-password"
          className="form-control"
          value={password}
          onChange={(ev) => setPassword(ev.target.value)}
          required
        />
      </div>
      <div className="mb-2 d-flex flex-row justify-content-center gap-2">
        <button className="btn btn-primary">Login</button>
        <button className="btn btn-danger" type="reset">
          Cancel
        </button>
      </div>
    </form>
  </div>
}

const Signup = () => {
  return <></>
}

export {
  Signup, Login
}
