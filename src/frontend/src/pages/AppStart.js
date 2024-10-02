/*
Project: Aplikace pro oziveni fotek
Author: Adrian Bobola
Email: xbobol00@stud.fit.vutbr.cz
University: FIT VUT Brno
Created on: 2024-05-09
*/

import React, {useEffect, useState} from "react";
import ReactPlayer from 'react-player/lazy';
import {Link} from 'react-router-dom';
import {useTranslation} from 'react-i18next';
import "../index.css";
import '../i18n';

/**
 * Uvodna stranka aplikacie
 * Zistuje orientaciu zariadenia a vola dalsie podstranky po kliknuti na pozadovane tlacidlo
 */
const AppStart = () => {
    const {t} = useTranslation();

    // Generovanie jedinecneho user tokenu z aktualneho casu
    const user_token = String(new Date().getTime());
    localStorage.setItem('user_token', user_token);

    // Ulozenie stavu orientacie zariadenia
    const [isLandscape, setIsLandscape] = useState(window.innerWidth > window.innerHeight);

    // Funkcia na zistovanie aktualneho stavu orientacie zariadenia
    const handleOrientationChange = () => {
        setIsLandscape(window.innerWidth > window.innerHeight);
    };

    // Event listener pri zmene orientacie zariadenia
    useEffect(() => {
        window.addEventListener('resize', handleOrientationChange);
        return () => {
            window.removeEventListener('resize', handleOrientationChange);
        };
    }, []);

    return (
        <div className="content">
            {isLandscape ? (
                <div className="content-container">
                    <div className="text-content">
                        <h1 className="title">
                            {t('ozivte_svoje')}<br/>{t('nudne_staticke')}<br/>{t('fotografie')}
                        </h1>
                        <div className="description">
                            {t('mozete_to_bezplatne')} <br/> {t('vyskusat_ihned')}
                        </div>
                        <div><br/><br/>
                            <Link to="/PhotoUploader" className="custom-file-upload" style={{textDecoration: 'none'}}>
                                {t('tryit')}
                            </Link>
                        </div>
                        <div className="terms"><br/><br/><br/>
                            {t('souhlas')} <br/> {t('souhlas_2')}{' '}
                            <Link to="/terms" style={{color: 'white'}}>{t('podmienky_page')} </Link>
                        </div>
                    </div>
                    <div className="video-player">
                        <ReactPlayer className="image" url='https://www.youtube.com/watch?v=XdYcLmnVLto' playing={true}
                                     loop={true} muted={true} controls={false}
                                     config={{youtube: {playerVars: {disable: 1}}}}
                        />
                    </div>
                </div>
            ) : (
                <div style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    height: '100vh',
                    textAlign: 'center',
                    backgroundColor: '#f0f0f0',
                    color: '#333'
                }}>
                    <h1>Prosím otočte svoje zariadenie na šírku, aby ste mohli spustiť aplikáciu.</h1>
                    <br/>
                    <h1>Please rotate your device to landscape mode to access this application.</h1>
                </div>
            )}
            <br/>
        </div>
    );
};

export default AppStart;
