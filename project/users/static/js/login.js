const loginForm = document.getElementById('login-form');
const loginButton = document.getElementById('login-button');
const messageContainer = document.getElementById('message-container');

function showMessage(text, type = 'error') {
  messageContainer.innerHTML = `<div class="message ${type} show">${text}</div>`;
  setTimeout(() => {
    const message = messageContainer.querySelector('.message');
    if (message) message.classList.remove('show');
  }, 5000);
}

function setLoading(loading) {
  loginButton.disabled = loading;
  if (loading) {
    loginButton.classList.add('loading');
  } else {
    loginButton.classList.remove('loading');
  }
}

loginForm.addEventListener('submit', async (e) => {
  e.preventDefault();

  const username = document.getElementById('username').value.trim();
  const password = document.getElementById('password').value.trim();

  if (!username || !password) {
    showMessage('Please fill in both fields', 'error');
    return;
  }

  setLoading(true);
  messageContainer.innerHTML = '';

  try {
    const res = await fetch('/user/login/', {
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

    if (res.ok && data.success) {
      // Save tokens
      localStorage.setItem('accessToken', data.access);
      if (data.refresh) localStorage.setItem('refreshToken', data.refresh);

      showMessage('Login successful! Redirecting...', 'success');

      // Redirect using the redirect value returned by backend
      const redirectUrl = data.redirect || '/user/upload/';
      setTimeout(() => {
        window.location.href = redirectUrl;
      }, 1000);
    } else {
      // Show error from backend
      const errorMessage = data.error || data.detail || 'Login failed';
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
  if (e.key === 'Enter' && !loginButton.disabled) {
    loginForm.dispatchEvent(new Event('submit'));
  }
});