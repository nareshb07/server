document.addEventListener('DOMContentLoaded', (event) => {
const searchInput = document.getElementById('searchInput');
const searchResults = document.getElementById('searchResults');
let timeoutId;

searchInput.addEventListener('input', function() {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => {
        const searchTerm = searchInput.value;
        
        if (searchTerm.trim() !== '') {
            fetchSearchResults(searchTerm);
        } else {
            searchResults.innerHTML = '';
        }
    }, 100);
});


function fetchSearchResults(searchTerm) {
    const url = '/search/?search=' + encodeURIComponent(searchTerm);
    fetch(url)
        .then(response => response.json())
        
        .then(data => {
            let searchResultsHTML = '';
            if (data.length > 0) {
                
                data.forEach(result => {
                    const imageUrl = result.image_url;
                    
                    searchResultsHTML += ` <a href="/${result.username}">
                                                <li class=" px-4 py-4 rounded-2xl text-[#00002E] hover:text-[#ade8f4] bg-inherit text-center hover:bg-[#ade8f4]">
                                                <div class="flex flex-row items-center ">
                                                    <img src="${imageUrl}" class="object-cover ml-5 h-14 w-14 flex-none rounded-full bg-black" />
                                                    <div class="ml-5 text-start ">
                                                    <div class="flex flex-row">
                                                    <p class=" flex-none"><b class=" font-bold">${result.first_name}</b> @${result.username}</p>
                                                    </div>
                                                    ${result.profession ? `<h1 class = "font-semibold">${result.profession}</h1>`  : ''}
                                                </div>
                                                </div>
                                                </li>
                                                </a>`;
                                            });
      
                                  searchResultsHTML += '</ul>';
                                   } else {
                                  searchResultsHTML = '<p class = "text-[#00002E] text-2xl mt-10 font-semibold">No users found.</p>';
                                  }

                                   searchResults.innerHTML = searchResultsHTML;
                                  })
                                    .catch(error => {
                                  console.error('Error:', error);
                                      });
                                 }
});