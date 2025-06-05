import React, { useEffect, useState } from 'react';
import ReactDOM from 'react-dom'
import styles from '../ModalWindow/ModalPersonalData.module.css'
import close_x from '../../assets/close_x.svg'

export const ModalPersonalData = ({isOpen, onClose}) => {

    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [phone, setPhone] = useState('');
    const [password, setPassword] = useState('');

    if (!isOpen) return null;

    const click_background = (e) => {
        if (e.target === e.currentTarget){
            onClose();
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        
        let bodyData = {
            name: username,
            email: email,
            phone: phone,
            password: password,
        };

        try {
            const response = await fetch('api/set_user_data/', {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify(bodyData),
            });

            const data = await response.json();

            if (!response.ok) {
                console.log("Ошибка сервера:", data);
            }
            else {
                console.log('Ответ сервера:', data);
            }
        }
        catch(err) {
            console.error(err);
        }
        onClose();
    };

    return ReactDOM.createPortal(
        <section className={styles.modal_personal_data} onClick={click_background}>
            <form onSubmit={handleSubmit} action="" className={`${styles.form_personal_data}`}>
                <img src={close_x} alt="" className={styles.close_x} onClick={onClose}/>
                <h2>Изменение данных</h2>
                <div className={styles.label_input_all}>
                    <div className={`${styles.label_input_username} ${styles.label_input}`}>
                        <label htmlFor="username">Как вас зовут</label>
                        <input type="text" name="username" id="username" placeholder='Имя:' value={username} onChange={(e) => setUsername(e.target.value)}/>
                    </div>
                    <div className={`${styles.label_input_email} ${styles.label_input}`}>
                        <label htmlFor="email">Ваша почта</label>
                        <input type="email" name="email" id="email" placeholder='Почта:' value={email} onChange={(e) => setEmail(e.target.value)}/>
                    </div>
                    <div className={`${styles.label_input_phone} ${styles.label_input}`}>
                        <label htmlFor="phone">Ваш телефон</label>
                        <input type="tel" name="phone" id="phone" placeholder='Телефон:' value={phone} onChange={(e) => setPhone(e.target.value)}/>
                    </div>
                    <div className={`${styles.label_input_password} ${styles.label_input}`}>
                        <label htmlFor="password">Ваш пароль</label>
                        <input type="password" name="password" id="password" placeholder='Пароль:' value={password} onChange={(e) => setPassword(e.target.value)}/>
                    </div>
                </div>
                <button type='submit' className={styles.button_pd}>Сохранить</button>
            </form>
        </section>,
        document.body
    );
};