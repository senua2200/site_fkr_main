import React, { useEffect, useState } from 'react';
import ReactDOM from 'react-dom'
import styles from '../ModalWindow/ModalRegLog.module.css'
import close_x from '../../assets/close_x.svg'

export const ModalRegLog = ({isOpen, onClose, modeForm, setModeForm, onLoginSuccess}) => {

    const isRegister = modeForm === "register";

    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [phone, setPhone] = useState('');
    const [emailOrPhone, setEmailOrPhone] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState(null);

    if (!isOpen) return null;

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
          const cookies = document.cookie.split(';');
          for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
            }
          }
        }
        return cookieValue;
    }

    const click_background = (e) => {
        if (e.target === e.currentTarget){
            onClose();
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);
    
        let bodyData = {};
    
        if (isRegister) {
          bodyData = {
            name: username,
            maill: email,
            tel: phone,
            password: password,
          };
        } else {
          bodyData = {
            // tel: emailOrPhone,
            maill: emailOrPhone,
            password: password,
          };
        }
    
        try {
          const response = await fetch('/api/reg_log/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify(bodyData),
          });
    
          const data = await response.json();
    
          if (!response.ok) {
            setError(data.error || 'Ошибка сервера');
          } else {
            console.log('Ответ сервера:', data);
    
            // Попытка прочитать токены из куки (если не HttpOnly)
            const accessToken = getCookie('access_token');
            const refreshToken = getCookie('refresh_token');
            console.log('Access token:', accessToken);
            console.log('Refresh token:', refreshToken);
    
            onLoginSuccess();
            onClose();
          }
        } catch (err) {
          setError('Ошибка сети');
          console.error(err);
        }
    };

    return ReactDOM.createPortal(
        <section className={styles.modal_reg_log} onClick={click_background}>
            <form onSubmit={handleSubmit} action="" className={`${styles.form_reg_log} ${!isRegister && styles.form_reg_log_upgrade_log}`}>
                <img src={close_x} alt="" className={styles.close_x} onClick={click_background}/>
                <h2>{isRegister ? "Регистрация": "Авторизация"}</h2>
                <div className={styles.label_input_all}>
                    {isRegister &&
                        <>
                            <div className={`${styles.label_input_username} ${styles.label_input}`}>
                                <label htmlFor="username">Как вас зовут</label>
                                <input type="text" name="username" id="username" placeholder='Имя:' value={username} onChange={(e) => setUsername(e.target.value)} required />
                            </div>
                            <div className={`${styles.label_input_email} ${styles.label_input}`}>
                                <label htmlFor="email">Ваша почта</label>
                                <input type="email" name="email" id="email" placeholder='Почта:' value={email} onChange={(e) => setEmail(e.target.value)} required/>
                            </div>
                            <div className={`${styles.label_input_phone} ${styles.label_input}`}>
                                <label htmlFor="phone">Ваш телефон</label>
                                <input type="tel" name="phone" id="phone" placeholder='Телефон:' value={phone} onChange={(e) => setPhone(e.target.value)}/>
                            </div>
                        </>
                    }
                    {!isRegister && 
                        <div className={`${styles.label_input_email_phone} ${styles.label_input}`}>
                            <label htmlFor="email_phone">Ваша почта / номер телефона</label>
                            <input type="text" name="email_phone" id="email_phone" placeholder='Почта / телефон:' value={emailOrPhone} onChange={(e) => setEmailOrPhone(e.target.value)} required/>
                        </div>
                    }
                    <div className={`${styles.label_input_password} ${styles.label_input}`}>
                        <label htmlFor="password">Ваш пароль</label>
                        <input type="password" name="password" id="password" placeholder='Пароль:' value={password} onChange={(e) => setPassword(e.target.value)} required/>
                    </div>
                </div>

                {error && <div style={{ color: 'red', marginBottom: '10px' }}>{error}</div>}

                <button type='submit' className={styles.button_reg}>{isRegister ? 'Регистрация' : 'Войти'}</button>
                <div className={styles.footer_form_reg_log}>
                    <span>{isRegister ? "Есть Аккаунт?" : "Нет Аккаунта?"}</span>
                    {isRegister ? <button type='button' onClick={() => setModeForm("login")}>Войти</button> : <button type='button' onClick={() => setModeForm("register")}>Регистрация</button>}
                </div>
            </form>
        </section>,
        document.body
    );
};