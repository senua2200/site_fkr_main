import ar1 from '../../assets/ar1.svg'
import ar2 from '../../assets/ar2.svg'
import ar3 from '../../assets/ar3.svg'
import styles from '../layout/MainPage/MainPage.module.css'

export const MiniMap = () => {
    return (
        <section className={styles.mini_map}>
            <h2>Вы можете ознакомиться с подробной инструкцией по использованию данного сервиса на странице <a href="">Как пользоваться</a></h2>
            <div className={styles.map}>
                <div className={styles.header_map}>
                    <p>Выделяете необходимым зветом все заголовки в своей курсовой работе</p>
                    <img src={ar1} alt="" />
                    <p>Выбираете тип оформления: стандартный / пользовательский</p>
                </div>
                <div className={styles.body_map}>
                    <img src={ar2} alt="" />
                </div>
                <div className={styles.footer_map}>
                    <p>Скачиваете оформленную работу</p>
                    <img src={ar3} alt="" />
                    <p>Загружаете документ на сайт</p>
                </div>
            </div>
        </section>
    );
};