import telebot
import os.path
from config import TOKEN, FORLDER_ID as parent_folder_id
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import pprint
import io

#config file for headless auto auth
#SETTINGS_FILE = 'settings.yaml'

token = TOKEN
bot = telebot.TeleBot(token)


gauth = GoogleAuth()           
#start connection google drive, (behind the code opening browser, inputing the data from setting.yaml file)
drive = GoogleDrive(gauth)  

@bot.message_handler(content_types=['video', 'photo', 'sticker'])
def main(message):

  try:
    if message.content_type == 'photo':
      file_info = bot.get_file(message.photo[len(message.photo)-1].file_id)
    else:
      file_info = bot.get_file(message.photo[len(message.photo)-1].file_id)
      print('bruh, what a cringe file??')
    
    #print(file_info.file_path)
    #print(os.path.exists(file_info.file_path)    
    
    if os.path.exists(file_info.file_path):
      bot.reply_to(message, "уже есть") 
    else:
      bot.reply_to(message, "Заберу себе") 
      img = open('photos/i_take_it.jpg','rb')
      bot.send_photo(message.chat.id, img)
      img.close()
      #bot download file in photos folder    
      downloaded_file = bot.download_file(file_info.file_path)
      print(file_info)
      src = file_info.file_path

      with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)

      #creating file in folder, which folder code decided from id
      gfile = drive.CreateFile({'parents': [{'id': parent_folder_id}]})
      
      #set which file add
      gfile.SetContentFile(src)
      #uploading
      gfile.Upload()


    

  except Exception as e:
    bot.reply_to(message, e)


if __name__ == '__main__':
  bot.polling(none_stop=True)