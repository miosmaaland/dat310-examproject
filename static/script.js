// Get elements from the DOM
const form = document.querySelector('form');
const usernameInput = document.querySelector('input[name="username"]');
const passwordInput = document.querySelector('input[name="password"]');
const addressBookContainer = document.querySelector('#address-book-container');

// Handle form submission for logging in
form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const formData = new FormData(form);
  const username = formData.get('username');
  const password = formData.get('password');

  const response = await fetch('/login', {
    method: 'POST',
    body: JSON.stringify({ username, password }),
    headers: {
      'Content-Type': 'application/json'
    }
  });

  const data = await response.json();
  if (response.ok) {
    // Redirect to the home page
    window.location.replace('/');
  } else {
    // Display an error message
    alert(data.message);
  }
});

// Get the address book for the logged-in user
async function getAddressBook() {
  const response = await fetch('http://127.0.0.1:5000/');
  const data = await response.json();
  if (response.ok) {
    // Display the address book
    let html = '';
    for (const name in data) {
      const address = data[name];
      html += `<div><strong>${name}:</strong> ${address}</div>`;
    }
    addressBookContainer.innerHTML = html;
  } else {
    // Display an error message
    addressBookContainer.innerHTML = `<div>${data.message}</div>`;
  }
}

// Add a new contact to the address book
async function addContact(name, address) {
  const response = await fetch('/address_book', {
    method: 'POST',
    body: JSON.stringify({ [name]: address }),
    headers: {
      'Content-Type': 'application/json'
    }
  });

  const data = await response.json();
  if (response.ok) {
    // Refresh the address book
    getAddressBook();
  } else {
    // Display an error message
    alert(data.message);
  }
}

// Edit an existing contact in the address book
async function editContact(name, address) {
  const response = await fetch('/address_book', {
    method: 'PUT',
    body: JSON.stringify({ [name]: address }),
    headers: {
      'Content-Type': 'application/json'
    }
  });

  const data = await response.json();
  if (response.ok) {
    // Refresh the address book
    getAddressBook();
  } else {
    // Display an error message
    alert(data.message);
  }
}

// Delete a contact from the address book
async function deleteContact(name) {
  const response = await fetch('/address_book', {
    method: 'DELETE',
    body: JSON.stringify([name]),
    headers: {
      'Content-Type': 'application/json'
    }
  });

  const data = await response.json();
  if (response.ok) {
    // Refresh the address book
    getAddressBook();
  } else {
    // Display an error message
    alert(data.message);
  }
}

