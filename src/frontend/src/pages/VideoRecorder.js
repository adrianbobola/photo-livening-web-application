/*
Project: Aplikace pro oziveni fotek
Author: Adrian Bobola
Email: xbobol00@stud.fit.vutbr.cz
University: FIT VUT Brno
Created on: 2024-05-09
*/

import React, {useState, useRef, useEffect} from "react";
import Webcam from 'react-webcam';
import {useTranslation} from 'react-i18next';
import {Link} from 'react-router-dom';

/**
 * Staticka stranka Webkamery
 * Umoznuje uzivatelovi nahranie pozadovaneho videa pohybu tvare priamo z jeho webkamery
 * Po nahrani videa dojde k jeho ulozeniu do zariadenia uzivatela pod nazvom video.webm
 *
 * Nepodporuje zariadenie iPad. Toto zariadenie ma moznost nahrania videa z kamery priamo po kliknuti na tlacidlo
 * 'Vybrat pozadovany subor' a nepotrebuje tuto komponentu.
 */
function VideoRecorder() {
    const {t} = useTranslation();
    const [isIPad, setIsIPad] = useState(false);
    const webcamReference = useRef(null);
    const recorderReference = useRef(null);
    const [isRecording, setIsRecording] = useState(false);
    const [videoData, setVideoData] = useState([]);

    useEffect(() => {
        // Detekcia iPadu, ten ma moznost nahrat video priamo pri nahravani video suboru danej tvari
        const isiPad = navigator.userAgent.match(/iPad/i);
        setIsIPad(!!isiPad);
    }, []);

    // Priradenie nahraneho videa premennej
    const appendVideo = ({data}) => {
        if (data && data.size > 0) {
            setVideoData(currentSegments => currentSegments.concat(data));
        }
    };

    // Akcia pre zapnutie nahravania videa z webkamery uzivatela
    const startRecording = () => {
        setIsRecording(true);
        const options = {mimeType: "video/webm"};
        const mediaRecorder = new MediaRecorder(webcamReference.current.stream, options);
        recorderReference.current = mediaRecorder;
        mediaRecorder.ondataavailable = appendVideo;
        mediaRecorder.start();
    };

    // Akcia pre vypnutie nahravania videa z webkamery uzivatela
    const stopRecording = () => {
        if (recorderReference.current) {
            recorderReference.current.stop();
        }
        setIsRecording(false);
    };

    // Akcia pre stiahnutie videa do zariadenia uzivatela
    const downloadVideo = () => {
        if (videoData.length > 0) {
            const videoBlob = new Blob(videoData, {type: "video/webm"});
            const videoUrl = URL.createObjectURL(videoBlob);
            const downloadLink = document.createElement("a");
            document.body.appendChild(downloadLink);
            downloadLink.href = videoUrl;
            downloadLink.download = "video.webm";
            downloadLink.click();
            URL.revokeObjectURL(videoUrl);
            setVideoData([]);
        }
    };

    if (isIPad) {
        return (
            <div className="rectangle-manual-page">
                <h2>{t('iPadNotSupported')}</h2>
                <div style={{display: 'flex', alignItems: 'center'}}>
                    <Link to="/FaceSelector" className="button-small"
                          style={{marginLeft: '200px', marginRight: '200px'}}>
                        {t('back')}
                    </Link>
                </div>
            </div>
        );
    }

    return (
        <div>
            <div className="rectangle-manual-page">
                <h1>{t('VideoRecorder')}</h1>
                <div style={{display: 'flex', alignItems: 'center'}}>
                    <Link to="/FaceSelector" className="button-small"
                          style={{marginLeft: '200px', marginRight: '200px'}}>
                        {t('back')}
                    </Link>
                </div>
                <br/>

                <Webcam
                    className="webcam-display"
                    audio={false}
                    mirrored={true}
                    ref={webcamReference}
                    videoConstraints={{
                        width: 1920,
                        height: 1080,
                        facingMode: "user",
                        frameRate: {ideal: 60, max: 60}
                    }}
                />
                <br/>
                <br/>

                {isRecording ? (
                    <button className="button-small" onClick={stopRecording}>{t('stop')}</button>
                ) : (
                    <button className="button-small" onClick={startRecording}>{t('start')}</button>
                )}
                {videoData.length > 0 && (
                    <button className="button-small" style={{marginLeft: '20px'}}
                            onClick={downloadVideo}>{t('download')}</button>
                )}
                <br/>
                <br/>
            </div>
        </div>
    );
}

export default VideoRecorder;