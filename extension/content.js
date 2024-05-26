document.addEventListener('focusin', function(event) {
  const field = event.target;
  if (field.tagName.toLowerCase() === 'input' && field.type === 'password') {
    const url = window.location.href;
    chrome.runtime.sendMessage({ action: 'fetchCredentials', url }, (data) => {
      if (data && !data.error) {
        const form = field.closest('form');
        const usernameField = form.querySelector('input[type="text"]');
        if (usernameField && data.username) {
          usernameField.value = data.username;
        }
        if (data.password) {
          field.value = data.password;
        }
      } else {
        console.error('Failed to fetch credentials:', data.error);
      }
    });
  }
});

document.addEventListener('submit', function(event) {
  const form = event.target;
  const usernameField = form.querySelector('input[type="text"]');
  const passwordField = form.querySelector('input[type="password"]');

  if (usernameField && passwordField) {
    const url = window.location.href;
    const username = usernameField.value;
    const password = passwordField.value;
    chrome.runtime.sendMessage({ action: 'saveCredentials', url, username, password }, (response) => {
      if (response && response.success) {
        console.log('Credentials saved successfully');
      } else {
        console.error('Failed to save credentials:', response.error);
      }
    });
  }
});
