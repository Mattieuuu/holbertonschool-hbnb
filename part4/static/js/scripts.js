// ======================================================================
// Gestion des événements lors du chargement du DOM
// ======================================================================
document.addEventListener('DOMContentLoaded', () => {
  // Initialisation du formulaire de connexion
  // Cette section gère la soumission du formulaire et l'authentification
  const loginForm = document.getElementById('login-form');
  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();

      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;

      await loginUser(email, password);
    });
  }

  // Vérifie si l'utilisateur est déjà connecté et charge les données nécessaires
  checkAuthentication();

  // Configuration du filtre de prix sur la page d'index
  // Permet aux utilisateurs de filtrer les locations par prix
  const priceFilter = document.getElementById('price-filter');
  if (priceFilter) {
    priceFilter.addEventListener('change', () => {
      const selectedPrice = priceFilter.value;
      filterPlacesByPrice(selectedPrice);
    });
  }

  // Configuration de la page de détails d'une location
  // Cette section ne s'exécute que sur la page de détails spécifique
  const detailsContainer = document.getElementById('place-details');
  if (detailsContainer) {
    const token = getCookie('token');
    const placeId = getPlaceIdFromURL();
    checkAuthAndFetchPlace(token, placeId);
  }
});

// ======================================================================
// Fonctions d'authentification et de gestion des lieux
// ======================================================================

// loginUser : Gère le processus de connexion et stocke le token
// Params: email et password fournis par l'utilisateur
// Retourne: Promesse qui redirige vers index.html en cas de succès
async function loginUser(email, password) {
  try {
    const response = await fetch('http://localhost:5000/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });

    if (response.ok) {
      const data = await response.json();
      document.cookie = `token=${data.access_token}; path=/`;

      alert('✅ Login successful');
      window.location.href = 'index.html';
    } else {
      alert('❌ Login failed: ' + response.statusText);
    }
  } catch (error) {
    alert('Erreur réseau: ' + error.message);
  }
}

// checkAuthentication : Vérifie la présence du token et adapte l'interface
// Cache ou affiche le lien de connexion selon l'état de l'authentification
function checkAuthentication() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');

  if (token) {
    if (loginLink) loginLink.style.display = 'none';
    console.log('✅ Token trouvé :', token);
    fetchPlaces(token);
  } else {
    if (loginLink) loginLink.style.display = 'block';
    console.log('❌ Aucun token trouvé');
  }
}

// getCookie : Utilitaire pour récupérer la valeur d'un cookie
// Param: name - Le nom du cookie à récupérer
// Retourne: La valeur du cookie ou null si non trouvé
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
  return null;
}

