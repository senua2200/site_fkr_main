import styles from '../layout/PersonalAccountPage/PersonalAccountPage.module.css'
import pen_usage from '../../assets/pen_usage.svg'
import { useState, useEffect } from 'react';
import { ModalPersonalData } from '../ModalWindow/ModalPersonalData';

export const ProfileInformation = () => {

    const [name, setName] = useState("Имя");
    const [email, setEmail] = useState("Почта");
    const [number, setNumber] = useState("Телефон");
    const [password, setPassword] = useState("Пароль");
    const [isModalOpen, setIsModalOpen] = useState(false);

    const openModal = () => setIsModalOpen(true);
    const closeModal = () => setIsModalOpen(false);

    const setPersonalData = () => {
        setName("qwe");
        setEmail("qwe");
        setNumber("qwe");
        setPassword("qwe");
    };

    useEffect(() => {
        if (isModalOpen){
            document.body.style.overflow = "hidden";
        } else {
            document.body.style.overflow = "";
        }
    
        return () => {
          document.body.style.overflow = "";
        };
    }, [isModalOpen]);

    return (
        <section className={styles.profile_information}>
            <div className={styles.profile_information_all}>
                <div className={styles.information_name} onClick={openModal}>
                    <span>{name}</span>
                    <img src={pen_usage} alt="" />
                </div>
                <div className={styles.information_email} onClick={openModal}>
                    <span>{email}</span>
                    <img src={pen_usage} alt="" />
                </div>
                <div className={styles.information_tel} onClick={openModal}>
                    <span>{number}</span>
                    <img src={pen_usage} alt="" />
                </div>
                <div className={styles.information_password} onClick={openModal}>
                    <span>{password}</span>
                    <img src={pen_usage} alt="" />
                </div>
            </div>
            <ModalPersonalData isOpen={isModalOpen} onClose={closeModal} />
        </section>
    );
};