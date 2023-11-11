import React, { useState, useEffect } from 'react';

export default function Profile() {
    const [name, setName] = useState('');
    const [tempName, setTempName] = useState('');
    const [password, setPassword] = useState('');
    const [tempPassword, setTempPassword] = useState('');
    const [profilePic, setProfilePic] = useState(null);
    const [error, setError] = useState('');

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
        if (savedProfilePic) setProfilePic(savedProfilePic);
    }, []);

    const validateName = (name) => {
        return name.trim() !== '';
    };

    const validatePassword = (password) => {
        return password.length >= 6;
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
                <input type="text" value={tempName} onChange={(e) => setTempName(e.target.value)} />
            </div>
            <div className="form-group">
                <label>Password:</label>
                <input type="password" value={tempPassword} onChange={(e) => setTempPassword(e.target.value)} />
            </div>
            <div className="form-group">
                <label>Profile Picture:</label>
                <input type="file" onChange={handleProfilePicChange} />
            </div>
            {profilePic && <img src={profilePic} alt="Profile" className="profile-pic" />}
            <button onClick={handleSave}>Save Changes</button>
            {error && <div className="error-message">{error}</div>}
        </div>
    );
}
