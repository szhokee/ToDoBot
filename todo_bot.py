import telebot
from telebot import types
from collections import defaultdict


class TodoBot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        self.user_tasks = defaultdict(list)

    def start(self):
        self.bot.message_handler(commands=['start'])(self.handle_start)
        self.bot.message_handler(commands=['tasks'])(self.handle_tasks)
        self.bot.message_handler(commands=['add'])(self.handle_add)
        self.bot.message_handler(commands=['update'])(self.handle_update)
        self.bot.message_handler(commands=['delete'])(self.handle_delete)
        self.bot.message_handler(commands=['clear'])(self.handle_clear)
        self.bot.message_handler(func=lambda message: True)(self.handle_unknown)
        self.bot.polling()

    def handle_start(self, message):
        user_id = message.from_user.id
        self.bot.reply_to(message, "Привет! Я ToDoBot. Чем я могу тебе помочь?")
        self.user_tasks[user_id] = []

    def handle_tasks(self, message):
        user_id = message.from_user.id
        task_list = self.user_tasks[user_id]
        task_text = ""
        if task_list:
            for index, task in enumerate(task_list):
                task_text += f"{index + 1}. {task}\n"
        else:
            task_text = "Список задач пуст."
        self.bot.reply_to(message, task_text)

    def handle_add(self, message):
        user_id = message.from_user.id
        self.bot.reply_to(message, "Введите новую задачу:")
        self.bot.register_next_step_handler(message, lambda msg: self.add_task(msg, user_id))

    def add_task(self, message, user_id):
        task = message.text
        self.user_tasks[user_id].append(task)
        self.bot.reply_to(message, "Задача успешно добавлена!")

    def handle_update(self, message):
        user_id = message.from_user.id
        self.bot.reply_to(message, "Введите номер задачи, которую хотите обновить:")
        self.bot.register_next_step_handler(message, lambda msg: self.update_task(msg, user_id))

    def update_task(self, message, user_id):
        task_index = int(message.text) - 1
        task_list = self.user_tasks[user_id]
        if 0 <= task_index < len(task_list):
            self.bot.reply_to(message, f"Введите новое значение для задачи \"{task_list[task_index]}\":")
            self.bot.register_next_step_handler(message, lambda msg: self.save_updated_task(msg, task_index, user_id))
        else:
            self.bot.reply_to(message, "Неверный номер задачи.")

    def save_updated_task(self, message, task_index, user_id):
        new_task = message.text
        self.user_tasks[user_id][task_index] = new_task
        self.bot.reply_to(message, "Задача успешно обновлена!")

    def handle_delete(self, message):
        user_id = message.from_user.id
        self.bot.reply_to(message, "Введите номер задачи, которую хотите удалить:")
        self.bot.register_next_step_handler(message, lambda msg: self.delete_task(msg, user_id))

    def delete_task(self, message, user_id):
        task_index = int(message.text) - 1
        task_list = self.user_tasks[user_id]
        if 0 <= task_index < len(task_list):
            deleted_task = task_list.pop(task_index)
            self.bot.reply_to(message, f"Task \"{deleted_task}\" успешно удалена!")
        else:
            self.bot.reply_to(message, "Неверный номер задачи.")

    def handle_clear(self, message):
        user_id = message.from_user.id
        self.user_tasks[user_id] = []
        self.bot.reply_to(message, "Список задач очищен!")

    def handle_unknown(self, message):
        self.bot.reply_to(message, "Извините, я не понимаю эту команду.")

if __name__ == "__main__":
    token = "6278169857:AAEwPYtUXxSzRQUQXjYPktI--7KEptTb01E"
    bot = TodoBot(token)
    bot.start()
    
    
    










# import telebot
# from telebot import types

# class TodoBot:
#     def __init__(self, token):
#         self.bot = telebot.TeleBot(token)
#         self.tasks = []

#     def start(self):
#         self.bot.message_handler(commands=['start'])(self.handle_start)
#         self.bot.message_handler(commands=['tasks'])(self.handle_tasks)
#         self.bot.message_handler(commands=['add'])(self.handle_add)
#         self.bot.message_handler(commands=['update'])(self.handle_update)
#         self.bot.message_handler(commands=['delete'])(self.handle_delete)
#         self.bot.message_handler(commands=['clear'])(self.handle_clear)
#         self.bot.message_handler(func=lambda message: True)(self.handle_unknown)
#         self.bot.polling()

