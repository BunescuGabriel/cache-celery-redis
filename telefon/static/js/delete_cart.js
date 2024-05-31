

function deleteToCart(phoneId, button) {
    const itemToRemove = button.closest('.item');

    fetch(`/remove_from_cart/${phoneId}/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => {
        if (response.ok) {
            itemToRemove.remove();
            alert('Telefonul a fost eliminat din coș!');
            updateTotalAndCount();
        } else {
            alert('A intervenit o eroare. Telefoanele din coș nu au putut fi actualizate.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('A intervenit o eroare. Telefoanele din coș nu au putut fi actualizate.');
    });
}