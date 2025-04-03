def login_user(email, password):
    # Connect to the database
    conn = mysql.connector.connect(host="localhost", user="root", password="", database="user_auth")
    cursor = conn.cursor()

    # Fetch user data
    query = "SELECT id, password FROM users WHERE email = %s"
    cursor.execute(query, (email,))
    user = cursor.fetchone()

    if user:
        user_id, hashed_password = user
        # Verify password
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            # Update last login
            update_query = "UPDATE users SET last_login = NOW() WHERE id = %s"
            cursor.execute(update_query, (user_id,))
            conn.commit()
            conn.close()
            return "Login successful"
        else:
            conn.close()
            return "Invalid password"
    else:
        conn.close()
        return "User not found"
