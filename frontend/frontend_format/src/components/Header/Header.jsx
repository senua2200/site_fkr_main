import styles from './Header.module.css'
import logo_img from '../../assets/logo.svg'
import user_log from '../../assets/user_log.svg'
import { Link } from "react-router-dom"
import { useEffect, useState } from 'react';
import { ModalRegLog } from '../ModalWindow/ModalRegLog';

export const Header = () => {

    const [isOpen, setIsOpen] = useState(false);
    const [modeForm, setModeForm] = useState("");

    const[usernameheader, setUsernameheader] = useState('Вход');

    const refreshUserName = () => {
        fetch('api/get_jwt_token_from_cookie/', {
          method: 'GET',
          credentials: 'include',
        })
          .then(res => res.json())
          .then(data => {
            if (data.user_name) {
              setUsernameheader(data.user_name);
            } else {
              setUsernameheader('Вход');
              console.log('Пользователь не авторизован');
            }
          })
          .catch(err => {
            console.error('Ошибка при получении имени пользователя:', err);
          });
    };
    
    useEffect(() => {
      if (isOpen){
          document.body.style.overflow = "hidden";
      } else {
          document.body.style.overflow = "";
      }
      refreshUserName();

      return () => {
        document.body.style.overflow = "";
      };
    }, [isOpen]);

    return (
        <header> 
            <nav>
                <Link to={"/"} className={styles.logo}>
                    <img src={logo_img} alt="Логотип" />
                    <span className={styles.logo_text}>EasyForm</span>
                </Link>
                <ul>
                    <li><Link to={"/"}>Главная</Link></li>
                    <li><Link to={"/how_usage"}>Как пользоваться</Link></li>
                    <li><Link to={"/price"}>Стоимость</Link></li>
                    {/* <li><Link to={"/"}>О нас</Link></li> */}
                    <li><Link to={"/support"}>Поддержка</Link></li>
                    {/* <li>Главная</li>
                    <li>Как пользоваться</li>
                    <li>Стоимость</li>
                    <li>О нас</li> 
                    <li>Поддержка</li> */}
                </ul>
                {/* <div className={styles.reg_log}>
                    <img src={user_log} alt="" />
                    <button onClick={() => {setIsOpen(true); setModeForm("login")}}>Вход</button>
                    <ModalRegLog isOpen={isOpen} onClose={() => setIsOpen(false)} modeForm={modeForm} setModeForm={setModeForm}></ModalRegLog>
                </div> */}
                <button className={styles.reg_log} onClick={() => {setIsOpen(true); setModeForm("login")}}>
                    <img src={user_log} alt="" />
                    {/* Вход */}
                    {usernameheader}
                </button>
                <ModalRegLog isOpen={isOpen} onClose={() => setIsOpen(false)} modeForm={modeForm} setModeForm={setModeForm} onLoginSuccess={refreshUserName}></ModalRegLog>
            </nav>
        </header>
    );
};