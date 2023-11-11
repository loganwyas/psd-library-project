import React from 'react';
import { render, fireEvent, screen } from '@testing-library/react';
import Profile from './Profile';

describe('Profile Component', () => {
  // Test to check if the Profile component renders correctly
  test('renders Profile component', () => {
    render(<Profile />);
    expect(screen.getByText('Profile')).toBeInTheDocument();
  });

  // Test to check if the user can enter a name and password
  test('allows the user to enter name and password', () => {
    render(<Profile />);
    fireEvent.change(screen.getByLabelText('Name:'), { target: { value: 'John Doe' } });
    fireEvent.change(screen.getByLabelText('Password:'), { target: { value: 'password123' } });

    expect(screen.getByLabelText('Name:').value).toBe('John Doe');
    expect(screen.getByLabelText('Password:').value).toBe('password123');
  });

  // Test to validate password length
  test('validates password length', () => {
    render(<Profile />);
    fireEvent.change(screen.getByLabelText('Password:'), { target: { value: 'short' } });

    expect(screen.getByText('Password must be at least 6 characters')).toBeInTheDocument();
  });

  // Test for image file upload
  test('allows a profile picture to be uploaded', () => {
    render(<Profile />);
    const file = new File(['(⌐□_□)'], 'chucknorris.png', { type: 'image/png' });
    const input = screen.getByLabelText('Profile Picture:');

    fireEvent.change(input, { target: { files: [file] } });
    expect(input.files[0]).toBe(file);
    expect(input.files.item(0)).toBe(file);
    expect(input.files).toHaveLength(1);
  });

  // Test for error message when an invalid file is uploaded
  test('shows an error message for large file size', () => {
    render(<Profile />);
    const bigFile = new File(['a'.repeat(1048577)], 'bigfile.png', { type: 'image/png' }); // File larger than 1MB
    fireEvent.change(screen.getByLabelText('Profile Picture:'), { target: { files: [bigFile] } });

    expect(screen.getByText('File size should be less than 1MB')).toBeInTheDocument();
  });

  // Add more tests as needed...
});
