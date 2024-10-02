/*
Project: Aplikace pro oziveni fotek
Author: Adrian Bobola
Email: xbobol00@stud.fit.vutbr.cz
University: FIT VUT Brno
Created on: 2024-05-09
*/

import React, {useState, useEffect} from "react";
import {useTranslation} from 'react-i18next';
import "../index.css";
import '../i18n';

/**
 * Stranka volana po vytvoreni rozpohybovanych jednotlivych tvari
 * Vola dalsi enpoint na vytvorenie finalneho videa nahradenim vyrezanych casti rozpohybovanym videom v nahranej fotografii
 * Zahrna integrovany prehravac videa priamo na stranke
 */
const VideoMaker = () => {
    const {t} = useTranslation();
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    // Vstavany prehravac vytvoreneho videa priamo na stranke aplikacii
    const VideoPlayer = () => {
        let user_token = localStorage.getItem('user_token');
        const backendUrl = process.env.REACT_APP_BACKEND_URL;
        const videoSource = `${backendUrl}/videos/result/${user_token}/`;

        // Stiahnutie video suboru do zariadenia uzivatela
        const handleDownload = async () => {
            try {
                const response = await fetch(videoSource);
                if (!response.ok) {
                    alert('Network response was not ok');
                }
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = "video.mp4";
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
            } catch (err) {
                console.error("Failed to download video: ", err);
            }
        };

        return (
            <div className="video-player">
                <br/><br/>
                <video width="500" controls autoPlay loop>
                    <source src={videoSource} type="video/mp4"/>
                    Prehliadac nepodporuje zobrazenie videa.
                    Web browser does not support to show a video.
                </video>
                <br/><br/>
                <button className="button-small" onClick={handleDownload}>{t('download_button')}</button>
            </div>
        );
    };

    // Volanie endpointu pre vytvorenie finalneho videa nahradenim rozpohybovanych casti v nahranej fotografii
    const runScript = async () => {
        let user_token = localStorage.getItem('user_token');

        try {
            const backendUrl = process.env.REACT_APP_BACKEND_URL;
            const response = await fetch(`${backendUrl}/videos/result/generate/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `user_token=${user_token}`,
            });
            const data = await response.json();

            if (!response.ok) {
                alert('Failed. Server returned status code: ' + response.status);
            }

            setLoading(false);
            return data.error === 'no' ? 'SUCCESS' : 'Unknown error occurred';
        } catch (error) {
            console.error(error);
            setError("Error occurred while running script");
            setLoading(false);
            throw error;
        }
    };

    useEffect(() => {
        runScript();
    }, []);


    return (
        <div>
            {loading ? (
                <div className="rectangle-file-uploading">
                    <br/><h2>  {t('loading')}</h2><br/><br/>
                    <img src={`${process.env.PUBLIC_URL}/images/loading.gif`} alt="Loading"
                         style={{width: '250px', height: '250px'}}/>
                </div>
            ) : error ? (
                error
            ) : (
                <div className="rectangle-file-uploading">
                    <br/>
                    <h2> {t('done')} </h2>
                    <br/>
                    <VideoPlayer/>
                </div>
            )}
        </div>
    );
};

export default VideoMaker;
