document.addEventListener('DOMContentLoaded', function() {
    // Находим необходимые элементы
    const guestDisplay = document.getElementById('guest-display');
    const guestPopup = document.getElementById('guest-popup');
    const applyButton = document.getElementById('apply-guests');
  
    // Элементы для счётчиков в popup
    const popupGuestCountEl = document.getElementById('popup-guest-count');
    const popupChildrenCountEl = document.getElementById('popup-children-count');
  
    // Элементы для отображения выбранных значений в поле
    const guestCountEl = document.getElementById('guest-count');
    const childrenCountEl = document.getElementById('children-count');
  
    // Скрытые input'ы, созданные формой Django (id формируются автоматически)
    const inputGuest = document.getElementById('id_guests');
    const inputChildren = document.getElementById('id_children');
  
    // Начальные значения (они же установлены по умолчанию)
    let guestCount = parseInt(popupGuestCountEl.textContent); // начальное значение = 1
    let childrenCount = parseInt(popupChildrenCountEl.textContent); // начальное значение = 0
  
    // Открытие popup при клике на поле
    guestDisplay.addEventListener('click', function(e) {
      guestPopup.style.display = 'block';
    });
  
    // Функция обновления числовых значений
    function updateDisplay() {
      popupGuestCountEl.textContent = guestCount;
      popupChildrenCountEl.textContent = childrenCount;
    }
  
    // Обработчики для кнопок + и –
    document.querySelectorAll('.increment').forEach(function(button) {
      button.addEventListener('click', function() {
        const target = button.getAttribute('data-target');
        if (target === 'guest') {
          guestCount++;
        } else if (target === 'children') {
          childrenCount++;
        }
        updateDisplay();
      });
    });
  
    document.querySelectorAll('.decrement').forEach(function(button) {
      button.addEventListener('click', function() {
        const target = button.getAttribute('data-target');
        if (target === 'guest' && guestCount > 1) { // минимум 1 гость
          guestCount--;
        } else if (target === 'children' && childrenCount > 0) {
          childrenCount--;
        }
        updateDisplay();
      });
    });
  
    // Применение выбранных значений
    applyButton.addEventListener('click', function() {
      // Обновляем отображение в поле выбора
      guestCountEl.textContent = guestCount;
      childrenCountEl.textContent = childrenCount;
      // Обновляем скрытые input'ы формы для отправки
      inputGuest.value = guestCount;
      inputChildren.value = childrenCount;
      // Закрываем popup
      guestPopup.style.display = 'none';
    });
  
    // Дополнительно: закрытие popup при клике вне области
    document.addEventListener('click', function(e) {
      if (!e.target.closest('.guest-field') && !e.target.closest('#guest-popup')) {
        guestPopup.style.display = 'none';
      }
    });

    const guestField = document.getElementById("guest-field");

    // Получаем объект с размерами и координатами элемента
    const guestCoords = guestField.getBoundingClientRect();
    guestPopup.style.top = guestCoords.y;
    guestPopup.style.left = guestCoords.x;

  });
  