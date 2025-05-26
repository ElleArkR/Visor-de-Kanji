document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('search-input');
    const searchButton = document.getElementById('search-button');
    const resultsSection = document.getElementById('results-section');

    searchButton.addEventListener('click', performSearch);
    searchInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            performSearch();
        }
    });

    async function performSearch() {
        const query = searchInput.value.trim();
        if (!query) {
            resultsSection.innerHTML = '<p>Por favor, introduce un término de búsqueda.</p>';
            return;
        }

        resultsSection.innerHTML = '<p>Buscando...</p>'; // Correctly "Buscando..." or "Procesando..."

        let apiUrl;
        // Basic check for single Japanese/Chinese character (this can be improved)
        // CJK Unified Ideographs Unicode block starts from U+4E00
        if (query.length === 1 && query.charCodeAt(0) >= 0x4E00) {
            apiUrl = `/api/kanji/${encodeURIComponent(query)}`;
        } else {
            apiUrl = `/api/search/kanji?query=${encodeURIComponent(query)}`;
        }

        try {
            const response = await fetch(apiUrl);
            if (!response.ok) {
                if (response.status === 404 && apiUrl.includes('/api/kanji/')) {
                    // Try search endpoint as a fallback if specific kanji not found
                    apiUrl = `/api/search/kanji?query=${encodeURIComponent(query)}`;
                    const searchResponse = await fetch(apiUrl);
                    if (!searchResponse.ok) {
                        throw new Error(`Error en la búsqueda: ${searchResponse.status} ${searchResponse.statusText}`);
                    }
                    const data = await searchResponse.json();
                    displayResults(data, query); // Pass query for "no results" message
                } else {
                    const errorData = await response.json();
                    let errorMessage = errorData.error || `Error: ${response.status} ${response.statusText}`;
                    if (response.status === 404 && apiUrl.includes('/api/kanji/')) {
                        errorMessage = `Kanji '${query}' no encontrado.`;
                    }
                    throw new Error(errorMessage);
                }
            } else {
                const data = await response.json();
                displayResults(Array.isArray(data) ? data : [data], query);
            }
        } catch (error) {
            console.error('Error en la búsqueda:', error);
            resultsSection.innerHTML = `<p>Error al realizar la búsqueda: ${error.message}</p>`;
        }
    }

    function displayResults(data, query) {
        resultsSection.innerHTML = ''; 

        if (!data || data.length === 0 || (data.length === 1 && data[0] === null && !data[0]?.kanji_char) ) {
            resultsSection.innerHTML = `<p>No se encontraron resultados para "${query}".</p>`;
            return;
        }
        
        const validData = data.filter(item => item !== null && item.kanji_char);

        if (validData.length === 0) {
             resultsSection.innerHTML = `<p>No se encontraron resultados válidos para "${query}".</p>`;
             return;
        }

        validData.forEach(kanji => {
            if (!kanji || !kanji.kanji_char) return; 

            const kanjiDiv = document.createElement('div');
            kanjiDiv.className = 'kanji-info';

            const title = document.createElement('h2');
            // title.textContent = `Kanji: ${kanji.kanji_char}`; // Label "Kanji:" is implicit with h2
            title.textContent = kanji.kanji_char;
            kanjiDiv.appendChild(title);

            appendDetail(kanjiDiv, 'Unicode:', kanji.unicode);
            appendDetail(kanjiDiv, 'Trazos:', kanji.stroke_count);
            appendDetail(kanjiDiv, 'Grado:', kanji.grade !== null ? kanji.grade : 'N/A');
            appendDetail(kanjiDiv, 'JLPT:', kanji.jlpt_level !== null ? `N${kanji.jlpt_level}` : 'N/A');
            
            appendList(kanjiDiv, 'Significados:', kanji.meanings);
            appendList(kanjiDiv, 'Lecturas Kun\'yomi:', kanji.kun_readings); // Kun'yomi with apostrophe
            appendList(kanjiDiv, 'Lecturas On\'yomi:', kanji.on_readings);   // On'yomi with apostrophe

            if (kanji.svg_filename) {
                const svgContainer = document.createElement('div');
                svgContainer.className = 'kanji-svg-container';
                
                const svgImg = document.createElement('img');
                svgImg.src = `/data/svgs/${kanji.svg_filename}`;
                svgImg.alt = `Orden de trazos para ${kanji.kanji_char}`;
                svgImg.onerror = () => { 
                    svgContainer.innerHTML = '<p>Diagrama de trazos no disponible.</p>';
                };
                svgContainer.appendChild(svgImg);
                kanjiDiv.appendChild(svgContainer);
            }

            resultsSection.appendChild(kanjiDiv);
        });
    }

    function appendDetail(parent, label, value) {
        if (value !== undefined && value !== null) {
            const p = document.createElement('p');
            const strong = document.createElement('strong');
            strong.textContent = label + ' ';
            p.appendChild(strong);
            p.appendChild(document.createTextNode(value === 'N/A' ? 'No disponible' : value)); // Translate N/A
            parent.appendChild(p);
        }
    }

    function appendList(parent, label, listItems) {
        if (listItems && listItems.length > 0) {
            const p = document.createElement('p');
            // Creating a separate h3 for list labels as per prompt example
            const h3 = document.createElement('h3');
            h3.textContent = label;
            parent.appendChild(h3);
            
            const ul = document.createElement('ul');
            listItems.forEach(item => {
                const li = document.createElement('li');
                li.textContent = item;
                ul.appendChild(li);
            });
            parent.appendChild(ul);
        } else {
            // If no items, show label with "No disponible"
            const p = document.createElement('p');
            const strong = document.createElement('strong');
            strong.textContent = label + ' ';
            p.appendChild(strong);
            p.appendChild(document.createTextNode('No disponible'));
            parent.appendChild(p);
        }
    }
});
