import mysql.connector
from mysql.connector import Error

class UserManager:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                database='web_demo',
                user='root',
                password='Gumb@110v0'  
            )
            self.cursor = self.connection.cursor()
            print("Kết nối thành công!")
            self._create_table()
        except Error as e:
            print(f"Lỗi kết nối: {e}")
            exit()

    def _create_table(self):
        """Tự động tạo bảng nếu chưa có"""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.connection.commit()

    # ─── THÊM ───────────────────────────────────────────
    def add_user(self, name, email):
        try:
            sql = "INSERT INTO users (name, email) VALUES (%s, %s)"
            self.cursor.execute(sql, (name, email))
            self.connection.commit()
            print(f" Đã thêm: {name} - {email}")
        except Error as e:
            print(f" Lỗi thêm: {e}")

    # ─── XEM TẤT CẢ ─────────────────────────────────────
    def show_all_users(self):
        try:
            self.cursor.execute("SELECT * FROM users")
            users = self.cursor.fetchall()
            if not users:
                print("Chưa có người dùng nào!")
                return
            print("\n{:<5} {:<25} {:<30} {}".format("ID", "Tên", "Email", "Ngày tạo"))
            print("-" * 75)
            for u in users:
                print("{:<5} {:<25} {:<30} {}".format(u[0], u[1], u[2], u[3]))
        except Error as e:
            print(f"Lỗi xem: {e}")

    # ─── SỬA ────────────────────────────────────────────
    def update_user(self, user_id, new_name, new_email):
        try:
            sql = "UPDATE users SET name=%s, email=%s WHERE id=%s"
            self.cursor.execute(sql, (new_name, new_email, user_id))
            self.connection.commit()
            if self.cursor.rowcount > 0:
                print(f" Đã sửa ID {user_id} → {new_name} - {new_email}")
            else:
                print(f" Không tìm thấy ID {user_id}")
        except Error as e:
            print(f"Lỗi sửa: {e}")

    # ─── XÓA ────────────────────────────────────────────
    def delete_user(self, user_id):
        try:
            sql = "DELETE FROM users WHERE id=%s"
            self.cursor.execute(sql, (user_id,))
            self.connection.commit()
            if self.cursor.rowcount > 0:
                print(f"Đã xóa ID {user_id}")
            else:
                print(f"  Không tìm thấy ID {user_id}")
        except Error as e:
            print(f"Lỗi xóa: {e}")

    # ─── TÌM KIẾM ───────────────────────────────────────
    def search_user(self, keyword):
        try:
            sql = "SELECT * FROM users WHERE name LIKE %s OR email LIKE %s"
            self.cursor.execute(sql, (f"%{keyword}%", f"%{keyword}%"))
            users = self.cursor.fetchall()
            if not users:
                print(f"  Không tìm thấy '{keyword}'")
                return
            print(f"\n Kết quả tìm '{keyword}':")
            print("{:<5} {:<25} {:<30} {}".format("ID", "Tên", "Email", "Ngày tạo"))
            print("-" * 75)
            for u in users:
                print("{:<5} {:<25} {:<30} {}".format(u[0], u[1], u[2], u[3]))
        except Error as e:
            print(f" Lỗi tìm: {e}")

    def close(self):
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print(" Đã đóng kết nối.")


# ═══════════════════════════════════════════════════════
#  MENU CHÍNH
# ═══════════════════════════════════════════════════════
def main():
    db = UserManager()

    while True:
        print("\n" + "═" * 35)
        print("       QUẢN LÝ NGƯỜI DÙNG")
        print("═" * 35)
        print("  1. Xem tất cả người dùng")
        print("  2. Thêm người dùng")
        print("  3. Sửa người dùng")
        print("  4. Xóa người dùng")
        print("  5. Tìm kiếm")
        print("  0. Thoát")
        print("═" * 35)

        choice = input("Chọn: ").strip()

        if choice == '1':
            db.show_all_users()

        elif choice == '2':
            name  = input("Tên: ").strip()
            email = input("Email: ").strip()
            if name and email:
                db.add_user(name, email)
            else:
                print("Vui lòng nhập đủ thông tin!")

        elif choice == '3':
            db.show_all_users()
            try:
                uid       = int(input("\nNhập ID cần sửa: "))
                new_name  = input("Tên mới: ").strip()
                new_email = input("Email mới: ").strip()
                if new_name and new_email:
                    db.update_user(uid, new_name, new_email)
                else:
                    print("Vui lòng nhập đủ thông tin!")
            except ValueError:
                print("ID phải là số!")

        elif choice == '4':
            db.show_all_users()
            try:
                uid = int(input("\nNhập ID cần xóa: "))
                confirm = input(f"Xác nhận xóa ID {uid}? (y/n): ")
                if confirm.lower() == 'y':
                    db.delete_user(uid)
            except ValueError:
                print("ID phải là số!")

        elif choice == '5':
            keyword = input("Nhập từ khóa tìm kiếm: ").strip()
            if keyword:
                db.search_user(keyword)

        elif choice == '0':
            db.close()
            break
        else:
            print("Vui lòng chọn từ 0-5!")

if __name__ == "__main__":
    main()
