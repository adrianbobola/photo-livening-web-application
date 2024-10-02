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
 * Staticka stranka 'Podmienky pouzitia'
 * Renderuje text podmienok pouzitia aplikacie v zvolenom jazyku
 */
function Terms() {
    const {t} = useTranslation();
    return (
        <div>
            <div className="rectangle-file-uploading">
                <h1>
                    {t('terms')}
                </h1>
                <div style={{display: 'flex', alignItems: 'center'}}> {}
                    <Link to="/" className="button-small"
                          style={{marginLeft: '200px', marginRight: '200px'}}>
                        {t('back')}
                    </Link>
                </div>
                <div className="about-container">
                    {t('terms_1')}
                    <br/>
                    {t('terms_2')}
                    <br/>
                    {t('terms_3')}
                    <br/>
                    {t('terms_4')}
                    <br/>
                    {t('terms_5')}
                    <br/>
                    {t('terms_6')}
                    <br/>
                    {t('terms_7')}
                    <br/><br/>
                    <div style={{color: 'black', fontStyle: 'italic'}}>{t('terms_date')}</div>
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

export default Terms;