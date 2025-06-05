import styles from '../layout/HowUsagePage/HowUsagePage.module.css'
import video_alt from '../../assets/video_alt.jpg'
import video_play from '../../assets/video_play.svg'

export const VideoUse = () => {
    return (
        <section className={styles.video_use}>
            <h2>Как пользоваться</h2>
            <div className={styles.video_use_container}>
                <h2>Пример использования с объяснением</h2>
                <div className={styles.video}>
                    <img className={styles.video_alt} src={video_alt} alt="" />
                    <img className={styles.video_play} src={video_play} alt="" />
                </div>
                <span className={styles.links_video}>
                    Видео доступно на:
                    <a href="">YouTube</a>
                    <a href="">Rutube</a>
                    <a href="">VK</a>
                </span>
            </div>
        </section>
    );
};