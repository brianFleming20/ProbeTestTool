

import smtplib
import AdminUser

AU = AdminUser


class send_emails():

    # def notify_training(self, email):
    #     filepath = "training_email.txt"
    #     name = email.split('@')[0]
    #     a_user = name.split('.')[0]
    #     print(name)
    #     print(a_user)
    #     link = "user link"
    #     with open(filepath) as letter_file:
    #         contents = letter_file.read()
    #         new_contents = contents.replace(
    #             "[NAME]", a_user).replace("[here]", link)
    #     print(new_contents)
    #     # if self.send_email(new_contents,email):
    #     #     return True
    #     # else:
    #     #     return False
    #
    #
    # def send_email(self, content,recipetent):
    #     my_email = "deltex.medical3mail@gmail.com"
    #     # my_password = "Hf4aubkDFz6yHjRS"
    #     app_password = "yicacircbaoqimgb"
    #     with smtplib.SMTP("smtp.gmail.com") as connection:
    #         connection.starttls()
    #         connection.login(user=my_email, password=app_password)
    #         connection.sendmail(
    #             from_addr=my_email,
    #             # to_addrs="lee.lindfield@deltexmedical.com",
    #             # to_addrs="brian.fleming@deltexmedical.com",
    #             to_addrs=recipetent,
    #             msg=f"Subject:Deltex Medical Training Request\n\n{content}"
    #         )
    #     return True

    def reset_password(self, link):
        AU.ChangePasswordWindow.reset_password(self, link)
        AU.ChangePasswordWindow.refresh_window(self)


    def confirm_change(self):
        pass


