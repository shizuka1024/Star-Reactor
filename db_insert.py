import mysql.connector
from mysql.connector import Error

def upload_to_sql(user_name, time):
    try:
        # Connect to the MySQL/MariaDB database
        connection = mysql.connector.connect(
            host='172.20.10.2',
            port=3306,        # Hostname
            database='gamedb', # Database name
            user='pi',        # Username
            password='pi'     # Password
        )

        sql = "INSERT INTO ranking(user_name, time) VALUES (%s, %s);"
        new_data = (user_name, time)
        cursor = connection.cursor()
        cursor.execute(sql, new_data)
        connection.commit()
        print("Data uploaded successfully")

    except Error as e:
        print("Failed to connect to the database:", e)

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("Database connection closed")

# Example usage
if __name__ == "__main__":
    user_name = "test"
    time = "29.16"
    upload_to_sql(user_name, time)

