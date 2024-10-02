# BP: Aplikace pro oživení fotek

**Link:** [https://dspace.vut.cz/items/132db686-f329-48f7-825e-e929a6b1d85b](https://dspace.vut.cz/items/132db686-f329-48f7-825e-e929a6b1d85b)

    Author: Adrian Bobola  
    Email: xbobol00@stud.fit.vutbr.cz  
    University: FIT VUT Brno  
    Created on: 2024-05-09

## Popis

    Cieľom tejto práce je vytvoriť webovú aplikáciu pre oživenie statických fotografií.
    Aplikácia umožňuje užívateľovi rozpohybovať svoje portrétové ako aj skupinové fotografie.
    Užívateľ môže nahrať vlastný pohyb, ktorý chce použiť, a aplikácia ho použije k rozpohybovaniu vybranej
    časti nahranej fotografie.
    Tváre osôb na fotografiách sú detegované automaticky, pričom užívateľ má možnosť manuálneho
    označenia tvárí na danej fotografii.
    Aplikácia podporuje nahrávanie vlastného pohybu z video súboru, alebo priamo z webkamery.

    Serverová časť aplikácie je implementovaná v jazyku Python s využitím frameworku Django.
    Klientská časť aplikácie využíva JavaScript a framework React.
    Komunikácia medzi klientom a serverom je zabezpečená prostredníctvom REST API.

## Odovzdané súbory

    thesis.pdf
        Text práce vo formáte PDF odovzdaný v IS

    thesis_printed.pdf
        Text práce vo formáte PDF použitý pre tlač

    video.mp4
        Demonštračné video vytvorenej webovej aplikácie

    poster.pdf
        Plagát vytvorenej aplikácie

    /thesis_latex/
        Zdrojový text práce určený pre LaTeX

    /build/
        Vytvorený produkčný spustiteľný build klientskej časti aplikácie.
        Je vytvorený pre adresu backendu: http://127.0.0.1:8000
        Tento build je možné sputiť napr. pomocou nástroja "serve":
            npm install -g serve
            serve -s build -l 3000
        Tento príkaz spustí server pre klientskú časť aplikácie na porte 3000
        Príkaz je potrebné spúšťať v adresári /src/ pomocou terminálu

    /src/
        Adresár obsahuje všetky zdrojové texty vytvorenej webovej aplikácie.
        Na spustenie serverovej časti aplikácie stačí v adresári /src/ zadať príkaz:
            python manage.py runserver
        Pred spustením serverovej časti sa uistite, že máte nainštalované všetky potrebné knižnice a balíky.

## Minimálne požiadavky pre spustenie serverovej časti aplikácie

    Webová aplikácia bola implementovaná pre operačné systémy založené na Debian GNU / Linux.
    Pre jej optimálne spustenie sa odporúča použiť systém Ubuntu, na ktorom bola vyvíjaná a testovaná.

    Je požadovaná grafická karta od výrobcu NVIDIA a správne nainštalovaný CUDA toolkit.
    Vyžaduje sa tiež inštalácia balíkov:
        Node.js (verzia 10.x alebo novšia) ktorý zahŕňa npm,
        Python (verzia 3.6 alebo novšia) so správcom balíčkov pip pre inštaláciu Django frameworku,
        ffmpeg (verzia 7.0 alebo novšia),
        OpenCV (verzia 4.9 alebo novšia)
        torch>=1.11.0,
        numpy>=1.23.5,
        PyYAML,
        imageio[ffmpeg],
        batch-face,
        gdown,
        scipy

## Klientská časť aplikácie

    Zdrojový kód klientskej časti aplikácie sa nachádza v priečinku /src/frontend/
    Vytvorený produkčný spustiteľný build klientskej časti aplikácie pre adresu backendu: http://127.0.0.1:8000 nájdete
    v adresári /build/.
    Viac info v sekcii "Odovzdané súbory".

    V súbore /frontend/.env je potrebné nastaviť hodnotu premennej REACT_APP_BACKEND_URL na URL adresu, kde je spustený backendový server.
    Uistite sa, že zadaná adresa je dostupná z prostredia v ktorom je klientská časť aplikácie spustená.
    Klientská časť aplikácie sa pre testovacie účely spúšťa v adresári /frontend/ pomocou príkazov:
        "npm install" a "npm run build"

    Príkaz "npm install" automaticky stiahne všetky potrebné knižnice a závislosti nevyhnutné pre správnu funkčnosť aplikácie.
    Po úspešnom stiahnutí týchto knižníc sa príkazom npm run build vytvorí produkčná verzia klientskej časti aplikácie.
    Túto verziu je možné na testovacie účely spustiť lokálne pomocou príkazu "serve -s build", ktorý spustí lokálny server
    a umožní prístup k aplikácii cez webový prehliadač.
    --------------------------------------------------------------------------------------------------------------------------------
    Priečinok /src/frontend/src/ obsahuje:
        /assets/ - ikony pre slovenský a anglický jazyk aplikácie
        /locales/ - json súbory textov pre anglickú a slovenskú verziu aplikácie
        /pages/ - jednotlivé podstránky klientskej časti aplikácie
        i18n.js - jazykova podpora obsahu stranok
        index.css - kaskádové štýly pre celú webovú aplikáciu
        index.js - vstupný bod aplikácie, ktorý načitáva ďalšie stránky z /pages/
        logo.svg - logo aplikácie
    --------------------------------------------------------------------------------------------------------------------------------
    Priečinok /src/frontend/src/pages/ obsahuje:
        About.js - statická stránka "O aplikacii"
        AppStart.js - úvodná stránka aplikácie. Zisťuje orientáciu zariadenia a volá ďalšie podstránky po kliknutí na požadované tlačidlo
        CustomCropping.js - stránka pre manuálne orezanie fotografie
        FaceReenactment.js - stránka volá endpointy na rozpohybovanie tvárí podľa nahraných videí
        FaceSelector.js - zobrazovanie jednolivých tvárí, správa nahrávia videí s pohybom patriacim jednotlivým osobám
        Main.js - renderuje základné prvky webu ako je hlavička, menu a päta stránky
        Manual.js - statická stránka 'Návod'
        PhotoUploader.js - stránka spustenia aplikacie, zahŕňa implementáciu čakacej fronty a funkciu nahrávania fotografie na server
        Terms.js - statická stránka 'Podmienky použitia'
        VideoMaker.js - stránka volaná po vytvorení rozpohybovaných jednotlivých tvárí. Volá ďalší enpoint na vytvorenie finálneho videa
                        nahradením orezaných častí rozpohybovaným videom v nahranej fotografii.
                        Zahŕňa integrovaný prehrávač videa priamo na stránke
        VideoRecorder.js - Statická stránka Webkamery. Slúži pre nahratie videa z webkamery

## Serverová časť aplikácie

    Zdrojový kód serverovej časti aplikácie sa nachádza v priečinku /src/backend/.
    Serverová časť aplikácie sa pre testovacie účely spúšťa pomocou príkazu python manage.py runserver v adresári /src/backend/
    Štandardne je spúšťaná na porte 8000, ale tento port je možné zmeniť pridaním požadovaného čísla portu za príkaz.
    Teda napríklad pre port 8080 by príkaz vyzeral takto: "python manage.py runserver 8080".
    Od jeho spustenia sú všetky akcie logované do súboru /src/django.log.
    --------------------------------------------------------------------------------------------------------------------------------
    Priečinok /src/ obsahuje:
        /backend/ - jednotlivé endpointy a skripty. Budú popísané detailne ďalej.
        /backend_config/ - obsahuje konfiguračné súbory a nastavenia servera. Automatický vygenerované Django aplikáciou, bez zásadných zmien
        /media/ - adresár slúži na ukladanie dočasných súborov vytvorených počas používania aplikácie.
                V adresári /media/results sú uložené výsledné vygenerované videá
        django.log - logy serverovej časti aplikácie
        db.sqlite3 - databáza aplikácie
        manage.py - hlavný spúšťací bod Djago aplikácie
    --------------------------------------------------------------------------------------------------------------------------------
    Priečinok /src/backend/ obsahuje:
        /custom_image_cropping/ - orezava obrazok podla poskytnutych suradnic a upravuje subor so suradnicami orezanych oblasti
        /face_detector/ - Automaticky deteguje tvare na fotografii.
                        Nasledne vytvori bounding-boxy okolo jednotlivych tvari a oreze vstupnu fotografiu na obrazky jednotlivych tvari osob.
        /face_reenactment/ - rozpohybovanie tvari podla nahraneho videa.
                        Zdrojovy kod v adresari /backend/face_reenactment/ je prevzaty z: https://github.com/sky24h/Face_Animation_Real_Time
                        Povodny autor kodu: sky24h
                        Upraveny bol iba subor: /src/backend/face_reenactment/camera_local.py
        /models/ - implementacia triedy SystemState na spravu stavu aktivity systemu,
                    implementacia triedy QueueItem na spravu uzivatelov cakajucich vo fronte na uvolnenie zdrojov pre spustenie aplikacie
        /video_maker/ - vytvara video z povodneho obrazku nahradenim jednotlivych bouding-boxov videom
