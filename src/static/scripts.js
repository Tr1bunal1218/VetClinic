function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null; // Возвращаем null, если куки не найдено
}

async function login() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const response = await fetch('http://127.0.0.1:8001/users/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
    });

    const data = await response.json();

    if (data.status === "ok") {
        const token = getCookie('acsess_token');
        if (token) {
            document.getElementById('auth-form').style.display = 'none';
            document.getElementById('booking-form').style.display = 'block';
            document.getElementById('schedule-form').style.display = 'block';
        } else {
            alert('Ошибка: токен не найден в куках');
        }
    } else {
        alert('Ошибка входа: ' + (data.message || 'Неизвестная ошибка'));
    }
}

async function addBooking() {
    try {
        const clinicId = 2;
        const doctorId = parseInt(document.getElementById('doctor-select').value);
        const petId = parseInt(document.getElementById('pet-select').value);
        const bookingTime = document.getElementById('booking-time').value.trim();
        const token = getCookie('access_token');

        // Валидация
        if (isNaN(doctorId)) {
            alert('Пожалуйста, выберите врача');
            return;
        }
        
        if (isNaN(petId)) {
            alert('Пожалуйста, выберите питомца');
            return;
        }

        const requestBody = {
            clinic_id: clinicId,
            doctor_id: doctorId,
            pet_id: petId, // Добавили ID питомца
            ...(bookingTime && { booking_time: bookingTime })
        };

        const response = await fetch(`http://127.0.0.1:8001/clinic/${clinicId}/doctors/${doctorId}/bookings/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`,
            },
            body: JSON.stringify(requestBody),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Ошибка сервера');
        }

        const data = await response.json();
        
        if (data.success) {
            alert('Запись успешно добавлена!');
            // Сброс формы
            doctorSelect.value = '';
            bookingTimeInput.value = '';
        }
    } catch (error) {
        console.error('Ошибка:', error);
        alert(`Ошибка записи: ${error.message}`);
    }
}