// fetchPlaces : Récupère la liste des locations depuis l'API
// Param: token - Le token d'authentification
// Actualise l'affichage avec les données reçues
async function fetchPlaces(token) {
  try {
    const response = await fetch('http://localhost:5000/places/', {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    if (!response.ok) throw new Error('Erreur API: ' + response.statusText);
    const places = await response.json();
    displayPlaces(places);
    window.allPlaces = places;
  } catch (err) {
    console.error('⛔ fetchPlaces error:', err);
  }
}

// displayPlaces : Génère l'affichage HTML pour la liste des locations
// Param: places - Tableau des locations à afficher
function displayPlaces(places) {
  const container = document.getElementById('places-list');
  if (!container) return;
  container.innerHTML = '';
  places.forEach(place => {
    const div = document.createElement('div');
    div.className = 'place-card';
    div.innerHTML = `
      <h3>${place.title}</h3>
      <p>${place.description}</p>
      <p>Prix: ${place.price} €</p>
      <a href="place.html?id=${place.id}" class="details-button">View Details</a>
    `;
    container.appendChild(div);
  });
}

// filterPlacesByPrice : Filtre les locations selon le prix sélectionné
// Param: price - Le prix maximum sélectionné par l'utilisateur
function filterPlacesByPrice(price) {
  const places = window.allPlaces || [];
  const filtered = places.filter(place => {
    if (price === 'All') return true;
    return place.price <= parseInt(price);
  });
  displayPlaces(filtered);
}

// ======================================================================
// Fonctions spécifiques à la page de détails d'une location
// ======================================================================

// getPlaceIdFromURL : Extrait l'identifiant de la location depuis l'URL
// Retourne: L'ID de la location ou null si non trouvé
function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get('id');
}

// checkAuthAndFetchPlace : Vérifie l'authentification pour la page de détails
// Params: token - Token d'authentification, placeId - ID de la location
function checkAuthAndFetchPlace(token, placeId) {
  const addReviewSection = document.getElementById('add-review');
  // Si le token existe, afficher le formulaire d'ajout d'avis
  if (token) {
    if (addReviewSection) {
      addReviewSection.style.display = 'block';
    }
    fetchPlaceDetails(token, placeId);
  } else {
    // Sinon, masquer le formulaire d'avis
    if (addReviewSection) {
      addReviewSection.style.display = 'none';
    }
    console.log('❌ Aucun token trouvé, pas de formulaire d\'ajout d\'avis');
  }
}

// fetchPlaceDetails : Récupère les détails d'une location spécifique
// Params: token - Token d'authentification, placeId - ID de la location
async function fetchPlaceDetails(token, placeId) {
  try {
    const response = await fetch(`http://localhost:5000/places/${placeId}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    if (!response.ok) throw new Error('Erreur API: ' + response.statusText);
    const place = await response.json();
    displayPlaceDetails(place);
  } catch (err) {
    console.error('⛔ fetchPlaceDetails error:', err);
  }
}

// displayPlaceDetails : Affiche les détails d'une location
// Param: place - Objet contenant les informations de la location
// Met à jour tous les éléments de la page avec les données reçues
function displayPlaceDetails(place) {
  // Partie 1 : Mise à jour des éléments HTML par ID
  const titleEl = document.getElementById('place-title');
  const locationEl = document.getElementById('place-location');
  const imageEl = document.getElementById('place-image');
  const hostNameEl = document.getElementById('host-name');
  const hostImageEl = document.getElementById('host-image');
  const priceEl = document.getElementById('place-price');
  const capacityEl = document.getElementById('place-capacity');
  const descriptionEl = document.getElementById('place-description');
  const amenitiesContainer = document.getElementById('place-amenities');
  const reviewsContainer = document.getElementById('reviews-container');
  const addReviewLink = document.getElementById('add-review-link');

  if (titleEl) titleEl.textContent = place.title;
  if (locationEl) locationEl.textContent = place.location || '[Location]';
  if (imageEl) {
    imageEl.src = "/static/images/place2.jpg";
    imageEl.alt = place.title;
  }
  if (hostNameEl) hostNameEl.textContent = place.host_name || '[Host Name]';
  if (hostImageEl) hostImageEl.src = "/static/images/host.jpg";
  if (priceEl) priceEl.textContent = `$${place.price} per night`;
  if (capacityEl) capacityEl.textContent = `${place.guest_capacity || '?'} guests · ${place.bedrooms || '?'} bedrooms · ${place.bathrooms || '?'} bathrooms`;
  if (descriptionEl) descriptionEl.textContent = place.description;

  if (amenitiesContainer) {
    amenitiesContainer.innerHTML = '';
    place.amenities.forEach(am => {
      const li = document.createElement('li');
      li.textContent = am.name || am;
      amenitiesContainer.appendChild(li);
    });
  }

  if (reviewsContainer) {
    reviewsContainer.innerHTML = '';
    if (place.reviews && place.reviews.length > 0) {
      place.reviews.forEach(r => {
        const review = document.createElement('article');
        review.className = 'review-card';
        review.innerHTML = `
          <div class="review-header">
            <img src="/static/images/user1.jpg" alt="${r.user.first_name}" class="user-image">
            <div class="review-meta">
              <h3>${r.user.first_name} ${r.user.last_name}</h3>
              <div class="rating">${'★'.repeat(r.rating)}${'☆'.repeat(5 - r.rating)}</div>
              <p class="review-date">${r.date || 'N/A'}</p>
            </div>
          </div>
          <p class="review-text">${r.text}</p>
        `;
        reviewsContainer.appendChild(review);
      });
    } else {
      reviewsContainer.innerHTML = '<p>No reviews yet.</p>';
    }
  }

  if (addReviewLink) {
    addReviewLink.href = `add_review.html?id=${place.id}`;
  }
}