const navSelect = document.querySelector('.nav-select');

navSelect.addEventListener('change', function() {
    const selectedValue = navSelect.value;
    if (selectedValue) {
        window.location.href = selectedValue;
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const select = document.getElementById('mySelect');
    const customSelect = document.createElement('div');
    customSelect.className = 'select-selected';
    customSelect.innerHTML = select.options[select.selectedIndex].innerHTML;
    select.parentNode.insertBefore(customSelect, select);
    
    const selectItems = document.createElement('div');
    selectItems.className = 'select-items select-hide';
    
    for (let i = 1; i < select.options.length; i++) {
        const item = document.createElement('div');
        item.innerHTML = select.options[i].innerHTML;
        item.addEventListener('click', function() {
            customSelect.innerHTML = this.innerHTML;
            select.selectedIndex = i;
            selectItems.classList.add('select-hide');
        });
        selectItems.appendChild(item);
    }
    
    customSelect.addEventListener('click', function() {
        selectItems.classList.toggle('select-hide');
    });
    
    document.body.appendChild(selectItems);
    
    document.addEventListener('click', function(e) {
        if (!customSelect.contains(e.target)) {
            selectItems.classList.add('select-hide');
        }
    });
}); 

document.addEventListener('DOMContentLoaded', function() {
    const select = document.getElementById('mySelect');

    select.addEventListener('change', function() {
        const selectedValue = select.value;
        console.log('Selected value:', selectedValue); // Ellenőrizzük a kiválasztott értéket

        if (selectedValue) {
            const targetElement = document.querySelector(selectedValue);
            if (targetElement) {
                targetElement.scrollIntoView({ behavior: 'smooth' });
                console.log('Görgetés sikeres:', targetElement); // Ellenőrizzük, hogy a megfelelő elem van-e kiválasztva
            } else {
                console.error('Hiba: Nem található az elem az azonosítóval:', selectedValue);
            }
        }
    });
});