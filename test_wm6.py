from fastapi.testclient import TestClient
from wm6_API import app

client = TestClient(app)

def test_API():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "Модель распознавания распознавания текста из видео- аудио, суммаразинга текста"

def test_textsumm():  
    response = client.post("/text_summ/",
               json={"text": "Ну что, дружище, ты же на Мехмате учился? На Мехмате"}
               )
    result = response.json().strip()
    sResult = 'Ну что, дружище'
    assert response.status_code == 200
    assert result[:len(sResult)]  == sResult 
    
def test_YTsubtitres():    
    #Выдергиваем субтитры
    response = client.post("/get_text/",
               json={"subtitres_whisper": "Субтитры",
                     "sURL": "https://www.youtube.com/watch?v=6EsCI3CbmTk",
                     "subtitres_lang":"ru",
                     "t_video": "",
                     "t_audio": ""}
               )
    result = response.json().strip()
    sResult = 'Ну что дружище'
    assert response.status_code == 200
    assert result[:len(sResult)]  == sResult

def test_YTaudio():      
    #распознаём аудио на ютюб
    response = client.post("/get_text/",
               json={"subtitres_whisper": "Распознать аудио",
                     "sURL": "https://www.youtube.com/watch?v=6EsCI3CbmTk",
                     "subtitres_lang":"ru",
                     "t_video": "",
                     "t_audio": ""}
               )
    result = response.json().strip()
    sResult = 'Ну что, дружище'
    assert response.status_code == 200
    assert result[:len(sResult)]  == sResult
    
def test_audio():  
    response = client.post("/get_text/",
               json={"subtitres_whisper": "Распознать аудио",
                     "sURL": "https://www.youtube.com/watch?v=6EsCI3CbmTk",
                     "subtitres_lang":"ru",
                     "t_video": "Savvateev.mp4",
                     "t_audio": "Kati_k_kasse.mp3"}
               )
    result = response.json().strip()
    sResult = 'Наш покупал'
    assert response.status_code == 200
    assert result[:len(sResult)]  == sResult        
 
def test_video():  
    response = client.post("/get_text/",
               json={"subtitres_whisper": "Распознать аудио",
                     "sURL": "https://www.youtube.com/watch?v=6EsCI3CbmTk",
                     "subtitres_lang":"ru",
                     "t_video": "Savvateev.mp4",
                     "t_audio": ""}
               )
    result = response.json().strip()
    sResult = 'Передаю слово Алексею Владимировичу Саватееву'
    assert response.status_code == 200
    assert result[:len(sResult)]  == sResult        
    
