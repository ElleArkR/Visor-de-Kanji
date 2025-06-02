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

            const mainInfoWrapper = document.createElement('div');
            mainInfoWrapper.className = 'kanji-main-info-wrapper';
            kanjiDiv.appendChild(mainInfoWrapper);

            if (kanji.svg_filename) {
                const animationTargetDiv = document.createElement('div');
                animationTargetDiv.id = `hanzi-writer-target-${kanji.unicode}`; 
                animationTargetDiv.className = 'hanzi-writer-target'; 
                mainInfoWrapper.appendChild(animationTargetDiv); // Append SVG container to wrapper first
                
                loadAndAnimateSvg(kanji.svg_filename, animationTargetDiv, kanji.kanji_char);
            }

            const textDetailsContainer = document.createElement('div');
            textDetailsContainer.className = 'kanji-text-details-container';
            mainInfoWrapper.appendChild(textDetailsContainer); // Append text container to wrapper

            appendDetail(textDetailsContainer, 'Unicode:', kanji.unicode);
            appendDetail(textDetailsContainer, 'Trazos:', kanji.stroke_count);
            appendDetail(textDetailsContainer, 'Grado:', kanji.grade !== null ? kanji.grade : 'N/A');
            appendDetail(textDetailsContainer, 'JLPT:', kanji.jlpt_level !== null ? `N${kanji.jlpt_level}` : 'N/A');
            
            appendList(textDetailsContainer, 'Significados:', kanji.meanings);
            appendList(textDetailsContainer, 'Lecturas Kun\'yomi:', kanji.kun_readings);
            appendList(textDetailsContainer, 'Lecturas On\'yomi:', kanji.on_readings);

            // Display Example Words (remains appended to kanjiDiv, after mainInfoWrapper)
            if (kanji.example_words && kanji.example_words.length > 0) {
                const examplesContainer = document.createElement('div');
                examplesContainer.className = 'example-words-container';
                
                const examplesTitle = document.createElement('h3');
                examplesTitle.textContent = 'Palabras de Ejemplo:';
                examplesContainer.appendChild(examplesTitle);
                
                const examplesList = document.createElement('ul');
                examplesList.className = 'example-words-list';
                kanji.example_words.forEach(example_string => {
                    const listItem = document.createElement('li');
                    listItem.className = 'example-word-item';
                    
                    // Directamente usamos la cadena pre-formateada que viene del backend
                    listItem.textContent = example_string; 
                    // La información de JLPT para palabras de ejemplo no se está pasando actualmente
                    // en este formato, así que la lógica de ex.jlpt_level_word se omite por ahora.
                    
                    examplesList.appendChild(listItem);
                });
                examplesContainer.appendChild(examplesList);
                kanjiDiv.appendChild(examplesContainer);
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

    async function loadAndAnimateSvg(svgFilename, targetDiv, kanjiChar) {
        targetDiv.innerHTML = '<p>Cargando diagrama...</p>'; // Initial loading message

        try {
            const response = await fetch(`/data/svgs/${svgFilename}`);
            if (!response.ok) {
                throw new Error(`No se pudo cargar el archivo SVG: ${response.status} ${response.statusText}`);
            }
            const svgText = await response.text();

            targetDiv.innerHTML = ''; // Clear loading message

            const parser = new DOMParser();
            const svgDoc = parser.parseFromString(svgText, "image/svg+xml");
            const svgElement = svgDoc.documentElement;

            if (svgElement.nodeName === 'parsererror' || !svgElement.querySelector('path')) {
                console.error("Error parsing SVG or SVG has no paths:", svgText);
                targetDiv.innerHTML = '<p>Error al procesar el diagrama de trazos.</p>';
                return;
            }
            
            svgElement.setAttribute('width', '100%');
            svgElement.setAttribute('height', '100%');
            svgElement.removeAttribute('id'); 

            targetDiv.appendChild(svgElement);

            const paths = Array.from(svgElement.querySelectorAll('path'));
            
            // Prepare paths for animation (initial state)
            paths.forEach(path => {
                const length = path.getTotalLength();
                path.style.strokeDasharray = length;
                path.style.strokeDashoffset = length;
                path.style.stroke = '#000000';
                path.style.strokeWidth = '3';
                path.style.fill = 'none';
                path.style.transition = 'none'; 
            });

            async function animateAllPathsSequentially() {
                for (const path of paths) {
                    const length = path.getTotalLength();
                    // Ensure path is reset before animating if it's not the first loop
                    // This is mostly handled by the initial setup now.
                    // path.style.strokeDashoffset = length; // Reset for re-animation

                    const animation = path.animate([
                        { strokeDashoffset: length },
                        { strokeDashoffset: 0 }
                    ], {
                        duration: 800, 
                        easing: 'linear',
                        fill: 'forwards'
                    });
                    await animation.finished;
                    await new Promise(resolve => setTimeout(resolve, 150)); 
                }

                // Add a delay before restarting the loop
                await new Promise(resolve => setTimeout(resolve, 1000)); // 1 second delay before loop

                // Reset all paths to their initial state for the loop
                paths.forEach(path => {
                    const length = path.getTotalLength();
                    path.style.strokeDashoffset = length;
                });
                
                // Loop the animation
                animateAllPathsSequentially(); 
            }

            // Start the animation loop
            animateAllPathsSequentially();

        } catch (error) {
            console.error(`Error al cargar o animar SVG para ${kanjiChar}:`, error);
            targetDiv.innerHTML = `<p>Diagrama de trazos no disponible para ${kanjiChar}.</p>`;
        }
    }
});
