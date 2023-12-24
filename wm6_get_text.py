import os
import moviepy.editor as mp 
from faster_whisper import WhisperModel
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi

import nltk
nltk.download('punkt')
nltk.download('stopwords')

# Загружаем модель Whisper
model = WhisperModel("large-v2")
#https://www.youtube.com/watch?v=6EsCI3CbmTk - пример
def process_video(subtitres_whisper, sURL, subtitres_lang, t_video, t_audio):
    # Распознаём аудио-файл
    if t_audio != "" and not(t_audio is None):  
        return GetTextFromVideoAudio(t_audio)
    # Распознаём видео-файл     
    if t_video != "" and not(t_video is None):
        return GetTextFromVideoAudio(t_video)

    # Извлекаем видео ID из URL
    if 'v=' in sURL and sURL[:len('https://www.youtube.com/watch?')] == 'https://www.youtube.com/watch?':
        video_id = sURL.split("v=")[1]
        # Получаем информацию о видео
        yt = YouTube(sURL)
        if subtitres_whisper == 'Субтитры':
            # Извлекаем субтитры
            return GetSubtitres(subtitres_lang, yt)

        if subtitres_whisper == 'Распознать аудио':
            # Анализ аудио
            return GetTextFromVideoYt(yt)    

    return "Укажите параметры работы с видео материалом."

# получаем субтитры с Ютьб

def GetSubtitres(first_language_code, yt):

    sLang = 'Базовые языки:' + '\n'
    bFind = False
    transcript_list = YouTubeTranscriptApi.list_transcripts(yt.video_id)
    for transcript in transcript_list:
        sLang += '   - ' + transcript.language_code + ' - ' + transcript.language + '\n'
        if transcript.language_code == first_language_code:
            Text_sub = transcript.fetch()
            bFind = True
            break
    sLang += '\n' + 'Переводы:' + '\n'

    if not bFind:
        for transcript in transcript_list:
            if transcript.is_translatable == True:
                sLang += '   - Базовый язык ' + transcript.language_code + ' - ' + transcript.language + '. Переводы:\n'
                for tr_l in transcript.translation_languages:
                    sLang += '      - ' + tr_l['language_code'] + ' - ' + tr_l['language'] + '\n'
                    if tr_l['language_code'] == first_language_code:
                        Text_sub = transcript.translate(first_language_code).fetch()
                        bFind = True
                        break
    sText = ''
    if bFind:
        for s1 in Text_sub:
            sText += s1['text'] + '\n'
        return sText
    else:
        return "Указанный код языка не найден. Возможо выбрать указанные ниже языки:" + '\n' + sLang

# получаем аудио с Ютьюб
def GetTextFromVideoYt(yt):
    fileName = yt.streams.filter(type = "audio").first().download()
    audio_file = mp.AudioFileClip(fileName) 
    audio_file.write_audiofile("vrem.wav")
    
    segments, info = model.transcribe("vrem.wav")
    sText = ''
    for segment in segments:
        sText += segment.text
    os.remove(fileName)
    os.remove("vrem.wav")

    return sText
        
# Работа с аудио/видео на локальном диске
def GetTextFromVideoAudio(fileName):
    audio_file = mp.AudioFileClip(fileName)
    audio_file.write_audiofile("vrem.wav")
    segments, info = model.transcribe("vrem.wav")
    sText = ''
    for segment in segments:
        sText += segment.text

    os.remove(fileName)
    os.remove("vrem.wav")

    return sText
