import React, { useState, useEffect } from 'react';

export default function Profile() {
    const [name, setName] = useState('');
    const [tempName, setTempName] = useState('');
    const [password, setPassword] = useState('');
    const [tempPassword, setTempPassword] = useState('');
    const [profilePic, setProfilePic] = useState(null);
    const [profilePicPreview, setProfilePicPreview] = useState(null);
    const [error, setError] = useState('');
    const [nameError, setNameError] = useState('');
    const [passwordError, setPasswordError] = useState('');

    useEffect(() => {
        const savedName = sessionStorage.getItem('name');
        const savedPassword = sessionStorage.getItem('password');
        const savedProfilePic = sessionStorage.getItem('profilePic');

        if (savedName) {
            setName(savedName);
            setTempName(savedName);
        }
        if (savedPassword) {
            setPassword(savedPassword);
            setTempPassword(savedPassword);
        }
        if (savedProfilePic) {
            setProfilePic(savedProfilePic);
            setProfilePicPreview(savedProfilePic);
        }
    }, []);

    const validateName = (name) => {
        if (name.trim() === '') {
            setNameError('Name cannot be empty');
            return false;
        }
        setNameError('');
        return true;
    };

    const validatePassword = (password) => {
        if (password.length < 6) {
            setPasswordError('Password must be at least 6 characters long');
            return false;
        }
        setPasswordError('');
        return true;
    };

    const handleSave = () => {
        if (!validateName(tempName) || !validatePassword(tempPassword)) {
            setError('Invalid input');
            return;
        }

        setName(tempName);
        setPassword(tempPassword);
        sessionStorage.setItem('name', tempName);
        sessionStorage.setItem('password', tempPassword);
        setError('');
    };

    const handleProfilePicChange = (e) => {
        const file = e.target.files[0];
        if (!file) return;

        if (file.size > 1048576) {
            setError('File size should be less than 1MB');
            return;
        }

        const reader = new FileReader();
        reader.onloadend = () => {
            setProfilePic(reader.result);
            setProfilePicPreview(reader.result);
            sessionStorage.setItem('profilePic', reader.result);
        };
        reader.onerror = () => {
            setError('Error in reading the file');
        };
        reader.readAsDataURL(file);
    };

    return (
        <div className="profile-container">
            <h1>Profile</h1>
            <div className="form-group">
                <label>Name:</label>
                <input type="text" value={tempName} onChange={(e) => setTempName(e.target.value)} onBlur={() => validateName(tempName)} />
                {nameError && <div className="error-message">{nameError}</div>}
            </div>
            <div className="form-group">
                <label>Password:</label>
                <input type="password" value={tempPassword} onChange={(e) => setTempPassword(e.target.value)} onBlur={() => validatePassword(tempPassword)} />
                {passwordError && <div className="error-message">{passwordError}</div>}
            </div>
            <div className="form-group">
                <label>Profile Picture:</label>
                <input type="file" onChange={handleProfilePicChange} />
                {profilePicPreview && <img src={profilePicPreview} alt="Profile Preview" className="profile-pic-preview" />}
            </div>
            {error && <div className="error-message">{error}</div>}
            <button onClick={handleSave}>Save Changes</button>
        </div>
    );
}
