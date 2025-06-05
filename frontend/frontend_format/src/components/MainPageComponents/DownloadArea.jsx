import word from '../../assets/word.svg'
import styles from '../layout/MainPage/MainPage.module.css'
import i1 from '../../assets/download/i1.svg'
import i2 from '../../assets/download/i2.svg'
import i3 from '../../assets/download/i3.svg'
import i4 from '../../assets/download/i4.svg'
import i5 from '../../assets/download/i5.svg'
import i6 from '../../assets/download/i6.svg'
import i7 from '../../assets/download/i7.svg'
import i8 from '../../assets/download/i8.svg'
import i9 from '../../assets/download/i9.svg'
import i10 from '../../assets/download/i10.svg'
import i1_2 from '../../assets/download/i1_2.svg'
import i2_2 from '../../assets/download/i2_2.svg'
import i3_2 from '../../assets/download/i3_2.svg'
import i4_2 from '../../assets/download/i4_2.svg'
import i5_2 from '../../assets/download/i5_2.svg'
import i6_2 from '../../assets/download/i6_2.svg'
import i7_2 from '../../assets/download/i7_2.svg'
import i8_2 from '../../assets/download/i8_2.svg'
import i9_2 from '../../assets/download/i9_2.svg'
import i10_2 from '../../assets/download/i10_2.svg'
import { ModalVariantChoice } from '../ModalWindow/ModalVariantChoice';
import { useEffect, useState, useCallback } from 'react'
import { ModalParameters } from '../ModalWindow/ModalParameters';
import { useDropzone } from 'react-dropzone';


export const DownloadArea = () => {
    const [isOpen, setIsOpen] = useState(false);
    const [isOpenParamModal, setIsOpenParamModal] = useState(false);

    const onDrop =  useCallback((acceptedFiles) => {
        if (acceptedFiles.length === 0) {
            console.log('Файл отклонен: неверный тип');
            return;
        }
        else {
            console.log("Загруженные файлы:", acceptedFiles);
            const fileData = new FormData();
            fileData.append('file', acceptedFiles[0]);
            sendFile(fileData);
        }
    }, []);

    const sendFile = async (fileData) => {
        const response = await fetch('api/get_user_file/', {
            method: 'POST',
            credentials: 'include',
            body: fileData,
        });

        const data = await response.json();

        if (!response.ok) {
            console.log('Ошибка');
            if (data.error) {
                console.log(data.error);
            }
        }
        else {
            console.log('Ответ сервера:', data);
        }
    }

    const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop, 
        accept: {'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx']},
        multiple: false
    });

    useEffect(() => {
        if (isOpen || isOpenParamModal){
            document.body.style.overflow = "hidden";
        }
        else{
            document.body.style.overflow = "";
        }
    });

    return (
        <section className={styles.download_area}>
            <div className={styles.container_download_area} {...getRootProps()}>
                <input type="file" {...getInputProps()} />
                <div className={styles.l_area_svg}>
                    <img src={i1} alt="" />
                    <img src={i9} alt="" />
                    <img src={i10} alt="" />
                    <img src={i8} alt="" />
                    <img src={i2} alt="" />
                    <img src={i4} alt="" />
                    <img src={i7} alt="" />
                    <img src={i5} alt="" />
                    <img src={i3} alt="" />
                    <img src={i6} alt="" />
                </div>
                <div className={styles.download} onClick={() => {setIsOpen(true)}}>
                    <span>Нажмите для выбора файла</span>
                    <img src={word} alt="word_svg"/>
                    <span>Или перетащите его сюда</span>
                </div>
                <div className={styles.r_area_svg}>
                    <img src={i1_2} alt="" />
                    <img src={i2_2} alt="" />
                    <img src={i4_2} alt="" />
                    <img src={i5_2} alt="" />
                    <img src={i6_2} alt="" />
                    <img src={i3_2} alt="" />
                    <img src={i9_2} alt="" />
                    <img src={i8_2} alt="" />
                    <img src={i10_2} alt="" />
                    <img src={i7_2} alt="" />
                </div>
            </div>
            {/* <ModalVariantChoice isOpen={isOpen} onClose={() => setIsOpen(false)}></ModalVariantChoice> */}
            <ModalVariantChoice isOpen={isOpen} onClose={() => setIsOpen(false)} openParamModal={() => {setIsOpenParamModal(true); setIsOpen(false);}}/>
            <ModalParameters isOpenParam={isOpenParamModal} onCloseParam={() => setIsOpenParamModal(false)}/>
        </section>
    );
};