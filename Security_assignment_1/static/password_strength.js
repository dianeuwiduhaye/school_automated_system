// password_strength.js

// Function to check the strength of a password
function checkPasswordStrength(password) {
    // Define a regular expression pattern for a strong password
    const strongPasswordPattern = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$/;

    // Check if the password matches the pattern
    if (strongPasswordPattern.test(password)) {
        return 'Strong';
    } else if (password.length >= 8) {
        return 'Medium';
    } else {
        return 'Weak';
    }
}

// Function to update the password strength message
function updatePasswordStrength() {
    const passwordInput = document.getElementById('password');
    const passwordStrengthText = document.getElementById('password-strength');

    const password = passwordInput.value;
    const strength = checkPasswordStrength(password);

    if (strength === 'Strong') {
        passwordStrengthText.textContent = 'Strong';
        passwordStrengthText.style.color = 'green';
    } else if (strength === 'Medium') {
        passwordStrengthText.textContent = 'Medium';
        passwordStrengthText.style.color = 'orange';
    } else {
        passwordStrengthText.textContent = 'Weak';
        passwordStrengthText.style.color = 'red';
    }
}

// Attach the updatePasswordStrength function to the password input field
document.getElementById('password').addEventListener('input', updatePasswordStrength);
