    def reg(self): # действия, если пользователь нажал кнопку "Зарегистрироваться"
        try:
            log = self.login.text()
            passw = self.password.text()
            con = sqlite3.connect('datebase/results.db')
            cur = con.cursor()
            check_new_login(log, cur)
            check_new_password(passw)
            cur.execute("INSERT INTO users(name,password) VALUES('" + "','".join([log, passw]) + "')")
            res = cur.execute("""SELECT id, name FROM users
                     WHERE name = ?""", (log,)).fetchone()
            con.commit()
            con.close()
            self.user += list(res)
            self.out()
        except LoginError as le:
            self.error.setText(le.__str__())
            con.close()
        except PasswordError as pe:
            self.error.setText(pe.__str__())
            con.close()