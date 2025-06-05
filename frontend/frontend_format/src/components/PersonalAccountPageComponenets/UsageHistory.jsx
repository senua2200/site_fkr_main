import { useEffect, useState } from 'react';
import styles from '../layout/PersonalAccountPage/PersonalAccountPage.module.css'

export const UsegeHistory = () => {
    const [fileNames, setFileNames] = useState([]);

    const getHistory = () => {
        fetch('api/get_history/', {
            method: 'GET',
            credentials: 'include',
        })
        .then(res => res.json())
        .then(data => {
            if (data.length) {
                const latestFive = data.slice(-5).map(elem => {
                    const fileName = elem.file_path.split('/').pop().replace(/\.[^/.]+$/, '');
                    return {
                        fileName,
                        filePath: elem.file_path
                    };
                });

                setFileNames(latestFive);
            }
            else {
                setFileNames([]);
            }
        })
        .catch(err => {
            console.error(err);
            setFileNames([]);
        });
    };

    const handleDownload = async (filePath) => {
        try {
            const fileName = filePath.split('/').pop();
            const response = await fetch(`/api/download_by_path/?file_path=${encodeURIComponent(filePath)}`, {
                method: 'GET',
                credentials: 'include',
            });
    
            if (!response.ok) {
                throw new Error('Ошибка при загрузке файла');
            }
    
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
    
            const a = document.createElement('a');
            a.href = url;
            a.download = fileName; // или любое другое имя
            document.body.appendChild(a);
            a.click();
            a.remove();
            window.URL.revokeObjectURL(url);
        } catch (error) {
            console.error('Ошибка при скачивании файла:', error);
            alert('Не удалось скачать файл.');
        }
    };     

    useEffect(() => {
        getHistory();
    }, []);

    return (
        <section className={styles.usege_history}>
            <div className={styles.usege_history_container}>
                <div className={styles.usege_history_table}>
                    <div className={styles.usege_history_header}>
                        <span className={styles.header_name}>Название работы</span>
                        <span className={styles.header_page_count}>Количество страниц</span>
                        <span className={styles.header_type_price}>Тип оплаты</span>
                        <span className={styles.header_file_link}>Скачать файл</span>
                        <span className={styles.header_date}>Дата</span>
                    </div>
                    <div className={styles.all_elements}>
                        {fileNames.length > 0 && fileNames.map((file, i) => (
                            <div key={i} className={styles.element}>
                                <span className={styles.element_name}>{file.fileName}</span>
                                <span className={styles.element_page_count}>—</span>
                                <span className={styles.element_type_price}>—</span>
                                <button className={styles.element_file_link} onClick={() => handleDownload(file.filePath)}>Скачать</button>
                                <span className={styles.element_date}>—</span>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </section>
    );
};