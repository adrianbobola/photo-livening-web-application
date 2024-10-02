/*
Project: Aplikace pro oziveni fotek
Author: Adrian Bobola
Email: xbobol00@stud.fit.vutbr.cz
University: FIT VUT Brno
Created on: 2024-05-09
*/

import "../index.css";
import React from "react";
import {useTranslation} from "react-i18next";
import {Link} from "react-router-dom";

/**
 * Staticka stranka 'O aplikacii'
 * Renderuje zakladne informacie o tomto projekte
 */
function About() {
    const {t} = useTranslation();
    return (
        <div>
            <div className="rectangle-file-uploading">
                <h1>
                    {t('about')}
                </h1>
                <div style={{display: 'flex', alignItems: 'center'}}> {}
                    <Link to="/" className="button-small"
                          style={{marginLeft: '200px', marginRight: '200px'}}>
                        {t('back')}
                    </Link>
                </div>
                <div className="about-container">
                    {t('about1')}
                    <br/><br/>
                    {t('about2')}
                    <br/>
                    {t('about3')}
                    <br/><br/>
                    {t('about4')}
                    <br/>
                    {t('about5')}
                    <br/><br/>
                    {t('about6')}
                    <br/>
                    {t('about7')}
                    <br/><br/>
                    {t('about8')}
                    <br/>
                    {t('about9')}
                    <br/>
                    {t('about10')}
                    <br/>
                    {t('about11')}
                    <br/><br/>
                    <nav className="nav">
                        <Link to="/" className="button-small">
                            {t('back')}
                        </Link>
                    </nav>
                </div>
            </div>
        </div>
    );
}

export default About;