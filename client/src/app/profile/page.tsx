"use client";

import { useState, useEffect } from "react";

export default function Profile() {
  const [name, setName] = useState("");
  const [tempName, setTempName] = useState("");
  const [password, setPassword] = useState("");
  const [tempPassword, setTempPassword] = useState("");
  const [profilePic, setProfilePic] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    const savedName = sessionStorage.getItem("name");
    const savedPassword = sessionStorage.getItem("password");
    const savedProfilePic = sessionStorage.getItem("profilePic");

    if (savedName) {
      setName(savedName);
      setTempName(savedName);
    }
    if (savedPassword) {
      setPassword(savedPassword);
      setTempPassword(savedPassword);
    }
    if (savedProfilePic) setProfilePic(savedProfilePic);
  }, []);

  function validateName(name: string) {
    return name.trim() !== "";
  }

  function validatePassword(password: String) {
    return password.length >= 6;
  }

  function handleSave() {
    if (!validateName(tempName) || !validatePassword(tempPassword)) {
      setError("Invalid input");
      return;
    }

    setName(tempName);
    setPassword(tempPassword);
    sessionStorage.setItem("name", tempName);
    sessionStorage.setItem("password", tempPassword);
    setError("");
  }

  function handleProfilePicChange(file: File | null) {
    if (!file) return;

    const reader = new FileReader();
    reader.onloadend = () => {
      setProfilePic(reader.result as string);
      sessionStorage.setItem("profilePic", reader.result as string);
    };
    reader.onerror = () => {
      setError("Error in reading the file");
    };
    reader.readAsDataURL(file);
  }

  return (
    <div className="text-center">
      <h1 className="text-3xl font-bold mb-5">Profile</h1>

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
        type="password"
        id="newPassword"
        className="px-1"
        value={tempPassword}
        onChange={(e) => setTempPassword(e.target.value)}
      />
      <br />
      <br />

      <label htmlFor="profilePic">Profile Picture:</label>
      <input
        type="file"
        id="profilePic"
        onChange={(event) =>
          handleProfilePicChange(
            event.target.files ? event.target.files[0] : null
          )
        }
      />
      <br />
      <br />

      {profilePic && (
        <div className="w-80 mx-auto">
          <img
            src={profilePic}
            alt="Profile"
            className="rounded-full w-80 h-80"
          />
        </div>
      )}
      <button
        className="mt-10 border border-solid border-black p-2"
        onClick={handleSave}
      >
        Save Changes
      </button>
      {error && <div className="error-message">{error}</div>}
    </div>
  );
}
