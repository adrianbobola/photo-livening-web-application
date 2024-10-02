/*
Project: Aplikace pro oziveni fotek
Author: Adrian Bobola
Email: xbobol00@stud.fit.vutbr.cz
University: FIT VUT Brno
Created on: 2024-05-09
*/

import React, {useEffect, useState} from "react";
import {Link} from 'react-router-dom';
import {useTranslation} from 'react-i18next';
import '../i18n';

/**
 * Zobrazovanie jednolivych tvari, sprava nahravia videi s pohybom patriacim jednotlivym osobam
 * Zahrna premenovanie nahravanych video suborov podla id_tvare, ktorej ma byt pohyb prideleny
 */
const FaceSelector = () => {
    const {t} = useTranslation();
    const [imageUploaded, setImageUploaded] = useState(false);
    const [selectedFile, setSelectedFile] = useState(null);
    const [faceImages, setFaceImages] = useState([]);
    const [numberOfFaces, setNumberOfFaces] = useState(0);
    const [numberOfVideos, setNumberOfVideos] = useState(0);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        // Zistenie vytvorenych orezanych obrazkov tvari z povodnej fotografie
        const handleCroppedFacesImages = async () => {
            // Po prvom spusteni nastav na 0, az kym ti nevrati server nejaky pocet
            setNumberOfVideos(0);
            try {
                const backendUrl = process.env.REACT_APP_BACKEND_URL;
                const getDataResponse = await fetch(`${backendUrl}/faces/count/`);
                if (!getDataResponse.ok) {
                    alert(t('error_get'));
                }

                // Ulozenie poctu tvari z odpovede
                setImageUploaded(true);
                const data = await getDataResponse.json();
                const numFaces = data.nb_of_faces;
                setNumberOfFaces(numFaces);

                if (numFaces > 0) {
                    // Nacitavanie obrazkov jednotlivych tvari
                    const images = Array.from({length: numFaces}, (_, index) => {
                        const timestamp = new Date().getTime();
                        // Casove razitko z dovodu nacitavania starych obrazkov z cache pamati prehliadaca
                        return `${backendUrl}/uploads/${index}.png?${timestamp}`;
                    });
                    setFaceImages(images);
                } else {
                    setFaceImages([]);
                }

                setError(null);
            } catch (error) {
                console.error(error);
                setError(error.message);
            }
        };

        handleCroppedFacesImages();
    }, [t]);

    // Kontrola typu nahravaneho video suboru
    const handleFileChange = (event, index) => {
        const file = event.target.files[0];
        const allowedVideoFormats = ["video/mp4", "video/webm", "video/quicktime", "video/MOV",
            "video/avi", "video/mkv"];
        if (index !== undefined && !allowedVideoFormats.includes(file.type)) {
            alert(t('error_fileformat_video') + " Aktualne: " + file.type);
            event.target.value = null;
            return;
        }
        setSelectedFile({file, extension: file.type.split("/")[1], index});
    };

    // Nahravanie vido suboru na server
    const handleVideoUpload = async (index) => {
        if (!selectedFile) {
            alert(t('select_file'));
            return;
        }

        // Premenovanie videa podla indexu tvare, ktorej bude pridelene
        const formData = new FormData();
        // Video je v tvare <face:id>_driving.<format>
        const renamedFileName = `${index}_driving.${selectedFile.extension}`;
        formData.append("video", selectedFile.file, renamedFileName);

        try {
            const backendUrl = process.env.REACT_APP_BACKEND_URL;
            // Nastav loading pre uzivatela, nech vie ze sa nahrava video a ma cakat
            setLoading(true);
            const response = await fetch(`${backendUrl}/videos/upload/`, {
                method: "POST",
                body: formData,
            });
            // Ukoncenie loadingu pre uzivatela, video bolo nahrane
            setLoading(false);
            setNumberOfVideos(numberOfVideos + 1);

            if (!response.ok) {
                alert(t('error_upload') + response.status);
            } else {
                alert("Ok");
            }
            setError(null);
        } catch (error) {
            setLoading(false);
            console.error(error);
            setError(error.message);
        }
    };

    return (
        <div className="content">
            {loading && (
                <div className="rectangle-file-uploading">
                    <h2>{t('loading')}</h2>
                    <img src={`${process.env.PUBLIC_URL}/images/loading.gif`} alt="Loading"
                         style={{width: '250px', height: '250px'}}/>
                </div>
            )}

            {!loading && numberOfFaces === 0 && !error && (
                <div className="error">
                    <div className="error-rectangle">
                        <h2>{t('error_not_face')}</h2>
                        <h3>{t('error_try_another')}</h3>
                        <div style={{alignItems: 'center', display: 'flex', justifyContent: 'center'}}>
                            <Link to="/CustomCropping" className="custom-file-upload-upload-page"
                                  style={{marginLeft: '200px', marginRight: '200px', textDecoration: 'none'}}>
                                {t('custom_face')}
                            </Link>
                            <Link to="/PhotoUploader" className="custom-file-upload-upload-page"
                                  style={{textDecoration: 'none'}}>
                                {t('back')}
                            </Link>
                        </div>
                    </div>
                </div>
            )}

            {!loading && numberOfFaces > 0 && imageUploaded && (
                <div className="rectangle">
                    <h2>{t('upload_video')}</h2>
                    <div style={{display: 'flex', alignItems: 'center'}}>
                        <Link to="/PhotoUploader" className="button-small"
                              style={{marginLeft: '50px', marginRight: '20px'}}>
                            {t('back')}
                        </Link>
                        <Link to="/CustomCropping" className="button-small" style={{marginRight: '20px'}}>
                            {t('custom_face')}
                        </Link>
                        <Link to="/VideoRecorder" className="button-small">
                            {t('VideoRecorder')}
                        </Link>
                        {numberOfVideos > 0 && (
                            <Link to="/FaceReenactment" className="button-small" style={{marginLeft: '50px'}}>
                                {t('next')}
                            </Link>
                        )}
                    </div>
                    <table className="center">
                        <tbody>
                        {faceImages.map((imageUrl, index) => (
                            <tr key={index}>
                                <td><img src={imageUrl} alt={`Face ${index + 1}`}
                                         style={{maxWidth: "200px", maxHeight: "200px", margin: "5px"}}/></td>
                                <td>
                                    <input type="file" accept=".mp4,.webm,.MOV,.avi,.mkv,.quicktime"
                                           onChange={(event) => handleFileChange(event, index)}/>
                                    <button className="button-small"
                                            onClick={() => handleVideoUpload(index)}>{t('upload_video_btn')}</button>
                                </td>
                            </tr>
                        ))}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
};

export default FaceSelector;
