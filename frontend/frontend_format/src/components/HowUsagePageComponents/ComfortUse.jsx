import styles from '../layout/HowUsagePage/HowUsagePage.module.css'

export const ComfortUse = () => {
    return (
        <section className={styles.comfort_use}>
            <div className={styles.comfort_use_container}>
                <h2>Почему это удобно?</h2>
                <div className={styles.facts}>
                    <div className={styles.fact}>
                        {/* <img src="" alt="" /> */}
                        <div className={styles.zagotovka}></div>
                        <div className={styles.text_content}>
                            <h3 className={styles.rrr}>Вы можете не думать о том, как писать текст</h3>
                            <p>Из-за копирования текста и других факторов, всегда, при написании работы размер текста, стиль, отступы и другие параметры не совпадают.</p>
                            <p>Расслабьтесь и просто пишите свою работу. Мы все исправим.</p>
                        </div>
                    </div>
                    <div className={styles.fact}>
                        <div className={styles.text_content}>
                            <h3>Забудьте про создание оглавления, центрирование картинок и диаграмм</h3>
                            <p>Вам больше не придется создавать оглавление, применять к нему стили, а также центрировать картинки и диаграммы с их подписями.</p>
                            <p>Не нумеруйте свои рисунки, диаграммы и таблицы. Мы сделаем это за вас.</p>
                        </div>
                        {/* <img src="" alt="" /> */}
                        <div className={styles.zagotovka}></div>
                    </div>
                    <div className={styles.fact}>
                        {/* <img src="" alt="" /> */}
                        <div className={styles.zagotovka}></div>
                        <div className={styles.text_content}>
                            <h3 className={styles.lll}>А так же множество других вещей мы берем на себя</h3>
                            <p>Мы сделаем все возможное, чтобы ваша работа была оформлена правильно.</p>
                            <p>Напишите работу и предоставьте все остальное нам.</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    );
};