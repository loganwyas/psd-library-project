// Page to login to the application

"use client";

import { useEffect, useState } from "react";
import { redirect } from "next/navigation";
import Cookies from "universal-cookie";
import { User } from "@/models/User";
const cookies = new Cookies();

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loggingIn, setLogging] = useState(false);

  const server = "http://127.0.0.1:5001/";
  function login(creatingAccount: boolean) {
    let address = creatingAccount ? "create_account" : "login";
    setLogging(false);
    fetch(server + address, {
      method: "POST",
      body: JSON.stringify({
        username: username.trim(),
        password: password.trim(),
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
            ? "Failed to create an account. This is most likely because the username already exists."
            : "Failed to login. This is most likely because the username or password are incorrect.";
          throw new Error(message);
        }
      })
      .then((user: User) => {
        sessionStorage.setItem("profilePic", user.profilePic);
        user.profilePic = "";
        cookies.set("user", user, { path: "/" });
        setLogging(true);
      })
      .catch((error: Error) => setError(error.message));
  }

  function inputFilled() {
    return !(username.trim() !== "" && password.trim() !== "");
  }

  useEffect(() => {
    let user = cookies.get("user");
    console.log(user);
    if (user) {
      redirect("/");
    }
  }, [loggingIn]);

  return (
    <div className="text-center">
      <h1 className="text-3xl font-bold">Login</h1>
      <br />
      <label htmlFor="username">Username: </label>
      <input
        onChange={(e) => setUsername(e.target.value)}
        id="username"
        className="px-1"
      />
      <br />
      <br />
      <label htmlFor="password">Password: </label>
      <input
        onChange={(e) => setPassword(e.target.value)}
        id="password"
        className="px-1"
      />
      <br />
      <br />
      <div>
        <button
          onClick={() => login(false)}
          className={
            "mr-3 p-2 border border-solid border-black " +
            (inputFilled() ? "text-gray-400 border-gray-400" : "")
          }
          disabled={inputFilled()}
        >
          Login
        </button>
        <button
          onClick={() => login(true)}
          className={
            "ml-3 p-2 border border-solid border-black " +
            (inputFilled() ? "text-gray-400 border-gray-400" : "")
          }
          disabled={inputFilled()}
        >
          Create Account
        </button>
      </div>
      {error && (
        <div className="mt-10">
          <p className="text-red-400">{error}</p>
        </div>
      )}
    </div>
  );
}
