    // script.js

    const titles = [
        "ETS BIG-TRANSPORT",
        "BTP BIG-TRANSPORT",
        "EXPERT TEAM AT YOUR SERVICE",
    ];

    const texts = [
        "Specialement dans la fourniture de materiaux essentiels pour vos projet de construction, nous vous offrons une gamme de produits de haute qualite",
        "En outre dans les activites de construction, demolition, locations de Betonniere, Niveleuse, Chargeur, Bull, Pelle Hydraulique,...",
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus lacinia odio vitae vestibulum.",
    ];

    let currentIndex = 0;

    const titleElement = document.getElementById('sectionTitle');
    const textElement = document.getElementById('sectionText');

    function updateContent() {
        titleElement.textContent = titles[currentIndex];
        textElement.textContent = texts[currentIndex];
    }

    // Fonction pour aller à l'image/texte précédent
    document.getElementById('prevBtn').addEventListener('click', () => {
        currentIndex = (currentIndex - 1 + titles.length) % titles.length; // Utilisation du modulo pour faire une boucle
        updateContent();
    });

    // Fonction pour aller à l'image/texte suivant
    document.getElementById('nextBtn').addEventListener('click', () => {
        currentIndex = (currentIndex + 1) % titles.length; // Utilisation du modulo pour faire une boucle
        updateContent();
    });

    // Initialiser le contenu
    updateContent();