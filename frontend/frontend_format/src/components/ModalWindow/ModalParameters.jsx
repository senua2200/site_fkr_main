import styles from './ModalParameters.module.css'
import close_x from '../../assets/close_x.svg'
import next from '../../assets/next.svg'
import ReactDOM from 'react-dom'

export const ModalParameters = ({isOpenParam, onCloseParam}) => {
    if (!isOpenParam) return null;

    const click_background = (e) => {
        if (e.target === e.currentTarget){
            onCloseParam();
        }
    }

    return ReactDOM.createPortal (
        <section className={styles.modal_parameters} onClick={click_background}>
            <div className={styles.form_button}>
                <form action="" className={styles.form_modal_parameters}>
                    <h2>Общие настройки</h2>
                    <img src={close_x} alt="" className={styles.close_x} onClick={click_background}/>
                    <div className={styles.left_right_div}>
                        <div className={styles.left_div}>
                            <div className={styles.param}>
                                <span className={styles.param_title}>Размер текста</span>
                                <div>
                                    <span className={styles.param_value}>14</span>
                                </div>
                            </div>
                            <div className={styles.param}>
                                <span className={styles.param_title}>Стиль текста</span>
                                <div>
                                    <span className={styles.param_value}>Times New Roman</span>
                                </div>
                            </div>
                            <div className={styles.param}>
                                <span className={styles.param_title}>Выравнивание основного текста</span>
                                <div>
                                    <span className={styles.param_value}>по ширине</span>
                                </div>
                            </div>
                            <div className={styles.param}>
                                <span className={styles.param_title}>Выравнивание заголовков</span>
                                <div>
                                    <span className={styles.param_value}>по центру</span>
                                </div>
                            </div>
                            <div className={styles.param}>
                                <span className={styles.param_title}>Отступ первой строки</span>
                                <div>
                                    <span className={styles.param_value}>1.25 см</span>
                                </div>
                            </div>
                            <div className={styles.param}>
                                <span className={styles.param_title}>Междустрочный интервал</span>
                                <div>
                                    <span className={styles.param_value}>1.5</span>
                                </div>
                            </div>
                        </div>
                        <div className={styles.right_div}> 
                            <div className={styles.param}>
                                <span className={styles.param_title}>Размер верхнего поля</span>
                                <div>
                                    <span className={styles.param_value}>20 мм</span>
                                </div>
                            </div>
                            <div className={styles.param}>
                                <span className={styles.param_title}>Размер нижнего поля</span>
                                <div>
                                    <span className={styles.param_value}>20 мм</span>
                                </div>
                            </div>
                            <div className={styles.param}>
                                <span className={styles.param_title}>Размер правого поля</span>
                                <div>
                                    <span className={styles.param_value}>10 мм</span>
                                </div>
                            </div>
                            <div className={styles.param}>
                                <span className={styles.param_title}>Размер левого поля</span>
                                <div>
                                    <span className={styles.param_value}>30 мм</span>
                                </div>
                            </div>
                            <div className={styles.param}>
                                <span className={styles.param_title}>Интервал перед абзацем</span>
                                <div>
                                    <span className={styles.param_value}>1</span>
                                </div>
                            </div>
                            <div className={styles.param}>
                                <span className={styles.param_title}>Интервал после абзаца</span>
                                <div>
                                    <span className={styles.param_value}>1</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </form>
                <button className={styles.next}>
                    <span>Дальше</span>
                    <img src={next} alt="" />
                </button>
            </div>
        </section>,
        document.body
    );
};