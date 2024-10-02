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
 * Staticka stranka 'Navod'
 * Renderuje obrazkovy navod v zvolenom jazyku
 */
function Manual() {
    const {t} = useTranslation();
    return (
        <div>
            <div className="rectangle-manual-page">
                <h1>{t('manual')}</h1>
                <div style={{display: 'flex', alignItems: 'center'}}> {}
                    <Link to="/" className="button-small"
                          style={{marginLeft: '200px', marginRight: '200px'}}>
                        {t('back')}
                    </Link>
                </div>
                <br/>
                {t('manual1')}
                <br/>
                <br/>
                <img src={`${process.env.PUBLIC_URL}${t('manual1_img')}`}
                     style={{width: '600px'}} alt={"img1"}/>
                <br/>
                <br/>
                <br/>
                <br/>
                {t('manual2')}
                <br/>
                <br/>
                <img src={`${process.env.PUBLIC_URL}${t('manual2_img')}`}
                     style={{width: '600px'}} alt={"img2"}/>
                <br/>
                <br/>
                <br/>
                <br/>
                {t('manual3')}
                <br/>
                <br/>
                <img src={`${process.env.PUBLIC_URL}${t('manual3_img')}`}
                     style={{width: '600px'}} alt={"img3"}/>
                <br/>
                <br/>
                <br/>
                <br/>
                {t('manual4')}
                <br/>
                <br/>
                {t('manual4_1')}
                <br/>
                {t('manual4_2')}
                <br/>
                {t('manual6')}
                <br/>
                <br/>
                <img src={`${process.env.PUBLIC_URL}${t('manual6_img')}`}
                     style={{width: '600px'}} alt={"img6"}/>
                <br/> <br/>
                {t('manual4_3')}
                <br/>
                <br/>
                <img src={`${process.env.PUBLIC_URL}${t('manual4_img')}`}
                     style={{width: '600px'}} alt={"img4"}/>
                <br/>
                <br/>
                <br/>
                <br/>
                {t('manual5')}
                <br/> <br/>
                {t('manual5_1')}
                <br/>
                {t('manual5_2')}
                <br/>
                {t('manual5_3')}
                <br/>
                {t('manual5_4')}
                <br/>
                <br/>
                {t('manual5_5')}
                <br/>
                {t('manual5_6')}
                <br/>
                <br/>
                <img src={`${process.env.PUBLIC_URL}${t('manual5_img')}`}
                     style={{width: '600px'}} alt={"img5"}/>
                <br/>
                <br/>
                <br/>
                <br/>
                {t('manual7')}
                <br/><br/>
                {t('manual7_1')}
                <br/>
                <br/>
                <img src={`${process.env.PUBLIC_URL}${t('manual7_img')}`}
                     style={{width: '600px'}} alt={"img7"}/>
                <br/>
                <br/>
                <br/>
                <br/>
                {t('manual8')}
                <br/>
                <br/>
                {t('manual8_1')}
                <br/>
                <br/>
                <img src={`${process.env.PUBLIC_URL}${t('manual8_img')}`}
                     style={{width: '600px'}} alt={"img8"}/>
                <br/>
                <br/>

                <div style={{display: 'flex', alignItems: 'center'}}> {}
                    <Link to="/" className="button-small"
                          style={{marginLeft: '200px', marginRight: '200px'}}>
                        {t('back')}
                    </Link>
                </div>

            </div>
        </div>
    );
}

export default Manual;