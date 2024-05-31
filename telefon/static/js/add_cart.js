function addToCart(phoneId, button) {
    const quantity = parseInt(button.getAttribute('data-quantity'));

    if (quantity > 0) {
        fetch(`/add_to_cart/${phoneId}/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            alert('Telefon adăugat în coș!');
        })
        .catch(error => {
            console.error('Error:', error);
        });
    } else {
        alert('Cantitatea trebuie să fie mai mare decât 0!');
    }
}