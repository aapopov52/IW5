# для сервера
from fastapi import FastAPI # API
from pydantic import BaseModel # какие параметры и какого типа мы пеедаём в запросах (автомат проверка формата и типов данных)

# для модели
import wm6_get_text
import wm6_summarize


# импортируем из pydantic базовый вариант класса для того
# чтобы задать какие именно данные требуются и какого типа
# здесь в поле text будем передавать текст для определения тональности
class Item_Get_text(BaseModel):
    subtitres_whisper: str = 'Субтитры'
    sURL: str = 'https://www.youtube.com/watch?v=6EsCI3CbmTk'
    subtitres_lang: str = 'ru'
    t_video: str = ''
    t_audio: str = ''
    
class Item_post_text_summ(BaseModel):
    text: str
    
# создаём приложене fastapi с переменной app
app = FastAPI()

# возврат сообщения которое хотим передать в формате json
# ключевое async нужно, чтобы обеспечить высокую производительность на Uvicorn
# где:
#     app — имя переменной объекта FastAP
#     get — название метода HTTP, который будет использоваться
#     ("/") — путь к запрашиваемому ресурсу. т.е. еслизапрос поступит к коревому каталогу сервера
@app.get("/")
async def root():
    return "Модель распознавания распознавания текста из видео- аудио, суммаразинга текста"

#http://127.0.0.1:8000/predict - в ответ на этот запрос выводится информация
@app.post("/text_summ/")
async def run_process_summarize(data_in: Item_post_text_summ):
    return wm6_summarize.process_summarize(data_in.text)

# теперь post
@app.post("/get_text/")
async def run_process_video(data_in: Item_Get_text): # в функцию передаётся об-т класса Item_Get_text
    return wm6_get_text.process_video(data_in.subtitres_whisper,                                   
                                      data_in.sURL, 
                                      data_in.subtitres_lang, 
                                      data_in.t_video, 
                                      data_in.t_audio)
    
    
# запуск приложения на сервере uvicorn       
#uvicorn wm6_API:app
# запуск post
#curl -X 'POST' \
#  'http://127.0.0.1:8000/predict/' \
#  -H 'Content-Type: application/json' \
#  -d '{
#  "text": "I hate machine learning engineering!"
#}'

#http://127.0.0.1:8000/get_text?subtitres_whisper=Субтитры&sURL=https://www.youtube.com/watch\?v=6EsCI3CbmTk&subtitres_lang=ru&t_video&t_audio=
