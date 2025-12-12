import os
import pymysql

class Database:

    def connect(self):
        return pymysql.connect(
            host=os.environ.get("DB_HOST", "localhost"),
            user=os.environ.get("DB_USER", "dev"),
            password=os.environ.get("DB_PASSWORD", "dev"),
            database=os.environ.get("DB_NAME", "crud_flask"),
            charset='utf8mb4'
        )

    def read(self, id):
        con = self.connect()
        cursor = con.cursor()
        try:
            if id is None:
                cursor.execute("SELECT * FROM phone_book ORDER BY name ASC")
            else:
                cursor.execute(
                    "SELECT * FROM phone_book WHERE id = %s ORDER BY name ASC", (id,)
                )
            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()

    def insert(self, data):
        con = self.connect()
        cursor = con.cursor()
        try:
            cursor.execute(
                "INSERT INTO phone_book(name, phone, address) VALUES(%s, %s, %s)",
                (data['name'], data['phone'], data['address'])
            )
            con.commit()
            return True
        except:
            con.rollback()
            return False
        finally:
            con.close()

    def update(self, id, data):
        con = self.connect()
        cursor = con.cursor()
        try:
            cursor.execute(
                "UPDATE phone_book SET name=%s, phone=%s, address=%s WHERE id=%s",
                (data['name'], data['phone'], data['address'], id)
            )
            con.commit()
            return True
        except:
            con.rollback()
            return False
        finally:
            con.close()

    def delete(self, id):
        con = self.connect()
        cursor = con.cursor()
        try:
            cursor.execute("DELETE FROM phone_book WHERE id=%s", (id,))
            con.commit()
            return True
        except:
            con.rollback()
            return False
        finally:
            con.close()
