/*
Project: Aplikace pro oziveni fotek
Author: Adrian Bobola
Email: xbobol00@stud.fit.vutbr.cz
University: FIT VUT Brno
Created on: 2024-05-09
*/

import React, {useState, useEffect, useRef} from "react";
import {Link} from 'react-router-dom';
import {useTranslation} from "react-i18next";

/**
 * Rozpohybovanie tvari podla nahranych videi
 */
const FaceReenactment = () => {
    const [loading, setLoading] = useState(true);
    const [numberOfUploadedVideos, setNumberOfUploadedVideos] = useState(0);
    const [uploadedVideosNames, setUploadedVideosNames] = useState([]);
    const linkRef = useRef(null);
    const [error, setError] = useState(null);
    const {t} = useTranslation();

    useEffect(() => {
        // Ziskanie poctu uspesne nahranych videi pre rozpohybovanie tvare na server
        const getNumberOfVideos = async () => {
            try {
                const backendUrl = process.env.REACT_APP_BACKEND_URL;
                const response = await fetch(`${backendUrl}/videos/upload/count/`, {method: "GET"});
                if (!response.ok) {
                    alert('Failed. Server returned status code:' + response.status)
                }
                const responseBody = await response.json();
                if ('nb_of_uploaded_videos' in responseBody && 'uploaded_videos_names' in responseBody) {
                    // Ulozenie poctu nahranych videi s pohybom tvare a ich nazvy suborov
                    setNumberOfUploadedVideos(responseBody.nb_of_uploaded_videos);
                    setUploadedVideosNames(responseBody.uploaded_videos_names);
                } else {
                    console.error('Expected data not found in response body');
                }
            } catch (error) {
                console.error(error);
                alert("Error occurred while running script");
            }
        };
        getNumberOfVideos();
    }, []);

    useEffect(() => {
        // Funckia vola endpoint na rozpohybovanie zvolenej tvare
        const runScript = async (arrayIndex) => {
            try {
                // Kontrola typu nahranych video suborov na server
                const uploadedVideoName = uploadedVideosNames[arrayIndex];
                const fileNameRegex = /(.+)_driving\.(mp4|webm|MOV|avi|mkv|quicktime)$/;
                const match = uploadedVideoName.match(fileNameRegex);
                const fileName = match ? match[1] : null;

                if (!fileName) {
                    console.error("Error: Could not extract file name from uploaded video name.");
                    alert("Error occurred while running script");
                }

                // Priprava a volanie endpointu na rozpohybovanie danej tvare
                const backendUrl = process.env.REACT_APP_BACKEND_URL;
                const responseUrl = `${backendUrl}/faces/reenactment/${fileName}/`;
                const response = await fetch(responseUrl, {method: "GET"});

                if (!response.ok) {
                    alert('Failed. Server returned status code:' + response.status)
                }

                const data = await response.json();
                return data.error === 'no' ? 'SUCCESS' : 'Unknown error occurred';
            } catch (error) {
                alert("Error occurred while running script");
            }
        };

        // Pomocna funkcia vola runScript(i) podla poctu nahranych videi s pohybom uzivatela
        // Chceme aby sa pouzilo kazde nahrane video pohybu
        const initiateProcess = async () => {
            if (numberOfUploadedVideos > 0 && uploadedVideosNames.length > 0) {
                let successCount = 0;
                for (let i = 0; i < numberOfUploadedVideos; i++) {
                    const status = await runScript(i);
                    if (status === 'SUCCESS') {
                        successCount++;
                        if (successCount === numberOfUploadedVideos) {
                            setLoading(false);
                        }
                    } else {
                        console.error(`Script ${i} encountered an error.`);
                        alert("Error occurred while running script");
                        setError(true)
                        break;
                    }
                }
            }
        };

        initiateProcess();
    }, [numberOfUploadedVideos, uploadedVideosNames]);


    useEffect(() => {
        if (!loading && !error) {
            // Pre vsetky nahrane videa s pohybom boli vygenerovane rozpohybovane tvare, prepni URL na VideoMaker
            redirectToVideoMaker();
        }
    }, [loading, error]);

    // Neviditelne automaticke tlacidlo, ktore zabezpecuje prepnutie uzivatela na URL s komponentou VideoMaker
    const redirectToVideoMaker = () => {
        if (linkRef.current) {
            linkRef.current.click();
        }
    };

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
                <div>
                    <Link to="/VideoMaker" className="button-small" style={{display: 'none'}} ref={linkRef}>
                        Continue
                    </Link>
                </div>
            )}
        </div>
    );
};

export default FaceReenactment;
