// Page for the user profile

"use client";

import Image from "next/image";
import { User } from "@/models/User";
import { useState, useEffect } from "react";
import { redirect } from "next/navigation";
import Cookies from "universal-cookie";
const cookies = new Cookies();

export default function Profile() {
  const [user, setUser] = useState(null as unknown as User);
  const [tempName, setTempName] = useState("");
  const [tempPassword, setTempPassword] = useState("");
  const [tempProfilePic, setTempProfilePic] = useState("");
  const [profilePicChanged, setProfilePicChanged] = useState(false);
  const [error, setError] = useState("");

  const server = "http://127.0.0.1:5001/";

  useEffect(() => {
    let userCookie: User = cookies.get("user");
    if (!userCookie) {
      redirect("/");
    } else {
      setUser(userCookie);
      const savedName = userCookie.name;
      const savedPassword = userCookie.password;
      const savedProfilePic = sessionStorage.getItem("profilePic");

      if (savedName) {
        setTempName(savedName);
      }
      if (savedPassword) {
        setTempPassword(savedPassword);
      }
      if (savedProfilePic !== null && savedProfilePic !== "null") {
        setTempProfilePic(savedProfilePic);
      }
    }
  }, []);

  function validateName(name: string) {
    return name.trim() !== "";
  }

  function validatePassword(password: String) {
    return password.length >= 6;
  }

  function validateChanged() {
    return (
      !validateName(tempName) ||
      !validatePassword(tempPassword) ||
      (user.name === tempName &&
        user.password === tempPassword &&
        !profilePicChanged)
    );
  }

  function handleSave() {
    if (!validateName(tempName) || !validatePassword(tempPassword)) {
      setError("Invalid input");
      return;
    }

    fetch(server + "profile", {
      method: "POST",
      body: JSON.stringify({
        username: user.username,
        password: tempPassword.trim(),
        name: tempName,
        profilePic: tempProfilePic,
      }),
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => {
        if (response.status == 200) {
          sessionStorage.setItem("profilePic", tempProfilePic);
          let tempUser = user;
          tempUser.name = tempName;
          tempUser.password = tempPassword;
          tempUser.profilePic = "";
          cookies.set("user", tempUser, { path: "/" });
          setUser(tempUser);
          window.location.reload();
        } else {
          let message = "Failed to change profile.";
          throw new Error(message);
        }
      })
      .catch((error: Error) => setError(error.message));

    setError("");
  }

  function handleProfilePicChange(file: File | null) {
    if (!file) return;

    const reader = new FileReader();
    reader.onloadend = () => {
      if (reader.result) {
        setTempProfilePic(reader.result as string);
        setProfilePicChanged(true);
      }
    };
    reader.onerror = () => {
      setError("Error in reading the file");
    };
    reader.readAsDataURL(file);
  }

  return (
    <div className="text-center">
      <h1 className="text-3xl font-bold mb-5">Profile</h1>

      {user && (
        <div>
          <label htmlFor="name">Name:</label>
          <input
            type="text"
            id="name"
            className="px-1"
            value={tempName}
            onChange={(e) => setTempName(e.target.value)}
          />
          <br />
          <br />

          <label htmlFor="newPassword">Password:</label>
          <input
            type="text"
            id="newPassword"
            className="px-1"
            value={tempPassword}
            onChange={(e) => setTempPassword(e.target.value)}
          />
          <br />
          <br />

          <input
            type="file"
            id="profilePic"
            className="hidden"
            onChange={(event) =>
              handleProfilePicChange(
                event.target.files ? event.target.files[0] : null
              )
            }
          />

          <label htmlFor="profilePic">
            <div className="w-80 mx-auto cursor-pointer">
              <img
                src={
                  tempProfilePic
                    ? tempProfilePic
                    : "/profile-img-placeholder.png"
                }
                alt="Profile Picture"
                className="rounded-full w-80 h-80"
              />
            </div>
          </label>
          <button
            className={
              "mt-10 mr-3 p-2 border border-solid border-black " +
              (validateChanged() ? "text-gray-400 border-gray-400" : "")
            }
            disabled={validateChanged()}
            onClick={handleSave}
          >
            Save Changes
          </button>
          {error && <div className="error-message">{error}</div>}
        </div>
      )}
    </div>
  );
}
