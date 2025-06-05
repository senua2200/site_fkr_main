import styles from '../Footer/Footer.module.css'
import vk from '../../assets/vk.svg'
import tg from '../../assets/tg.svg'
import yt from '../../assets/yt.svg'
import { Link } from "react-router-dom"

export const Footer = () => {
    return (
        <footer>
            <div className={styles.footer_container}>
                <div className={styles.social_network}>
                    <img src={vk} alt="vk" />
                    <img src={tg} alt="telegram" />
                    <img src={yt} alt="youtube" />
                </div>
                <div className={styles.links_pages}>
                    <Link to={"/"}>Главная</Link>
                    <Link to={"/how_usage"}>Как пользоваться</Link>
                    <Link to={"/price"}>Стоимость</Link>
                    {/* <Link to={"/"}>О нас</Link> */}
                    <Link to={"/support"}>Поддержка</Link>
                </div>
                <div className={styles.neznau}>
                    <span className={styles.neznau_content}>© 2025 EasyForm. Все права защищены. Использование материалов сайта возможно только с согласия правообладателя.</span>
                </div>
            </div>
        </footer>
    );
};