import json
import random
from datetime import datetime

# 定义数据文件名
DATA_FILE = 'data.json'

# 定义用户类
class User:
    def __init__(self, username, password=None):
        self.username = username
        self.password = password
        self.points = 0
        self.last_login_date = None

    def set_password(self, password):
        self.password = password

    def check_password(self, password):
        return self.password == password

    def add_points(self, points):
        self.points += points

    def can_sign_in(self):
        if self.last_login_date is None:
            return True
        last_login = datetime.strptime(self.last_login_date, '%Y-%m-%d')
        return (datetime.now() - last_login).days > 0

    def update_last_login(self):
        self.last_login_date = datetime.now().strftime('%Y-%m-%d')

# 定义用户管理系统
class UserManager:
    def __init__(self):
        self.users = {}

    def load_users(self):
        try:
            with open(DATA_FILE, 'r') as f:
                users_data = json.load(f)
                for username, data in users_data.items():
                    user = User(username)
                    user.password = data['password']
                    user.points = data['points']
                    user.last_login_date = data['last_login_date']
                    self.users[username] = user
        except FileNotFoundError:
            self.users = {}

    def save_users(self):
        with open(DATA_FILE, 'w') as f:
            users_data = {user.username: {
                'password': user.password,
                'points': user.points,
                'last_login_date': user.last_login_date
            } for user in self.users.values()}
            json.dump(users_data, f)

    def get_user(self, username):
        return self.users.get(username)

    def add_user(self, user):
        self.users[user.username] = user

# 主程序
def main():
    user_manager = UserManager()
    user_manager.load_users()

    while True:
        username = input("输入用户名：>_ ")
        user = user_manager.get_user(username)

        if user is None:
            print("检测到首次登陆！")
            password = input("输入密码：>_ ")
            user = User(username)
            user.set_password(password)
            user_manager.add_user(user)
        else:
            password = input("输入密码：>_ ")
            if not user.check_password(password):
                print("密码错误！")
                continue

        print("登陆成功！请输入指令：>_ ", end='')
        command = input()

        if command == 'qd':
            if user.can_sign_in():
                points = random.randint(10, 20)
                user.add_points(points)
                user.update_last_login()
                user_manager.save_users()
                print(f"签到成功！获得{points}积分")
            else:
                print("今天已经签到过了！")
        elif command.startswith('hx '):
            try:
                deduct_points = int(command.split(' ')[1])
                if user.points >= deduct_points:
                    user.points -= deduct_points
                    user_manager.save_users()
                    print(f"成功扣除{deduct_points}积分，当前剩余{user.points}积分。")
                else:
                    print("积分不足，无法扣除。")
            except ValueError:
                print("输入格式错误，请使用 'hx 分数' 格式。")
        elif command == 'cx':
            print(f"您当前的积分为：{user.points} 分。")
        elif command == 'logout':
            print("Logout！")
            break
        else:
            print("未知指令！")

        print("Logout！")
        main()
        break

# 运行主程序
main()  # 这行代码在实际使用时可以取消注释来运行程序

