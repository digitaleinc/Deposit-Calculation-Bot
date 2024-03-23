from config import cursor, connection


# DB
def create_calculation(user_id, calc_id, f_dep, r_per, m_quan):
    cursor.execute(
        'INSERT INTO calculations (user_id, calc_id, first_deposit, real_percentage, months_quantity) VALUES (''?, ?, ?, ?, ?)',
        (user_id, calc_id, f_dep, r_per, m_quan))
    connection.commit()


def get_calculation(calc_id):
    cursor.execute(f"SELECT first_deposit FROM calculations WHERE calc_id = {calc_id}")
    f_dep = cursor.fetchone()

    cursor.execute(f"SELECT real_percentage FROM calculations WHERE calc_id = {calc_id}")
    r_per = cursor.fetchone()

    cursor.execute(f"SELECT months_quantity FROM calculations WHERE calc_id = {calc_id}")
    m_quan = cursor.fetchone()

    cursor.execute(f"SELECT monthly_payment FROM calculations WHERE calc_id = {calc_id}")
    m_payment = cursor.fetchone()

    cursor.execute(f"SELECT monthly_amount FROM calculations WHERE calc_id = {calc_id}")
    m_amount = cursor.fetchone()

    return f_dep[0], r_per[0], m_quan[0], m_payment[0], m_amount[0]


def set_regular_payment_yes(calc_id):
    cursor.execute('UPDATE calculations SET monthly_payment = ? WHERE calc_id = ?', (1, calc_id))
    connection.commit()


def set_regular_payment_no(calc_id):
    cursor.execute('UPDATE calculations SET monthly_payment = ? WHERE calc_id = ?', (0, calc_id))
    connection.commit()


def set_regular_payment_amount(calc_id, m_amount):
    cursor.execute('UPDATE calculations SET monthly_amount = ? WHERE calc_id = ?', (m_amount, calc_id))
    connection.commit()
