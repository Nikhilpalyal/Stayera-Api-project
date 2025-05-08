document.addEventListener('DOMContentLoaded', function() {
    const slider = document.getElementById('destinationSlider');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const cardWidth = 295; 
    
    prevBtn.addEventListener('click', function() {
        slider.scrollLeft -= cardWidth * 3;
    });
    
    nextBtn.addEventListener('click', function() {
        slider.scrollLeft += cardWidth * 3;
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const slider = document.getElementById('destinationsSlider');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const cardWidth = 300; // card width + margin
    
    prevBtn.addEventListener('click', function() {
        slider.scrollLeft -= cardWidth * 3;
    });
    
    nextBtn.addEventListener('click', function() {
        slider.scrollLeft += cardWidth * 3;
    });
});