#     def start(self):
#         markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
#         start_button = types.KeyboardButton('/start')
#         tasks_button = types.KeyboardButton('/tasks')
#         add_button = types.KeyboardButton('/add')
#         update_button = types.KeyboardButton('/update')
#         delete_button = types.KeyboardButton('/delete')
#         clear_button = types.KeyboardButton('/clear')
#         markup.add(start_button, tasks_button, add_button, update_button, delete_button, clear_button)

#         @self.bot.message_handler(commands=['start'])
#         def handle_start(message):
#             self.bot.reply_to(message, "Привет! Я ToDoBot. Чем я могу тебе помочь?", reply_markup=markup)

#         @self.bot.message_handler(commands=['tasks'])
#         def handle_tasks(message):
#             task_list = ""
#             if self.tasks:
#                 for index, task in enumerate(self.tasks):
#                     task_list += f"{index + 1}. {task}\n"
#             else:
#                 task_list = "Список задач пуст."
#             self.bot.reply_to(message, task_list, reply_markup=markup)

#         @self.bot.message_handler(commands=['add'])
#         def handle_add(message):
#             self.bot.reply_to(message, "Введите новую задачу:", reply_markup=markup)
#             self.bot.register_next_step_handler(message, self.add_task)

#         @self.bot.message_handler(commands=['update'])
#         def handle_update(message):
#             self.bot.reply_to(message, "Введите номер задачи, которую вы хотите обновить:", reply_markup=markup)
#             self.bot.register_next_step_handler(message, self.update_task)

#         @self.bot.message_handler(commands=['delete'])
#         def handle_delete(message):
#             self.bot.reply_to(message, "Введите номер задачи, которую вы хотите удалить:", reply_markup=markup)
#             self.bot.register_next_step_handler(message, self.delete_task)

#         @self.bot.message_handler(commands=['clear'])
#         def handle_clear(message):
#             self.tasks.clear()
#             self.bot.reply_to(message, "Все задачи были удалены!", reply_markup=markup)

#         @self.bot.message_handler(func=lambda message: True)
#         def handle_unknown(message):
#             self.bot.reply_to(message, "Неизвестная команда. Пожалуйста, попробуйте снова.", reply_markup=markup)

#         self.bot.polling()    

#     def handle_start(self, message):
#         self.bot.reply_to(message, "Привет! Я ToDoBot. Чем я могу тебе помочь?")

#     def handle_tasks(self, message):
#         task_list = ""
#         if self.tasks:
#             for index, task in enumerate(self.tasks):
#                 task_list += f"{index + 1}. {task}\n"
#         else:
#             task_list = "Список задач пуст."
#         self.bot.reply_to(message, task_list)

#     def handle_add(self, message):
#         self.bot.reply_to(message, "Введите новую задачу:")
#         self.bot.register_next_step_handler(message, self.add_task)

#     def add_task(self, message):
#         task = message.text
#         self.tasks.append(task)
#         self.bot.reply_to(message, "Задача успешно добавлена!")

#     def handle_update(self, message):
#         self.bot.reply_to(message, "Введите номер задачи, которую вы хотите обновить:")
#         self.bot.register_next_step_handler(message, self.update_task)

#     def update_task(self, message):
#         task_index = int(message.text) - 1
#         if 0 <= task_index < len(self.tasks):
#             self.bot.reply_to(message, f"Введите новое значение для задачи \"{self.tasks[task_index]}\":")
#             self.bot.register_next_step_handler(message, self.save_updated_task, task_index)
#         else:
#             self.bot.reply_to(message, "Неверный номер задачи.")

#     def save_updated_task(self, message, task_index):
#         new_task = message.text
#         self.tasks[task_index] = new_task
#         self.bot.reply_to(message, "Задача успешно обновлена!")

#     def handle_delete(self, message):
#         self.bot.reply_to(message, "Введите номер задачи, которую вы хотите удалить:")
#         self.bot.register_next_step_handler(message, self.delete_task)

#     def delete_task(self, message):
#         task_index = int(message.text) - 1
#         if 0 <= task_index < len(self.tasks):
#             deleted_task = self.tasks.pop(task_index)
#             self.bot.reply_to(message, f"Задача \"{deleted_task}\" успешно удалена!")
#         else:
#             self.bot.reply_to(message, "Неверный номер задачи.")

#     def handle_clear(self, message):
#         self.tasks.clear()
#         self.bot.reply_to(message, "Все задачи были удалены!")

#     def handle_unknown(self, message):
#         self.bot.reply_to(message, "Неизвестная команда. Пожалуйста, попробуйте снова.")

# # Создание экземпляра бота и его запуск
# bot = TodoBot('')
# bot.start()




