Dropzone.autoDiscover = false;

const myDropzone = new Dropzone("#myDropzone", {
    url: "/upload",
    paramName: "file", 
    maxFiles: 3,
    acceptedFiles: ".jpg,.jpeg,.png,.pdf,.txt",
    addRemoveLinks: true,
    init: function() {
        this.on("success", function(file, response) {
            displayOCRResult(response.ocr_text);
            displaySuggestions(response.suggestions);
        });

        this.on("error", function(file, errorMessage) {
            alert("Error during file upload: " + errorMessage);
        });
    }
});

// Function to display OCR text result
function displayOCRResult(ocrText) {
    const ocrResultContainer = document.getElementById("ocr-result");
    const ocrTextElement = document.getElementById("ocr-text");

    if (ocrText) {
        ocrTextElement.innerHTML = ocrText;
        ocrResultContainer.style.display = "block";
    } else {
        ocrTextElement.innerHTML = "No text detected, please try another file.";
        ocrResultContainer.style.display = "block";
    }
}

// Function to display analysis suggestions with interactive animations
function displaySuggestions(suggestions) {
    const suggestionsContainer = document.getElementById("suggestions");
    suggestionsContainer.innerHTML = ""; // Clear previous suggestions
    
    // Split the suggestions into individual items and create HTML for each
    const suggestionItems = suggestions.split("\n\n").map(suggestion => {
        const suggestionDiv = document.createElement("div");
        suggestionDiv.classList.add("suggestion-item");
        
        // Add a dynamic class for animation
        setTimeout(() => {
            suggestionDiv.classList.add("visible");
        }, 100);

        // Parse each suggestion and add corresponding content
        // <p><span class="emoji">✨</span></p>
        suggestionDiv.innerHTML = `
            
            <p>${suggestion}</p>
        `;
        return suggestionDiv;
    });

    // Append each suggestion to the container
    suggestionItems.forEach(item => suggestionsContainer.appendChild(item));
    document.getElementById("analysis-result").style.display = "block";
}
