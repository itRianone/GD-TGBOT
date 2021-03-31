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

@bot.message_handler(content_types=['video', 'photo', 'sticker', 'document'])
def main(message):

  try:
    if message.content_type == 'photo':
      file_info = bot.get_file(message.photo.file_id)
    elif message.content_type == 'video':
      file_info = bot.get_file(message.video.file_id)
    elif message.content_type == 'sticker':
      file_info = bot.get_file(message.sticker.file_id)
    else:
      file_info = bot.get_file(message.document.file_id)
    
    #print(file_info.file_path)
    #print(os.path.exists(file_info.file_path)    
    
    src = file_info.file_path
    if os.path.exists('media/' + str(src)):
      bot.reply_to(message, "уже есть") 
    else:
      bot.reply_to(message, "Заберу себе") 
      img = open('media/photos/i_take_it.jpg','rb')
      bot.send_photo(message.chat.id, img)
      img.close()
      #bot download file in photos folder    
      downloaded_file = bot.download_file(src)
      print(file_info)

      with open('media/' + str(src), 'wb') as new_file:
        new_file.write(downloaded_file)

      #creating file in folder, which folder code decided from id
      gfile = drive.CreateFile({'parents': [{'id': parent_folder_id}]})
      
      #set which file add
      gfile.SetContentFile('media/' + str(src))
      #uploading
      gfile.Upload()


    

  except Exception as e:
    bot.reply_to(message, e)


if __name__ == '__main__':
  bot.polling(none_stop=True)