// Pass the Flask URLs to the script.js file
const searchResultsUrl = "{{ url_for('search_results') }}";
const saveSearchUrl = "{{ url_for('search') }}"; // Update the URL to 'search' endpoint

const searchForm = document.querySelector("#search-form");
const switchButtons = document.querySelectorAll("#switch-btn");

switchButtons.forEach((switchBtn) => {
  switchBtn.addEventListener("click", () => {
    const signupForm = document.querySelector("#signup-form");
    const loginForm = document.querySelector("#login-form");

    signupForm.classList.toggle("hidden");
    loginForm.classList.toggle("hidden");

    if (signupForm.classList.contains("hidden")) {
      switchBtn.textContent = "Don't have an account? Sign Up";
    } else {
      switchBtn.textContent = "Already have an account? Log In";
    }
  });
});

searchForm.addEventListener('submit', function(e) {
  e.preventDefault();

  const genre = document.querySelector("#genre").value;
  const platform = document.querySelector("#platform").value;

  fetch(saveSearchUrl, {
    method: 'POST',
    body: new URLSearchParams({
      genre: genre,
      platform: platform
    })
  })
  .then(response => response.text())
  .then(data => {
    document.querySelector("#results").innerHTML = data;
  })
  .catch(error => {
    console.error('Error:', error);
  });
});
document.getElementById('addToListForm').addEventListener('submit', function(event) {
  event.preventDefault();
  var form = event.target;
  var formData = new FormData(form);
  var xhr = new XMLHttpRequest();
  xhr.open(form.method, form.action, true);
  xhr.onload = function() {
      if (xhr.status === 200) {
          window.location.href = '/results';
      }
  };
  xhr.send(formData);
});