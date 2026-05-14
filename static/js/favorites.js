document.addEventListener('DOMContentLoaded', function() {
    const favButtons = document.querySelectorAll('.project-fav-icon');
    
    favButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const projectId = this.dataset.projectId;
            
            fetch(`/toggle-favorite/${projectId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({})
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'ok') {
                    if (data.is_favorite) {
                        this.classList.remove('not-favorite');
                        this.classList.add('favorite');
                        this.dataset.fav = 'true';
                    } else {
                        this.classList.remove('favorite');
                        this.classList.add('not-favorite');
                        this.dataset.fav = 'false';
                    }
                }
            })
            .catch(error => console.error('Ошибка:', error));
        });
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
