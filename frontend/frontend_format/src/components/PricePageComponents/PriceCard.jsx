import styles from '../layout/PricePage/PricePage.module.css'

export const PriceCard = () => {
    return (
        <section className={styles.price_card}>
            <div className={styles.container_price}>
                <h2>Варианты оплаты сервиса</h2>
                <div className={styles.all_cards}>
                    <div className={`${styles.card} ${styles.card_1}`}>
                        <h3>Разовое форматирование курсовой работы</h3>
                        <div className={styles.price}>
                            <p>Обработка одной страницы</p>
                            <p>=</p>
                            <p>3 руб.</p>
                        </div>
                        <div className={styles.list_price}>
                            <ul>
                                <li>Качественно оформленная курсовая работа</li>
                                <li>Форматирование только для одного документа</li>
                                <li>Возможность опробовать работу серсиса</li>
                            </ul>
                        </div>
                        <button>Перейти к закрузке документа</button>
                    </div>
                    <div className={`${styles.card} ${styles.card_2}`}>
                        <h3>Набор из 5 обработок курсовых работ</h3>
                        <div className={styles.price}>
                            <p>Набор из 5 обработок</p>
                            <p>=</p>
                            <p>500 руб.</p>
                        </div>
                        <div className={styles.list_price}>
                            <ul>
                                <li>Качественно оформленная курсовая работа</li>
                                <li>Дешевле при форматировании нескольких работ</li>
                                <li>Платишь 1 раз и забываешь об этом</li>
                            </ul>
                        </div>
                        <button>Перейти к оплате</button>
                    </div>
                </div>
            </div>
        </section>
    );
};