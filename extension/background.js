if (typeof browser === 'undefined') {
  var browser = chrome;
}

browser.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'fetchCredentials') {
    fetch('http://127.0.0.1:5000/get_password/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ url: request.url })
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      console.log('Received data:', data);
      sendResponse(data);
    })
    .catch(error => {
      console.error('Error fetching password:', error);
      sendResponse({ error: 'Failed to fetch credentials' });
    });
    return true; // Keep the message channel open for sendResponse
  } else if (request.action === 'saveCredentials') {
    fetch('http://127.0.0.1:5000/save_password/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        url: request.url,
        username: request.username,
        password: request.password
      })
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      sendResponse({ success: true });
    })
    .catch(error => {
      console.error('Error saving password:', error);
      sendResponse({ error: 'Failed to save credentials' });
    });
    return true; // Keep the message channel open for sendResponse
  }
});
