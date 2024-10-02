/*
Project: Aplikace pro oziveni fotek
Author: Adrian Bobola
Email: xbobol00@stud.fit.vutbr.cz
University: FIT VUT Brno
Created on: 2024-05-09
*/

import React, {useRef, useEffect, useState} from 'react';
import {Stage, Layer, Rect, Transformer, Image as KonvaImage} from 'react-konva';
import useImage from 'use-image';
import {Link} from "react-router-dom";
import {useTranslation} from "react-i18next";
import "../index.css";
import '../i18n';

/**
 * Zistenie velkosti aktualneho viewpointu pre zobrazenie fotografie a pouzitie konvy
 */
const useViewportSize = () => {
    // Definovane velkosti hlavicky a paty stranky, ktore treba odcitat od celeho viewpointu
    const headerHeight = 80;
    const footerHeight = 160;

    const calculateSize = () => ({
        width: window.innerWidth - 50,
        height: window.innerHeight - headerHeight - footerHeight
    });

    const [size, setSize] = useState(calculateSize);

    useEffect(() => {
        const handleResize = () => setSize(calculateSize());
        window.addEventListener('resize', handleResize);
        return () => window.removeEventListener('resize', handleResize);
    }, []);

    return size;
};

/**
 * Komponenta pre manualne orezanie fotografie
 */
const CustomCropping = () => {
    const {t} = useTranslation();
    const [imageUrl, setImageUrl] = useState("");
    const [image, status] = useImage(imageUrl);
    const viewportSize = useViewportSize();
    const [rect, setRect] = useState({x: 50, y: 50, width: 100, height: 100});
    const rectRef = useRef(null);
    const trRef = useRef(null);

    useEffect(() => {
        const timestamp = new Date().getTime();
        const backendUrl = process.env.REACT_APP_BACKEND_URL;
        // Casove razitko kvoli zobrazovanemu staremu obrazku z cache prehliadaca
        const imageUrl = `${backendUrl}/uploads/input.jpg?${timestamp}`;
        setImageUrl(imageUrl);
    }, []);

    useEffect(() => {
        if (trRef.current) {
            trRef.current.nodes([rectRef.current]);
            trRef.current.getLayer().batchDraw();
        }
    }, [rectRef, trRef]);

    const handleCropping = async () => {
        if (!image) return 1;
        // Vypocty kvoli zobrazovaniu zmensenej povodnej fotografie na spravne umiestnenie do viewPointu
        // Pri zasielani suradnic umiestnenho bouding-boxu je potrebne zohladnit scale zobrazovaneho obrazku
        // a vypocitat spatne suradnice
        const scaleX = image.width / scaledWidth;
        const scaleY = image.height / scaledHeight;
        let correctedRectX = Math.max(0, (rect.x - xPosition) * scaleX);
        let correctedRectY = Math.max(0, (rect.y - yPosition) * scaleY);
        let originalRectWidth = Math.min(image.width, rect.width * scaleX);
        let originalRectHeight = Math.min(image.height, rect.height * scaleY);

        // Nesmie presahovat povodny obrazok, ak presahuje nastav hodnotu z velkosti fotografie
        correctedRectX = Math.min(correctedRectX, image.width - originalRectWidth);
        correctedRectY = Math.min(correctedRectY, image.height - originalRectHeight);

        try {
            // Vytvaranie tela endpointu so suradnicami umiestneneho bouding-boxu, po zohladneni scale parametru
            const formData = new FormData();
            formData.append('x', correctedRectX);
            formData.append('y', correctedRectY);
            formData.append('width', originalRectWidth);
            formData.append('height', originalRectHeight);

            const backendUrl = process.env.REACT_APP_BACKEND_URL;
            const response = await fetch(`${backendUrl}/images/cropping/`, {
                method: "POST",
                body: formData,
            });

            if (!response.ok) {
                alert(t('error_upload') + response.status)
            } else {
                alert("Ok");
            }
        } catch (error) {
            console.error(error);
        }
    };

    // Vypocet skalovania obrazku pre spravne umiestnenie do viewPointu aby nevycnieval zo stranky
    const getScaledImageSize = () => {
        if (status !== 'loaded' || !image) return {width: 0, height: 0};
        const maxWidth = 800;
        const maxHeight = 800;
        const imgRatio = image.width / image.height;
        let width, height;

        if (maxWidth / maxHeight < imgRatio) {
            width = maxWidth;
            height = maxWidth / imgRatio;
        } else {
            height = maxHeight;
            width = maxHeight * imgRatio;
        }

        return {width, height};
    };

    const {width: scaledWidth, height: scaledHeight} = getScaledImageSize();
    const xPosition = (viewportSize.width - scaledWidth) / 2;
    const yPosition = (viewportSize.height - scaledHeight) / 2;

    return (
        <div>
            <h2 style={{color: 'white'}}>{t('cropping')}</h2>
            <button
                className="button-small"
                onClick={() => handleCropping()}
                style={{marginRight: '50px'}}
            >
                {t('crop')}
            </button>
            <Link to="/FaceSelector" className="button-small">
                {t('continue')}
            </Link>
            <Stage width={viewportSize.width} height={viewportSize.height}>
                <Layer>
                    <KonvaImage
                        image={image}
                        width={scaledWidth}
                        height={scaledHeight}
                        x={xPosition}
                        y={yPosition}
                    />
                    <Rect
                        ref={rectRef}
                        x={rect.x}
                        y={rect.y}
                        width={rect.width}
                        height={rect.height}
                        fill="transparent"
                        stroke="red"
                        draggable
                        onDragEnd={(e) => setRect({
                            x: e.target.x(),
                            y: e.target.y(),
                            width: rect.width,
                            height: rect.height
                        })}
                        onTransformEnd={() => {
                            const node = rectRef.current;
                            const scaleX = node.scaleX();
                            const scaleY = node.scaleY();
                            node.scaleX(1);
                            node.scaleY(1);
                            setRect({
                                x: node.x(),
                                y: node.y(),
                                width: Math.max(5, node.width() * scaleX),
                                height: Math.max(5, node.height() * scaleY)
                            });
                        }}
                    />
                    <Transformer
                        ref={trRef}
                        boundBoxFunc={(oldBox, newBox) => newBox.width < 5 || newBox.height < 5 ? oldBox : newBox}
                    />
                </Layer>
            </Stage>
        </div>
    );
};

export default CustomCropping;
