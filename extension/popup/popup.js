document.addEventListener('DOMContentLoaded', function() {
  var getDataButton = document.getElementById('getDataButton');
  var dataContainer = document.getElementById('dataContainer');

  getDataButton.addEventListener('click', function() {
    fetch('http://localhost:5000/get_data/')
      .then(response => response.json())
      .then(data => {
        // Process the received data
        console.log(data);
        // Display data in dataContainer
        dataContainer.textContent = JSON.stringify(data);
      })
      .catch(error => console.error('Error:', error));
  });
});
