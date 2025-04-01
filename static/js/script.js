// Function to create movie cards (updated to match database fields)
function createMovieCard(movie) {
    return `
        <div class="movie-card">
            <img src="${movie.poster}" alt="${movie.title}" class="movie-poster">
            <div class="movie-info">
                <h3 class="movie-title">${movie.title}</h3>
                <div class="movie-details">
                    <span>${new Date(movie.releaseDate).getFullYear()}</span>
                    <span class="rating">★ ${movie.rating.toFixed(1)}</span>
                </div>
            </div>
            <button class="save-movie-btn" data-movie-id="${movie.id}">💾 Save</button>
        </div>
    `;
}

// Add hover effect function
function initializeHoverEffects() {
    document.querySelectorAll('.movie-card').forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            card.style.transform = `perspective(1000px) rotateX(${(y - rect.height/2)/10}deg) rotateY(${-(x - rect.width/2)/10}deg) translateY(-10px)`;
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0)';
        });
    });
}

// Fetch and populate movies from Flask API
async function populateMovies() {
    try {
        const response = await fetch('/api/movies');
        const categories = await response.json();
        
        const containers = {
            "latest": "#latest-movies",
            "popular": "#popular-movies",
            "action": "#action-movies",
            "Recommended": "#Recommended-movies"
        };

        Object.entries(containers).forEach(([category, selector]) => {
            const container = document.querySelector(selector);
            container.innerHTML = '';
            categories[category].forEach(movie => {
                // Map database fields to expected format
                const movieData = {
                    title: movie.title,
                    poster: movie.poster_path ? 
                        `https://image.tmdb.org/t/p/w500${movie.poster_path}` : 
                        'https://via.placeholder.com/250x350',
                    releaseDate: movie.release_date,
                    rating: movie.vote_average
                };
                container.innerHTML += createMovieCard(movieData);
            });
        });
        
        // Reinitialize hover effects after content loads
        initializeHoverEffects();
    } catch (error) {
        console.error('Error fetching movies:', error);
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    populateMovies();
});


document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".save-movie-btn").forEach(button => {
        button.addEventListener("click", function () {
            let movieId = this.getAttribute("data-movie-id");
            let userId = localStorage.getItem("user_id"); // Assuming user session handling

            if (!userId) {
                alert("Please log in to save movies.");
                return;
            }

            fetch("/api/save_movie", {
                method: "POST",
                body: new URLSearchParams({ user_id: userId, movie_id: movieId }),
                headers: { "Content-Type": "application/x-www-form-urlencoded" }
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert("Error: " + data.error);
                } else {
                    this.textContent = "✔ Saved"; // Change button text on success
                    this.style.backgroundColor = "#2ed573"; // Green color for saved
                }
            })
            .catch(error => console.error("Error:", error));
        });
    });
});
