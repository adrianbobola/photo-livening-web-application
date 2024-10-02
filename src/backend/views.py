"""
Project: Aplikace pro oziveni fotek
Author: Adrian Bobola
Email: xbobol00@stud.fit.vutbr.cz
University: FIT VUT Brno
Created on: 2024-05-09
"""

import subprocess
from django.http import JsonResponse
from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse, Http404
import os
import logging
from .models import enqueue, dequeue, get_user_position, set_user_last_activity, remove_inactive_users, SystemState

uploaded_videos_motions = []


def write_log(stdout, stderr):
    """
    Zapis predane parametre do django.log
    """
    logger = logging.getLogger('std_output_logger')
    logger.info("stdout: %s", stdout)
    logger.info("stderr: %s", stderr)


def users_access(request):
    """
    Komponenta pre riadenie pristupu uzivatelov do aplikacie.
    Monitoruje aktualne vyuzitie systemu, zaraduje uzivatelov do cakacej fronty a povoluje pristup uzivatelovi
    do aplikacie
    """

    # Skontroluj neaktivych uzivatelov v cakajucej fronte a zisti aktualny stav vyuzitia systemu
    remove_inactive_users()
    SystemState.check_active_timer()

    if request.method == 'POST':
        user_token = request.POST.get('user_token')
        if not user_token:
            return JsonResponse({'error': 'User token is required'}, status=400)

        if not get_user_position(user_token):
            # Token uzivatela este nepoznam, zarad ho do cakajucej fronty
            enqueue(user_token)
            write_log("New user_token added to queue. User_token in stderr.", user_token)
        else:
            # Token uzivatela uz poznam, aktualizuj casove razitko jeho aktivity
            set_user_last_activity(user_token)

        if not SystemState.is_activated():
            # Aplikaciu aktualne nikto nepouziva, povol pristup uzivatelovi z cakajucej fronty
            user_token_allowed = dequeue()
            SystemState.set_active(user_token_allowed)
            write_log("SystemStatus activated. User_token is written in stderr value.", user_token_allowed)

        if SystemState.get_current_user_token() == user_token:
            # Uzivatelovi bol povoleny pristup do aplikacie
            return JsonResponse({'error': 'no'}, status=200)
        else:
            # Uzivatel musi cakat vo fronte, system je obsluhovany
            user_position_in_queue = get_user_position(user_token)
            return JsonResponse({'user_in_queue': user_position_in_queue}, status=202)

    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


def upload_image(request):
    """
    Komponenta pre nahravanie obrazkov na server
    """
    if request.method == 'POST' and request.FILES.get('image'):
        uploaded_image = request.FILES['image']
        upload_dir = os.path.join(settings.MEDIA_ROOT, '')

        # kontrola existencie adresaru /media
        os.makedirs(upload_dir, exist_ok=True)
        saved_image_path = os.path.join(upload_dir, uploaded_image.name)
        cache.set('saved_image_path', saved_image_path, timeout=300)
        with open(saved_image_path, 'wb') as f:
            for chunk in uploaded_image.chunks():
                f.write(chunk)

        # zostavenie URL nahraneho suboru, vyuziva ziskanu URL adresu backendu doplnenu o nazov nahraneho suboru
        image_url = request.build_absolute_uri(f"{settings.MEDIA_URL}{uploaded_image.name}")
        return JsonResponse({
            'image_url': image_url,
        }, status=200)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


def images_cropping(request):
    """
    Komponenta pre manualny orez obrazku pomocou zadanych suradnic
    """
    if request.method == 'POST':
        saved_image_path = cache.get('saved_image_path', "")
        nb_of_faces = int(cache.get('nb_of_faces', ""))

        # Ziskanie parametrov bounding-boxu pre pozadovany orez fotografie
        x = request.POST.get('x')
        y = request.POST.get('y')
        width = request.POST.get('width')
        height = request.POST.get('height')

        # Spustenie pomocneho skriptu a zapisanie vysledkov behu programu do django logu pre dohladanie chyb
        script_path = os.path.join(settings.SCRIPT_ROOT, 'custom_image_cropping', 'custom_image_cropping.py')
        result = subprocess.run(
            ['python', script_path, saved_image_path, str(nb_of_faces), str(x), str(y), str(width), str(height)],
            capture_output=True, text=True)

        write_log(result.stdout, result.stderr)

        if result.returncode == 0:
            # Orez fotografie prebehol uspesne, zvys pocet obrazkov orezanych tvari
            nb_of_faces += 1
            cache.set('nb_of_faces', str(nb_of_faces), timeout=300)
            return JsonResponse({'error': 'no'}, status=200)
        else:
            return JsonResponse({'error': result.stderr}, status=500)

    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


