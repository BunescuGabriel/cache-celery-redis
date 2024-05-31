function incrementCount(button) {
    const counterContainer = button.parentElement;
    const counterValueElement = counterContainer.querySelector('.counter-value');
    let currentValue = parseInt(counterValueElement.textContent);
    counterValueElement.textContent = currentValue + 1;
    updateTotalAndCount();
}

function decrementCount(button) {
    const counterContainer = button.parentElement;
    const counterValueElement = counterContainer.querySelector('.counter-value');
    let currentValue = parseInt(counterValueElement.textContent);
    if (currentValue > 0) {
        counterValueElement.textContent = currentValue - 1;
    }
    updateTotalAndCount();
}



function toggleSelectAllItems() {
    const checkboxes = document.querySelectorAll('.item-checkbox');
    const selectAllButton = document.querySelector('.select-all');
    let allChecked = true;
    let atLeastOneChecked = false;

    checkboxes.forEach(checkbox => {
        if (!checkbox.checked) {
            allChecked = false;
        } else {
            atLeastOneChecked = true;
        }
    });

    checkboxes.forEach(checkbox => {
        checkbox.checked = !atLeastOneChecked;
    });

    if (atLeastOneChecked) {
        selectAllButton.classList.remove('active');
    } else {
        selectAllButton.classList.add('active');
        checkboxes.forEach(checkbox => {
            checkbox.checked = true;
        });
    }

    updateTotalAndCount();
}

function updateTotalAndCount() {
    const checkboxes = document.querySelectorAll('.item-checkbox');
    let total = 0;
    let count = 0;
    const conversionRate = 19.07;

    checkboxes.forEach(checkbox => {
        if (checkbox.checked) {
            const item = checkbox.closest('.item');
            const priceElement = item.querySelector('.item-price');
            const counterValueElement = item.querySelector('.counter-value');
            const price = parseFloat(priceElement.textContent.replace('Price: ', '').replace(' €', ''));
            const quantity = parseInt(counterValueElement.textContent);
            total += price * quantity;
            count += 1;

            checkbox.dataset.totalPrice = (price * quantity).toFixed(2);
        }
    });

    document.getElementById('total-price').textContent = total.toFixed(2);
    document.getElementById('total-price-lei').textContent = (total * conversionRate).toFixed(2);
    document.getElementById('checkout-button').textContent = `Checkout (${count})`;
}

function checkout() {
    const checkboxes = document.querySelectorAll('.item-checkbox:checked');
    const selectedItems = Array.from(checkboxes).map(checkbox => ({
        totalPrice: checkbox.dataset.totalPrice,
        itemId: checkbox.dataset.itemId,
         
    }));

    fetch('/checkout/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: JSON.stringify({ selected_items: selectedItems })
    })
    .then(response => {
        if (response.ok) {
            window.location.href = '/success/';
        } else {
            alert('A intervenit o eroare. Plata nu a putut fi efectuată.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('A intervenit o eroare. Plata nu a putut fi efectuată.');
    });
}

