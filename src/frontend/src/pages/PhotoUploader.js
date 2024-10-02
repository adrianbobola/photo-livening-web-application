/*
Project: Aplikace pro oziveni fotek
Author: Adrian Bobola
Email: xbobol00@stud.fit.vutbr.cz
University: FIT VUT Brno
Created on: 2024-05-09
*/

import React, {useEffect, useState} from "react";
import {Link, useNavigate} from 'react-router-dom';
import {useTranslation} from 'react-i18next';
import '../i18n';

/**
 * Stranka spustenia aplikacie, zahrna implementaciu cakacej fronty pre uvolnenie dostupnych prostriedkov
 * Obsahuje funkciu nahravania povodnej fotografie na server
 */
const PhotoUploader = () => {
    const navigate = useNavigate();
    const {t} = useTranslation();
    const [queuePosition, setQueuePosition] = useState(null);
    const [queueTimeWaiting, setqueueTimeWaiting] = useState(null);
    const [error, setError] = useState('');
    const [allowed, setAllowed] = useState(false);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        let isMounted = true;

        // Kontrola pristupu k stranke a sprava cakacej fronty uzivatelov
        const checkAccess = async () => {
            const user_token = localStorage.getItem('user_token');

            try {
                const backendUrl = process.env.REACT_APP_BACKEND_URL;
                const response = await fetch(`${backendUrl}/users/access/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: `user_token=${user_token}`,
                });

                const data = await response.json();

                if (isMounted) {
                    if (response.status === 200) {
                        setAllowed(true);
                    } else if (response.status === 202) {
                        // Uzivatel bol zaradeny do cakacej fronty, uloz si ziskane udaje pre vypis uzivatelovi
                        setQueuePosition(data.user_in_queue);
                        const queueWaitingTime = 5 * Number(data.user_in_queue);
                        setqueueTimeWaiting(queueWaitingTime);
                        setTimeout(() => {
                            if (isMounted) {
                                checkAccess();
                            }
                        },
                            // Nahodne od 4 do 13 sekund posielam poziadavku
                            Math.random() * (13000 - 4000) + 4000);
                    } else {
                        setError(data.error || 'Unknown error');
                    }
                }
            } catch (error) {
                if (isMounted) {
                    setError(t('connection_error'));
                    alert(t('connection_error'));
                    console.error(error);
                }
            }
        };
        checkAccess();

        return () => {
            isMounted = false;
        };
    }, [t]);

    // Nahravanie statickej fotografie na server, zahrna volanie endpointu na vycistenie prostredia od nepotrebnych
    // suborov predchadzajuceho behu aplikacie
    const handleImageUpload = async (event, index) => {
        const file = event.target.files[0];
        // Povolene typy nahravanych fotografii
        const allowedImageFormats = ["image/jpg", "image/jpeg"];

        // Premenuj nahrany obrazok na input.jpg
        const renamedFile = new File([file], 'input.jpg', {type: file.type});

        // Zly format obrazka
        if (!allowedImageFormats.includes(renamedFile.type)) {
            alert(t('error_fileformat_photo'));
            event.target.value = null;
            return;
        }

        // Vytvorenie tela endpointu pre nahranie obrazku na server
        const formData = new FormData();
        formData.append("image", renamedFile);

        // Cistenie prostredia od predchadzajuceho behu aplikacie
        try {
            const backendUrl = process.env.REACT_APP_BACKEND_URL;
            const deleteResponse = await fetch(`${backendUrl}/environment/cleanup/`, {
                method: "DELETE",
            });

            if (!deleteResponse.ok) {
                alert(t('error_clean') + deleteResponse.status)
            }
        } catch (error) {
            alert(t('connection_error'));
            console.error(error);

            if (error instanceof TypeError) {
                alert(t('connection_error'));
            } else {
                alert(error.message);
            }
        }

        // Nahravanie obrazku na server
        try {
            const backendUrl = process.env.REACT_APP_BACKEND_URL;
            setLoading(true);
            const uploadResponse = await fetch(`${backendUrl}/images/upload/`, {
                method: "POST",
                body: formData,
            });

            setLoading(true);
            if (!uploadResponse.ok) {
                alert(t('error_upload') + uploadResponse.status)
            }
        } catch (error) {
            console.error(error);
            alert(error.message);
        }

        // Spustenie automatickej detekcie tvari na fotografii a jej orezanie na jednotlive casti
        try {
            const backendUrl = process.env.REACT_APP_BACKEND_URL;
            const detectorResponse = await fetch(`${backendUrl}/faces/detect/`, {
                method: "GET",
            });

            if (detectorResponse.ok) {
                navigate('/FaceSelector');
            } else {
                alert(t('error_detection') + detectorResponse.status)
            }
        } catch (error) {
            setLoading(false);
            console.error(error);
            alert(error.message);
        }
    };

    return (
        <div className="content">
            {loading ? (
                <div className="rectangle-file-uploading">
                    <h2>{t('loading')}</h2>
                    <img src={`${process.env.PUBLIC_URL}/images/loading.gif`} alt="Loading"
                         style={{width: '250px', height: '250px'}}/>
                </div>
            ) : (
                <>
                    {allowed ? (
                        <div className="rectangle-file-uploading">
                            <center>
                                <h2>{t('nahrajte_foto')}</h2>
                                <div>
                                    <br/>
                                    <br/>
                                    <label htmlFor="file-upload" className="custom-file-upload-upload-page">
                                        {t('upload')}
                                    </label>
                                    <input
                                        id="file-upload"
                                        type="file"
                                        accept=".jpg"
                                        onChange={handleImageUpload}
                                    />
                                </div>

                                <div className="terms-upload-page"><br/><br/><br/>
                                    {t('souhlas')} <br/> {t('souhlas_2')}{' '}
                                    <Link to="/terms" style={{color: 'white'}}>{t('podmienky_page')}</Link>
                                </div>
                            </center>
                        </div>
                    ) : error ? (
                        error
                    ) : (
                        <div className="rectangle-file-uploading">
                            <br/>
                            <h2>{t('system_busy')}
                                <br/><br/><br/>
                                {t('queue_info')} {queuePosition}
                                <br/><br/>
                                {t('queue_waiting')} {queueTimeWaiting} {t('minutes')}
                            </h2>
                            <br/>
                            <br/>
                            <img src={`${process.env.PUBLIC_URL}/images/loading.gif`} alt="Loading"
                                 style={{width: '250px', height: '250px'}}/>
                        </div>
                    )}
                </>
            )}
        </div>
    );
};

export default PhotoUploader;