async function updateSchedule(scheduleId, doctorId, clinicId) {
    const dialog = document.createElement('dialog');
    dialog.innerHTML = `
        <form id="update-form">
            <label>Начало:
                <input type="datetime-local" id="update-start" required>
            </label>
            <label>Конец:
                <input type="datetime-local" id="update-end" required>
            </label>
            <button type="submit">Обновить</button>
            <button type="button" onclick="dialog.close()">Отмена</button>
        </form>
    `;
    document.body.appendChild(dialog);
    dialog.showModal();

    document.getElementById('update-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const token = localStorage.getItem('token');
        const startInput = document.getElementById('update-start').value;
        const endInput = document.getElementById('update-end').value;

        // Конвертируем в нужный формат "YYYY-MM-DD HH:mm:ss"
        const formatDateTime = (input) => {
            const date = new Date(input);
            return [
                date.getFullYear(),
                String(date.getMonth() + 1).padStart(2, '0'),
                String(date.getDate()).padStart(2, '0'),
            ].join('-') + ' ' + [
                String(date.getHours()).padStart(2, '0'),
                String(date.getMinutes()).padStart(2, '0'),
                '00'
            ].join(':');
        };

        try {
            const response = await fetch(
                `http://127.0.0.1:8001/clinic/${clinicId}/doctors/${doctorId}/schedules/${scheduleId}`, 
                {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`,
                    },
                    body: JSON.stringify({
                        start_time: formatDateTime(startInput),
                        end_time: formatDateTime(endInput)
                    })
                }
            );

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Ошибка обновления');
            }

            alert('Расписание обновлено!');
            dialog.close();
            displaySchedules(await fetchSchedules());
            
        } catch (error) {
            alert(error.message);
        }
    });
}

async function loadDoctors() {
    const response = await fetch(`http://127.0.0.1:8001/clinic/{clinic_id}/doctors`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
        credentials: 'include'
    });
    const doctors = await response.json();
    const doctorSelect = document.getElementById('doctor-select');
    doctors.forEach(doctor => {
        const option = document.createElement('option');
        option.value = doctor.id;
        option.textContent = `${doctor.first_name} ${doctor.last_name}`;
        doctorSelect.appendChild(option);
    });
}

document.addEventListener('DOMContentLoaded', async () => {
    await loadDoctors();
    await loadPets();
});

async function loadPets() {
    try {
        const token = getCookie('access_token');
        const response = await fetch('http://127.0.0.1:8001/pets', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) throw new Error('Ошибка загрузки питомцев');
        
        const pets = await response.json();
        const petSelect = document.getElementById('pet-select');
        
        // Очищаем и заполняем список
        petSelect.innerHTML = '<option value="" disabled selected>Выберите питомца</option>';
        
        pets.forEach(pet => {
            const option = document.createElement('option');
            option.value = pet.id;
            option.textContent = `${pet.name} (${pet.vid})`;
            petSelect.appendChild(option);
        });
        
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Не удалось загрузить список питомцев');
    }
}

async function checkUserRole() {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = '/login.html';
        return;
    }

    const response = await fetch('http://127.0.0.1:8001/users/me', {
        headers: { 'Authorization': `Bearer ${token}` }
    });
    const user = await response.json();

    if (user.role === 'admin') {
        document.getElementById('admin-panel').style.display = 'block';
    }
}

async function loadSchedules() {
    // const doctorId = document.getElementById('search-doctor-id').value;
    const clinicId = 1; // Предполагаем фиксированную клинику
    const token = localStorage.getItem('token');

    const response = await fetch(`http://127.0.0.1:8001/clinic/{clinic_id}/doctors/{doctor_id}/schedule`, {
        headers: { 'Authorization': `Bearer ${token}` }
    });
    
    const schedules = await response.json();
    displaySchedules(schedules);
}

async function displaySchedules(schedules) {
    const container = document.getElementById('schedules-list');
    
    // Получаем данные врачей параллельно
    const enrichedSchedules = await Promise.all(
        schedules.map(async schedule => {
            try {
                const clinicId = 1; // Убедитесь, что clinicId установлен правильно
                const response = await fetch(`http://127.0.0.1:8001/clinic/clinic_id/doctors/${schedule.doctor_id}`);
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const doctors = await response.json();
                const doctor = doctors.length > 0 ? doctors[0] : null;
                const doctorName = `${doctor.first_name} ${doctor.last_name}`;
                return {
                    ...schedule,
                    doctorName: doctorName || `Неизвестный врач (ID: ${schedule.doctor_id})`
                };
            } catch (error) {
                return {
                    ...schedule,
                    doctorName: `Ошибка загрузки (ID: ${schedule.doctor_id})`
                };
            }
        })
    );

    container.innerHTML = `
        <table class="schedule-table">
            <tr>
                <th>Клиника ID</th>
                <th>Врач</th>
                <th>Начало</th>
                <th>Конец</th>
                <th>ID расписания</th>
                <th>Действия</th>
            </tr>
            ${enrichedSchedules.map(schedule => `
                <tr>
                    <td>${schedule.clinic_id}</td>
                    <td>${schedule.doctorName}</td>
                    <td>${new Date(schedule.start_time).toLocaleString()}</td>
                    <td>${new Date(schedule.end_time).toLocaleString()}</td>
                    <td>${schedule.id}</td>
                    <td>
                        <button onclick="deleteSchedule(${schedule.id}, ${schedule.doctor_id}, ${schedule.clinic_id})">
                            Удалить
                        </button>
                        <button onclick="updateSchedule(${schedule.id}, ${schedule.doctor_id}, ${schedule.clinic_id})" 
                                style="margin-left: 8px;">
                            Обновить
                        </button>
                    </td>
                </tr>
            `).join('')}
        </table>
    `;
}
async function deleteSchedule(scheduleId, doctorId) {
    const clinicId = 1;
    const token = localStorage.getItem('token');
    const confirmDelete = confirm('Вы уверены, что хотите удалить расписание?');
    
    if (!confirmDelete) return;

    const response = await fetch(
        `http://127.0.0.1:8001/clinic/{clinic_id}/schedules/${scheduleId}`,
        {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${token}` }
        }
    );

    const result = await response.json();
    if (result.status === 'success') {
        alert('Расписание удалено!');
        loadSchedules(); // Обновляем список
    } else {
        alert('Ошибка: ' + result.message);
    }
}

window.onload = checkUserRole;