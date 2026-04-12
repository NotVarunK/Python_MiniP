import mysql.connector

DB_CONFIG = {
    "host":     "metro.proxy.rlwy.net",
    "user":     "root",
    "password": "dOUejIuaMGNpPtecvWJauGyGTDvyvTYX",   # change this to your MySQL password
    "database": "railway"
}

def get_conn():
    return mysql.connector.connect(**DB_CONFIG)

def is_slot_taken(doctor, day, slot):
    conn   = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM appointments WHERE doctor=%s AND day=%s AND slot=%s",
        (doctor, day, slot)
    )
    result = cursor.fetchone()
    conn.close()
    return result is not None   # True = already booked

def save_appointment(doctor, department, day, slot):
    conn   = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO appointments (doctor, department, day, slot) VALUES (%s, %s, %s, %s)",
        (doctor, department, day, slot)
    )
    conn.commit()
    conn.close()