def faces_detect(request):
    """
    Komponenta pre detekciu tvari na obrazku a orezanie na samostatne obrazky tvari
    """
    if request.method == 'GET':
        # Spustenie skriptu na detekciu tvari a orez fotografie
        script_path = os.path.join(settings.SCRIPT_ROOT, 'face_detector', 'face_detector.py')
        saved_image_path = cache.get('saved_image_path', "")
        result = subprocess.run(['python', script_path, saved_image_path], capture_output=True, text=True)
        nb_of_faces = result.stdout.strip()
        write_log(result.stdout, result.stderr)

        # Aktualizuj parametre o poctu orezanych fotografii
        if nb_of_faces == '':
            nb_of_faces = 0
        cache.set('nb_of_faces', str(nb_of_faces), timeout=300)

        return JsonResponse({
            'number_of_faces': int(nb_of_faces)
        }, status=200)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


def upload_video(request):
    """
    Komponenta pre nahravanie videi na server do priecinku /media
    """
    if request.method == 'POST' and request.FILES.get('video'):
        # kontrola existencie adresaru /media a ulozenie suboru
        uploaded_video = request.FILES['video']
        upload_dir = os.path.join(settings.MEDIA_ROOT, '')
        os.makedirs(upload_dir, exist_ok=True)
        saved_video_path = os.path.join(upload_dir, uploaded_video.name)
        with open(saved_video_path, 'wb') as f:
            for chunk in uploaded_video.chunks():
                f.write(chunk)

        # Aktualizuj parametre o pocte nahranych videi a ich nazvy
        global uploaded_videos_motions
        uploaded_videos_motions.append(uploaded_video.name)
        nb_of_uploaded_videos = int(cache.get('nb_of_uploaded_videos', 0))
        nb_of_uploaded_videos += 1
        cache.set('nb_of_uploaded_videos', int(nb_of_uploaded_videos), timeout=300)

        # zostavenie URL nahraneho video suboru
        processed_video_url = request.build_absolute_uri(f"{settings.MEDIA_URL}{uploaded_video.name}")

        return JsonResponse({
            'processed_video_url': processed_video_url
        }, status=200)
    else:
        return JsonResponse({'error': 'No video file provided'}, status=400)


def videos_count(request):
    """
    Komponenta pre poskytnutie informaci o pocte nahranych videi
    """
    if request.method == 'GET':
        nb_of_uploaded_videos = int(cache.get('nb_of_uploaded_videos', 0))
        global uploaded_videos_motions
        return JsonResponse({'nb_of_uploaded_videos': nb_of_uploaded_videos,
                             'uploaded_videos_names': uploaded_videos_motions}, status=200)
    else:
        return JsonResponse({'error': 'DELETE method required'}, status=405)


def faces_count(request):
    """
    Komponenta pre poskytnutie informaci o pocte samostatnych orezanych fotografii
    """
    if request.method == 'GET':
        nb_of_faces = int(cache.get('nb_of_faces', ""))
        return JsonResponse({'nb_of_faces': nb_of_faces}, status=200)
    else:
        return JsonResponse({'error': 'Bad request'}, status=400)


