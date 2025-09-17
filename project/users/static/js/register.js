const registerForm = document.getElementById('register-form');
const registerButton = document.getElementById('register-button');
const messageContainer = document.getElementById('message-container');
const passwordInput = document.getElementById('password');
const passwordStrength = document.getElementById('password-strength');

function showMessage(text, type = 'error') {
  messageContainer.innerHTML = `<div class="message ${type} show">${text}</div>`;
  setTimeout(() => {
    const message = messageContainer.querySelector('.message');
    if (message) message.classList.remove('show');
  }, 5000);
}

function setLoading(loading) {
  registerButton.disabled = loading;
  if (loading) {
    registerButton.classList.add('loading');
  } else {
    registerButton.classList.remove('loading');
  }
}

function checkPasswordStrength(password) {
  const strength = {
    score: 0,
    message: '',
    class: ''
  };

  if (password.length >= 8) strength.score++;
  if (/[a-z]/.test(password)) strength.score++;
  if (/[A-Z]/.test(password)) strength.score++;
  if (/[0-9]/.test(password)) strength.score++;
  if (/[^a-zA-Z0-9]/.test(password)) strength.score++;

  if (password.length < 6) {
    strength.message = 'Password too short (minimum 6 characters)';
    strength.class = 'weak';
  } else if (strength.score <= 2) {
    strength.message = 'Weak password - try adding uppercase, numbers, or symbols';
    strength.class = 'weak';
  } else if (strength.score <= 3) {
    strength.message = 'Medium strength - good but could be stronger';
    strength.class = 'medium';
  } else {
    strength.message = 'Strong password!';
    strength.class = 'strong';
  }

  return strength;
}

passwordInput.addEventListener('input', (e) => {
  const password = e.target.value;
  if (password.length > 0) {
    const strength = checkPasswordStrength(password);
    passwordStrength.textContent = strength.message;
    passwordStrength.className = `password-strength ${strength.class}`;
  } else {
    passwordStrength.style.display = 'none';
  }
});

registerForm.addEventListener('submit', async (e) => {
  e.preventDefault();

  const username = document.getElementById('username').value.trim();
  const password = document.getElementById('password').value.trim();

  if (!username || !password) {
    showMessage('Please fill in both fields', 'error');
    return;
  }

  if (password.length < 6) {
    showMessage('Password must be at least 6 characters long', 'error');
    return;
  }

  setLoading(true);
  messageContainer.innerHTML = '';

  try {
    const res = await fetch('/user/api/register/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });

    const text = await res.text();
    
    // Check if response is HTML (error page)
    if (text.trim().startsWith('<!DOCTYPE') || text.trim().startsWith('<html')) {
      console.error('Server returned HTML error page');
      showMessage(`Server error (${res.status}): Please try again later`, 'error');
      return;
    }

    if (!text) {
      showMessage('Server returned empty response', 'error');
      return;
    }

    let data;
    try {
      data = JSON.parse(text);
    } catch (parseError) {
      console.error('Failed to parse JSON:', parseError);
      showMessage('Server error: Invalid response format', 'error');
      return;
    }

    if (res.ok) {
      console.log('Registration successful');
      localStorage.setItem('accessToken', data.access);
      localStorage.setItem('refreshToken', data.refresh);

      showMessage('Account created successfully! Redirecting...', 'success');

      // Redirect to upload page since user is already authenticated
      setTimeout(() => {
        window.location.href = '/user/upload/';
      }, 1000);
    } else {
      const errorMessage = data.detail || data.error || 'Registration failed';
      showMessage(errorMessage, 'error');
    }
  } catch (err) {
    console.error('Network error:', err);
    showMessage('Connection error: Unable to reach server', 'error');
  } finally {
    setLoading(false);
  }
});

// Add enter key support
document.addEventListener('keypress', (e) => {
  if (e.key === 'Enter' && !registerButton.disabled) {
    registerForm.dispatchEvent(new Event('submit'));
  }
});