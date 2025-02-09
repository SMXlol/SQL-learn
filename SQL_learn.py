import sqlite3

conn = sqlite3.connect("trips.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS trips (
    id INTEGER PRIMARY KEY,
    duration INTEGER,
    start_date TEXT,
    start_station INTEGER,
    end_date TEXT,
    end_station INTEGER,
    bike_number TEXT,
    sub_type TEXT,
    zip_code TEXT,
    birth_date INTEGER,
    gender TEXT
)
''')

trips_data = [
    (1, 300, "2024-02-09 08:00:00", 101, "2024-02-09 08:05:00", 102, "B123", "Зарегистрированный", "12345", 1985, "Мужчина"),
    (2, 1500, "2024-02-09 09:00:00", 103, "2024-02-09 09:25:00", 104, "B124", "Случайный", None, 1992, "Женщина"),
    (3, 600, "2024-02-09 10:00:00", 101, "2024-02-09 10:10:00", 105, "B125", "Зарегистрированный", "54321", 1990, "Женщина"),
    (4, 3600, "2024-02-09 11:00:00", 102, "2024-02-09 12:00:00", 103, "B123", "Зарегистрированный", "67890", 1980, "Мужчина"),
    (5, 900, "2024-02-09 12:30:00", 104, "2024-02-09 12:45:00", 105, "B126", "Случайный", None, 1995, "Мужчина"),
    (6, 2400, "2024-02-09 14:00:00", 105, "2024-02-09 14:40:00", 101, "B127", "Зарегистрированный", "24680", 1975, "Женщина")
]

cursor.executemany("INSERT INTO trips VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", trips_data)
conn.commit()

cursor.execute("SELECT MAX(duration) FROM trips")
longest_trip = cursor.fetchone()[0]
print("Самое длительное путешествие (в секундах):", longest_trip)

cursor.execute("SELECT COUNT(*) FROM trips WHERE sub_type = 'Зарегистрированный'")
registered_trips = cursor.fetchone()[0]
print("Количество поездок зарегистрированных пользователей:", registered_trips)

cursor.execute("SELECT AVG(duration) FROM trips")
avg_duration = cursor.fetchone()[0]
print("Средняя продолжительность поездки (в секундах):", avg_duration)

cursor.execute("SELECT AVG(duration) FROM trips WHERE sub_type = 'Зарегистрированный'")
avg_registered = cursor.fetchone()[0]
cursor.execute("SELECT AVG(duration) FROM trips WHERE sub_type = 'Случайный'")
avg_guest = cursor.fetchone()[0]
print("Средняя продолжительность поездки (зарегистрированные):", avg_registered)
print("Средняя продолжительность поездки (гости):", avg_guest)
if avg_registered > avg_guest:
    print("Зарегистрированные пользователи совершают более длительные поездки.")
else:
    print("Гости совершают более длительные поездки.")

cursor.execute("SELECT bike_number, COUNT(*) as count FROM trips GROUP BY bike_number ORDER BY count DESC LIMIT 1")
most_used_bike = cursor.fetchone()
print("Самый используемый велосипед:", most_used_bike[0])

cursor.execute("SELECT AVG(duration) FROM trips WHERE birth_date IS NOT NULL AND (strftime('%Y', 'now') - birth_date) > 30")
avg_duration_over_30 = cursor.fetchone()[0]
print("Средняя продолжительность поездок пользователей старше 30 лет (в секундах):", avg_duration_over_30)

conn.close()
