document.addEventListener('DOMContentLoaded', function () {
    const inputs = document.querySelectorAll('input, select');
    const checks = document.querySelectorAll('.check-icon');
    const progressBar = document.getElementById('progress-bar');
    const completionText = document.getElementById('completion-text');

    function updateProgress() {
        let filled = 0;
        inputs.forEach((input, index) => {
            if (input.value.trim() !== '') {
                filled++;
                checks[index].style.color = 'green';
                checks[index].style.visibility = 'visible';
            } else {
                checks[index].style.visibility = 'hidden';
            }
        });

        let percent = Math.round((filled / inputs.length) * 100);
        progressBar.style.width = percent + '%';
        completionText.innerText = percent + '%';
    }

    inputs.forEach(input => {
        input.addEventListener('input', updateProgress);
    });

    updateProgress(); // initial update
});