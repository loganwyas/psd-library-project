import Image from "next/image";
import { useEffect, useState } from "react";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const server = "http://127.0.0.1:5000/";
  function login() {
    fetch(server + "login", {
      method: "POST",
      body: JSON.stringify({
        username,
        password,
      }),
      headers: {
        "Content-Type": "application/json",
        Authorization: username,
      },
    })
      .then((response) => response.json())
      .then((response) => console.log(response))
      .catch((error) => console.log(error));
  }

  return (
    <div className="text-center">
      <h1 className="text-3xl font-bold">Login</h1>
      <br />
      <label htmlFor="username">Username: </label>
      <input onChange={(e) => setUsername(e.target.value)} id="username" />
      <br />
      <br />
      <label htmlFor="password">Password: </label>
      <input onChange={(e) => setPassword(e.target.value)} id="password" />
      <br />
      <br />
      <button onClick={login}>Login</button>
    </div>
  );
}