def clean_up(request):
    """
    Komponenta pre reset hodnot v pamati a odstanenie docasnych suborov z adresaru /media
    Pouziva sa pre novy beh aplikcie
    """
    if request.method == 'DELETE':
        upload_dir = settings.MEDIA_ROOT
        try:
            global uploaded_videos_motions
            uploaded_videos_motions.clear()
            cache.delete('nb_of_faces')
            cache.delete('saved_image_path')
            cache.delete('nb_of_uploaded_videos')

            for filename in os.listdir(upload_dir):
                # najdi vsetky docasne subory v adresari /media, ktore sa mozu zmazat
                file_path = os.path.join(upload_dir, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)

            return JsonResponse({'message': 'All uploaded images deleted successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'DELETE method required'}, status=405)


def faces_reenactment(request, face_id):
    """
    Komponenta pre rozpohybovanie tvare podla nahraneho videa s pohybom

    Parameters:
        face_id (int) -  identifikator tvare, ktora sa ma rozpohybovat
    """
    if request.method == 'GET':
        script_dir = os.path.join(settings.SCRIPT_ROOT, 'face_reenactment')
        source_image = os.path.join(settings.MEDIA_ROOT, f'{face_id}.png')
        os.chdir(script_dir)

        # Spustenie skriptu a zapis vysledku spustenia do logu
        result = subprocess.run(['python', 'camera_local.py', '--source_image', source_image], capture_output=True,
                                text=True)
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        write_log(result.stdout, result.stderr)

        if result.returncode == 0:
            return JsonResponse({'error': 'no'}, status=200)
        else:
            return JsonResponse({'error': result.stderr}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def convert_video_to_h264(video_path, output_path):
    """
    Konverzia videa do H.264

    Parameters:
        video_path (str) - cesta povodneho videa
        output_path (str) - cesta pre ulozenie konvertovaneho videa
    """
    command = [
        'ffmpeg',
        '-i', video_path,
        '-c:v', 'libx264',
        '-preset', 'slow',
        '-crf', '22',
        '-c:a', 'aac',
        '-b:a', '128k',
        output_path
    ]
    subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return output_path


def videos_generator(request):
    """
    Vytvorenie finalneho videa nahradenim rozpohybovanych videami v orezanych castiach obrazku
    """
    if request.method == 'POST':
        user_token = request.POST.get('user_token')
        if not user_token:
            return JsonResponse({'error': 'User token is required'}, status=400)

        # Ziskanie nazvov vsetkych suborov, ktore vznikli rozpohybovanim obrazku podla nahraneho videa
        global uploaded_videos_motions
        filenames = ''
        for file in uploaded_videos_motions:
            helper = file
            if '_driving.mp4' in file:
                helper = helper.split('_driving.mp4')[0]
            elif '_driving.webm' in file:
                helper = helper.split('_driving.webm')[0]
            filenames += helper
            filenames += ' '
        filenames = filenames[:-1]

        # Ziskanie pozadovanych umiestneni
        script_dir = os.path.join(settings.SCRIPT_ROOT, 'video_maker')
        media_root = settings.MEDIA_ROOT
        os.chdir(script_dir)

        # Spustenie skriptu video_maker.py a zapis vysledkov spustenia do logu
        arguments = ['python', 'video_maker.py', filenames, media_root]
        result = subprocess.run(arguments, capture_output=True, text=True)
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        write_log(result.stdout, result.stderr)

        if result.returncode == 0:
            # Vytvorenie finalneho videa prebehlo uspesne, spust konverziu do H.264 a predaj cestu k videu uzivatelovi
            video_path = os.path.join(settings.MEDIA_ROOT, 'output.mp4')
            output_filename = f"video_{user_token}.mp4"
            output_path = os.path.join(settings.MEDIA_ROOT, 'results', output_filename)
            converted_video_path = convert_video_to_h264(video_path, output_path)

            return JsonResponse({'converted_video_path': converted_video_path}, status=200)
        else:
            return JsonResponse({'error': result.stderr}, status=500)

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def videos_result(request, user_token):
    """
    Predanie cesty s vytvorenym videom danemu uzivatelovi

    Parameters:
        user_token (string): Token uzivatela, pod ktorym sa vygenerovalo video
    """
    if request.method == 'GET':
        # Video sa vygenerovalo, umozni beh dalsiemu uzivatelovi v cakajucej fronte
        SystemState.set_inactive()
        write_log("SystemState deactivated", '')

        # Ziskanie cesty vygenerovaneho videa a predanie video suboru uzivatelovi
        source_video = os.path.join(settings.MEDIA_ROOT, 'results', f'video_{user_token}.mp4')
        with open(source_video, 'rb') as video_file:
            response = HttpResponse(video_file.read(), content_type="video/mp4")
            return response
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
