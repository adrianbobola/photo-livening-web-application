/*
Project: Aplikace pro oziveni fotek
Author: Adrian Bobola
Email: xbobol00@stud.fit.vutbr.cz
University: FIT VUT Brno
Created on: 2024-05-09
*/

import React, {useState, useEffect} from "react";
import {BrowserRouter as Router, Route, Routes, Link} from 'react-router-dom';
import {useTranslation} from 'react-i18next';

import "../index.css";
import '../i18n';

import iconEN from '../assets/icon-en.png';
import iconSK from '../assets/icon-sk.png';

import AppStart from "./AppStart";
import PhotoUploader from "./PhotoUploader";
import About from './About';
import Terms from "./Terms";
import Manual from "./Manual";
import FaceReenactment from "./FaceReenactment";
import FaceSelector from "./FaceSelector"
import VideoMaker from "./VideoMaker";
import CustomCropping from "./CustomCropping";
import VideoRecorder from "./VideoRecorder";

/**
 * Renderuje zakladne prvky webu ako je hlavicka, menu a pata stranky
 * Obsahuje definicie tras jednotlivych podstranok
 */
function Main() {
    const {t, i18n} = useTranslation();
    const [actualLanguage, setLanguage] = useState(i18n.language);

    // Komponenta pre podporu roznych jazykov
    useEffect(() => {
        i18n.changeLanguage(actualLanguage);
    }, [actualLanguage, i18n]);

    // Zmena loga stranky podla nastaveneho jazyka
    useEffect(() => {
        document.title = t('logo');
    }, [t]);

    // Prepinac jazykov
    const toggleLanguage = () => {
        setLanguage((prevLanguage) => (prevLanguage === 'en' ? 'sk' : 'en'));
    };

    return (
        <Router>
            <div className="main-container">
                <header className="header">
                    <nav className="nav">
                        <Link to="/" className="logo"
                              style={{display: 'flex', alignItems: 'center', textDecoration: 'none', color: 'inherit'}}>
                            <img src={`${process.env.PUBLIC_URL}/images/fit_logo.png`} alt="FIT VUT Logo"
                                 style={{marginRight: '10px', width: '55px', height: 'auto'}}/>
                            {t('logo')}
                        </Link>
                        <Link to="/about" className="navbar-text" style={{textDecoration: 'none'}}>
                            {t('about')}
                        </Link>
                        <Link to="/terms" className="navbar-text" style={{textDecoration: 'none'}}>
                            {t('terms')}
                        </Link>
                        <Link to="/manual" className="navbar-text" style={{textDecoration: 'none'}}>
                            {t('manual')}
                        </Link>
                        <div onClick={toggleLanguage} style={{cursor: 'pointer'}}>
                            <img src={actualLanguage === 'en' ? iconSK : iconEN} alt='Language'
                                 style={{maxWidth: '30px'}}/>
                        </div>
                    </nav>
                </header>

                <Routes>
                    <Route path="/" element={<AppStart/>}/>
                    <Route path="/about" element={<About/>}/>
                    <Route path="/terms" element={<Terms/>}/>
                    <Route path="/manual" element={<Manual/>}/>
                    <Route path="/PhotoUploader" element={<PhotoUploader/>}/>
                    <Route path="/FaceSelector" element={<FaceSelector/>}/>
                    <Route path="/FaceReenactment" element={<FaceReenactment/>}/>
                    <Route path="/VideoMaker" element={<VideoMaker/>}/>
                    <Route path="/CustomCropping" element={<CustomCropping/>}/>
                    <Route path="/VideoRecorder" element={<VideoRecorder/>}/>
                </Routes>

                <footer className="footer">
                    <a href="https://www.fit.vut.cz/" target="_blank" rel="noopener noreferrer"
                       style={{color: 'inherit', textDecoration: 'none'}}>
                        © 2024 Adrian Bobola | FIT VUT Brno
                    </a>
                </footer>
            </div>
        </Router>
    );
}

export default Main;
