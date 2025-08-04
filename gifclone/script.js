const API_KEY = 'SUA_CHAVE_DE_API_AQUI'; // Substitua pela sua chave de API
const searchInput = document.getElementById('search-input');
const searchButton = document.getElementById('search-button');
const gifResultsContainer = document.getElementById('gif-results');
const trendingResultsContainer = document.getElementById('trending-results');

// Função para buscar e exibir GIFs
async function fetchGifs(query) {
    let url = '';
    if (query) {
        url = `https://api.giphy.com/v1/gifs/search?api_key=${API_KEY}&q=${query}&limit=25&rating=g`;
    } else {
        url = `https://api.giphy.com/v1/gifs/trending?api_key=${API_KEY}&limit=25&rating=g`;
    }

    try {
        const response = await fetch(url);
        const data = await response.json();
        return data.data;
    } catch (error) {
        console.error('Erro ao buscar GIFs:', error);
    }
}

// Função para renderizar os GIFs na tela
function renderGifs(gifs, container) {
    container.innerHTML = '';
    gifs.forEach(gif => {
        const gifContainer = document.createElement('div');
        gifContainer.classList.add('gif-container');

        const img = document.createElement('img');
        img.src = gif.images.fixed_height.url;
        img.alt = gif.title;

        gifContainer.appendChild(img);
        container.appendChild(gifContainer);
    });
}

// Evento de clique no botão de pesquisa
searchButton.addEventListener('click', async () => {
    const query = searchInput.value.trim();
    if (query) {
        const gifs = await fetchGifs(query);
        renderGifs(gifs, gifResultsContainer);
        // Oculta os trending GIFs ao fazer uma pesquisa
        document.getElementById('trending-gifs').style.display = 'none'; 
    }
});

// Carregar GIFs em alta ao carregar a página
document.addEventListener('DOMContentLoaded', async () => {
    const trendingGifs = await fetchGifs();
    renderGifs(trendingGifs, trendingResultsContainer);
});