# import telebot
# from telebot import types
# from collections import defaultdict


# class StartHandler:
#     def handle(self, message, bot, user_tasks):
#         user_id = message.from_user.id
#         bot.reply_to(message, "Hello! I'm ToDoBot. How can I assist you?")
#         user_tasks[user_id] = []


# class TasksHandler:
#     def handle(self, message, bot, user_tasks):
#         user_id = message.from_user.id
#         task_list = user_tasks[user_id]
#         task_text = ""
#         if task_list:
#             for index, task in enumerate(task_list):
#                 task_text += f"{index + 1}. {task}\n"
#         else:
#             task_text = "The task list is empty."
 
#         bot.reply_to(message, task_text)


# class AddHandler:
#     def __init__(self, user_tasks, bot):
#         self.user_tasks = user_tasks
#         self.bot = bot
        
#     def handle(self, message, bot, user_tasks):
#         user_id = message.from_user.id
#         self.bot.reply_to(message, "Enter a new task:")
#         self.bot.register_next_step_handler(message, lambda msg: self.add_task(msg, user_id, bot))

#     def add_task(self, message, user_id, bot):
#         task = message.text
#         self.user_tasks[user_id].append(task)
#         self.bot.reply_to(message, "Task successfully added!")


# class DeleteHandler:
#     def __init__(self, user_tasks):
#         self.user_tasks = user_tasks

#     def handle(self, message, bot, user_tasks):
#         user_id = message.from_user.id
#         bot.reply_to(message, "Enter the task number you want to delete:")
#         bot.register_next_step_handler(message, lambda msg: self.delete_task(msg, user_id, bot))

#     def delete_task(self, message, user_id, bot):
#         task_index = int(message.text) - 1
#         task_list = self.user_tasks[user_id]
#         if 0 <= task_index < len(task_list):
#             deleted_task = task_list.pop(task_index)
#             bot.reply_to(message, f"Task \"{deleted_task}\" successfully deleted!")
#         else:
#             bot.reply_to(message, "Invalid task number.")


# class UpdateHandler:
#     def __init__(self, user_tasks):
#         self.user_tasks = user_tasks

#     def handle(self, message, bot, user_tasks):
#         user_id = message.from_user.id
#         bot.reply_to(message, "Enter the task number you want to update:")
#         bot.register_next_step_handler(message, lambda msg: self.update_task(msg, user_id, bot))

#     def update_task(self, message, user_id, bot):
#         task_index = int(message.text) - 1
#         task_list = self.user_tasks[user_id]
#         if 0 <= task_index < len(task_list):
#             bot.reply_to(message, f"Enter a new value for the task \"{task_list[task_index]}\":")
#             bot.register_next_step_handler(message, lambda msg: self.save_updated_task(msg, task_index, user_id, bot))
#         else:
#             bot.reply_to(message, "Invalid task number.")

#     def save_updated_task(self, message, task_index, user_id, bot):
#         new_task = message.text
#         self.user_tasks[user_id][task_index] = new_task
#         bot.reply_to(message, "Task successfully updated!")


# class UnknownHandler:
#     def handle(self, message, bot):
#         bot.reply_to(message, "Sorry, I don't understand this command.")


# class TodoBot:
#     def __init__(self, token):
#         self.bot = telebot.TeleBot(token)
#         self.user_tasks = defaultdict(list)

#         self.start_handler = StartHandler()
#         self.tasks_handler = TasksHandler()
#         self.add_handler = AddHandler(self.user_tasks, self.bot)
#         self.delete_handler = DeleteHandler(self.user_tasks)
#         self.update_handler = UpdateHandler(self.user_tasks)
#         self.unknown_handler = UnknownHandler() 

#         self.register_commands() 
#         self.register_buttons() 

#     def register_commands(self):
#         self.bot.message_handler(commands=['start'])(lambda message: self.start_handler.handle(message, self.bot, self.user_tasks))
#         self.bot.message_handler(commands=['tasks'])(lambda message: self.tasks_handler.handle(message, self.bot, self.user_tasks))
#         self.bot.message_handler(commands=['add'])(lambda message: self.add_handler.handle(message, self.bot, self.user_tasks))
#         self.bot.message_handler(commands=['update'])(lambda message: self.update_handler.handle(message, self.bot, self.user_tasks))
#         self.bot.message_handler(commands=['delete'])(lambda message: self.delete_handler.handle(message, self.bot, self.user_tasks))
#         self.bot.message_handler(func=lambda message: True)(lambda message: self.unknown_handler.handle(message, self.bot))

#     def register_buttons(self):
#         start_button = types.KeyboardButton('/start')
#         add_button = types.KeyboardButton('/add')
#         delete_button = types.KeyboardButton('/delete')
#         update_button = types.KeyboardButton('/update')
#         tasks_button = types.KeyboardButton('/tasks')

#         markup = types.ReplyKeyboardMarkup(row_width=2)
#         markup.add(start_button, tasks_button)
#         markup.add(add_button, update_button, delete_button)       

#         self.bot.message_handler(commands=['start'])(lambda message: self.bot.send_message(message.chat.id, 'Choose an action:', reply_markup=markup))

#     def start(self):
#         self.bot.polling()    


# if __name__ == "__main__":
#     token = "6278169857:AAEwPYtUXxSzRQUQXjYPktI--7KEptTb01E"
#     bot = TodoBot(token)
#     bot.start()