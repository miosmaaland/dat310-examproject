// When the page is loaded
window.addEventListener('load', function() {
  // Get the form element
  const form = document.querySelector('form');

  // Add an event listener to the form
  form.addEventListener('submit', function(event) {
    // Prevent the form from submitting
    event.preventDefault();

    // Get the selected genre and platform
    const genre = document.querySelector('[name="genre"]').value;
    const platform = document.querySelector('[name="platform"]').value;

    // Make a GET request to the server to get the movies
    fetch(`/movies?genre=${genre}&platform=${platform}`)
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(movies => {
        // Update the DOM with the movies information
        const moviesContainer = document.querySelector('.movies-container');
        moviesContainer.innerHTML = '';

        movies.forEach(movie => {
          const movieEl = document.createElement('div');
          movieEl.classList.add('movie');

          const titleEl = document.createElement('h2');
          titleEl.textContent = movie.title;
          movieEl.appendChild(titleEl);

          const descriptionEl = document.createElement('p');
          descriptionEl.textContent = movie.description;
          movieEl.appendChild(descriptionEl);

          const imageEl = document.createElement('img');
          imageEl.setAttribute('src', movie.image_url);
          imageEl.setAttribute('alt', movie.title);
          movieEl.appendChild(imageEl);

          moviesContainer.appendChild(movieEl);
          app.get('/movies', function(req, res) {
            const genre = req.query.genre;
            const platform = req.query.platform;
          
            const query = `SELECT * FROM movies WHERE genre = '${genre}' AND platform = '${platform}'`;
          
            db.all(query, [], function(err, rows) {
              if (err) {
                console.error(err.message);
                res.status(500).send('Internal server error');
                return;
              }
          
              if (rows.length == 0) {
                res.status(404).send('No movies found for the given genre and platform');
                return;
              }
          
              // Send the movie data as a JSON response
              res.json(rows);
            });
          });
          
        });
      })
      .catch(error => {
        console.error('Error:', error);
      });
  });
});
