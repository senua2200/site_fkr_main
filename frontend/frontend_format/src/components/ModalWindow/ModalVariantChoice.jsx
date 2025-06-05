import styles from "./ModalVariantChoice.module.css";
import arrow_menu from "../../assets/arrow_menu.svg"
import close_x from "../../assets/close_x.svg"
import ReactDOM from 'react-dom'
import { useState } from "react";
import { ModalParameters } from "./ModalParameters";

export const ModalVariantChoice = ({isOpen, onClose, openParamModal}) => {
    if (!isOpen) return null;
    const [isDropdownOpen, setIsDropeDown] = useState(false);

    const toggleDropdown = () => {
        setIsDropeDown((value) => !value);
    };

    const click_background = (e) => {
        if (e.target === e.currentTarget){
            onClose();
        }
    }

    const [isOpenParam, setIsOpenParam] = useState(false);

    return ReactDOM.createPortal(
        <section className={styles.modal_variant_choice} onClick={click_background}>
            <form className={styles.form_variant_choice} action="">
                <h2>Выберите вариант форматирования</h2>
                <img src={close_x} alt="" className={styles.close_x} onClick={click_background}/>
                <div className={styles.cont_stand_castom}>
                    <div className={`${styles.standard_variant} ${isDropdownOpen ? styles.standard_variant_open : ''}`}>
                        <div className={styles.standard_variant_header} onClick={toggleDropdown}>
                            <span>Учебное заведение</span>
                            <img className={`${styles.arrow_menu} ${isDropdownOpen ? styles.arrow_menu_open : ''}`} src={arrow_menu} alt="" />
                        </div>
                        <ul className={`${styles.standard_variant_choice} ${isDropdownOpen ? styles.standard_variant_choice_open : ''}`}>
                            <li>
                                <p>Иркутский национальный исследовательский технический университет</p>
                            </li>
                            <li>
                                <p>Иркутский государственный университет</p>
                            </li>
                        </ul>
                    </div>
                    <button type="button" className={styles.castom} onClick={() => {openParamModal()}}>Свой шаблон</button>
                </div>
            </form>
            <ModalParameters isOpenParam={isOpenParam} onCloseParam={() => setIsOpenParam(false)}></ModalParameters>
        </section>,
        document.body
    );
};