const express = require('express');
const bodyParser = require('body-parser');
const { Pool } = require('pg');

const app = express();
const port = 3000;

// Настройка подключения к базе данных PostgreSQL
const pool = new Pool({
    host: 'postgres', // Имя сервиса из docker-compose
    user: 'myuser', // Имя пользователя
    password: 'mysecretpassword', // Пароль
    database: 'mydatabase', // Имя базы данных
    port: 5432, // Порт
});

// Middleware для обработки данных формы
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

// Обработка POST-запроса для входа
app.post('/login', async (req, res) => {
    const { email, password } = req.body;

    try {
        // Используйте хэширование паролей в реальном приложении
        const query = 'SELECT * FROM users WHERE email = $1 AND password = $2';
        const result = await pool.query(query, [email, password]);

        if (result.rows.length > 0) {
            // Успешный вход
            res.send('Успешный вход!');
        } else {
            // Неверные учетные данные
            res.status(401).send('Неверные учетные данные');
        }
    } catch (err) {
        console.error(err);
        res.status(500).send('Ошибка сервера');
    }
});

// Запуск сервера
app.listen(port, () => {
    console.log(`Сервер запущен на http://localhost:${port}`);
});