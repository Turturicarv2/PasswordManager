document.addEventListener('DOMContentLoaded', function() {
  const statusElement = document.getElementById('status');

  // Send a request to the server
  fetch('http://127.0.0.1:5000/')
    .then(response => {
      if (response.ok) {
        return response.json();
      } else {
        throw new Error('Network response was not ok.');
      }
    })
    .then(data => {
      if (data.success === true) {
        statusElement.textContent = 'Logged in';
      } else {
        statusElement.textContent = 'Log into your password manager';
      }
    })
    .catch(error => {
      console.error('Error:', error);
      statusElement.textContent = 'Error';
    });
});
