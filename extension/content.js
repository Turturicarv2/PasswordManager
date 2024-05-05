// content.js

// Listen for focus or load events on input fields
document.addEventListener('focusin', async function(event) {
    const field = event.target;
    if (field.tagName.toLowerCase() === 'input' && field.type === 'password') {
      // Send a request to the server to retrieve credentials
      try {
        const response = await fetch('http://127.0.0.1:5000/get_password/');
        const data = await response.json();
  
        // Autofill the password field
        field.value = data.password;
      } catch (error) {
        console.error('Error fetching password:', error);
      }
    }
  });
  
  // Listen for form submission events
  document.addEventListener('submit', async function(event) {
    const form = event.target;
    const usernameField = form.querySelector('input[type="text"]');
    const passwordField = form.querySelector('input[type="password"]');
  
    // Check if the form has both username and password fields
    if (usernameField && passwordField) {
      // Send the username and password to the server
      const username = usernameField.value;
      const password = passwordField.value;
      try {
        await fetch('http://127.0.0.1:5000/save_password/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ username, password })
        });
      } catch (error) {
        console.error('Error saving credentials:', error);
      }
    }
  });
  