"use client";

import { useEffect, useState } from "react";
import { redirect } from "next/navigation";
import Cookies from "universal-cookie";
const cookies = new Cookies();

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loggingIn, setLogging] = useState(false);

  const server = "http://127.0.0.1:5001/";
  function login(creatingAccount: boolean) {
    let address = creatingAccount ? "create_account" : "login";
    fetch(server + address, {
      method: "POST",
      body: JSON.stringify({
        username: username.trim(),
        password,
        role: "user",
      }),
      headers: {
        "Content-Type": "application/json",
        Authorization: username,
      },
    })
      .then((response) => {
        if (response.status == 200) {
          return response.json();
        } else {
          let message = creatingAccount
            ? "Failed to create an account"
            : "Failed to login";
          throw new Error(message);
        }
      })
      .then((user) => {
        cookies.set("user", user, { path: "/" });
        setLogging(true);
      })
      .catch((error) => console.log(error));
  }

  useEffect(() => {
    let user = cookies.get("user");
    if (user) {
      redirect("/");
    }
  }, [loggingIn]);

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
      <div>
        <button onClick={() => login(false)}>Login</button>
        <button onClick={() => login(true)}>Create Account</button>
      </div>
    </div>
  );
}
