import telebot
from telebot import types
from collections import defaultdict


class TodoBot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        self.user_tasks = defaultdict(list)

    def start(self):
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        start_button = types.KeyboardButton('/start')
        tasks_button = types.KeyboardButton('/tasks')
        add_button = types.KeyboardButton('/add')
        update_button = types.KeyboardButton('/update')
        delete_button = types.KeyboardButton('/delete')
        clear_button = types.KeyboardButton('/clear')
        markup.add(start_button, tasks_button, add_button, update_button, delete_button, clear_button)

        @self.bot.message_handler(commands=['start'])
        def handle_start(message):
            self.bot.reply_to(message, "Hello! I am ToDoBot. How can I assist you?", reply_markup=markup)

        @self.bot.message_handler(commands=['tasks'])
        def handle_tasks(message):
            user_id = message.from_user.id
            task_list = self.user_tasks[user_id]
            task_text = ""
            if task_list:
                for index, task in enumerate(task_list):
                    task_text += f"{index + 1}. {task}\n"
            else:
                task_text = "Task list is empty."
            self.bot.reply_to(message, task_text, reply_markup=markup)

        @self.bot.message_handler(commands=['add'])
        def handle_add(message):
            user_id = message.from_user.id
            self.bot.reply_to(message, "Enter a new task:", reply_markup=markup)
            self.bot.register_next_step_handler(message, lambda msg: self.add_task(msg, user_id))

        @self.bot.message_handler(commands=['update'])
        def handle_update(message):
            user_id = message.from_user.id
            self.bot.reply_to(message, "Enter the task number you want to update:", reply_markup=markup)
            self.bot.register_next_step_handler(message, lambda msg: self.update_task(msg, user_id))

        @self.bot.message_handler(commands=['delete'])
        def handle_delete(message):
            user_id = message.from_user.id
            self.bot.reply_to(message, "Enter the task number you want to delete:", reply_markup=markup)
            self.bot.register_next_step_handler(message, lambda msg: self.delete_task(msg, user_id))

        @self.bot.message_handler(commands=['clear'])
        def handle_clear(message):
            user_id = message.from_user.id
            self.user_tasks[user_id] = []
            self.bot.reply_to(message, "All tasks have been cleared!", reply_markup=markup)

        @self.bot.message_handler(func=lambda message: True)
        def handle_unknown(message):
            self.bot.reply_to(message, "Unknown command. Please try again.", reply_markup=markup)

        self.bot.polling()

    def add_task(self, message, user_id):
        task = message.text
        self.user_tasks[user_id].append(task)
        self.bot.reply_to(message, "Task successfully added!")

    def update_task(self, message, user_id):
        task_index = int(message.text) - 1
        task_list = self.user_tasks[user_id]
        if 0 <= task_index < len(task_list):
            self.bot.reply_to(message, f"Enter the new value for the task \"{task_list[task_index]}\":")
            self.bot.register_next_step_handler(message, lambda msg: self.save_updated_task(msg, task_index, user_id))
        else:
            self.bot.reply_to(message, "Invalid task number.")

    def save_updated_task(self, message, task_index, user_id):
        new_task = message.text
        self.user_tasks[user_id][task_index] = new_task
        self.bot.reply_to(message, "Task successfully updated!")

    def delete_task(self, message, user_id):
        task_index = int(message.text) - 1
        task_list = self.user_tasks[user_id]
        if 0 <= task_index < len(task_list):
            deleted_task = task_list.pop(task_index)
            self.bot.reply_to(message, f"Task \"{deleted_task}\" successfully deleted!")
        else:
            self.bot.reply_to(message, "Invalid task number.")

if __name__ == "__main__":
    token = "6278169857:AAEwPYtUXxSzRQUQXjYPktI--7KEptTb01E"
    bot = TodoBot(token)
    bot.start()                                            
