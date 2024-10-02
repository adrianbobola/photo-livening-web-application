/*
Project: Aplikace pro oziveni fotek
Author: Adrian Bobola
Email: xbobol00@stud.fit.vutbr.cz
University: FIT VUT Brno
Created on: 2024-05-09
*/

import i18n from 'i18next';
import {initReactI18next} from 'react-i18next';

import translEN from './locales/en.json';
import translSK from './locales/sk.json';

// Jazykova podpora obsahu stranok
const resources = {
    en: {
        translation: translEN
    },
    sk: {
        translation: translSK
    }
};

i18n
    .use(initReactI18next)
    .init({
        resources,
        // predvoleny jazyk sk
        lng: 'sk',
        fallbackLng: 'en',

        interpolation: {
            escapeValue: false
        }
    });

export default i18n;
