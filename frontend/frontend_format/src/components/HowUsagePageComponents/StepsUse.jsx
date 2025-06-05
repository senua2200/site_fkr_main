import styles from '../layout/HowUsagePage/HowUsagePage.module.css'
import arrow_steps_lr from '../../assets/arrow_steps_lr.svg'
import arrow_steps_rl from '../../assets/arrow_steps_rl.svg'

export const StepsUse = () => {
    return (
        <section className={styles.steps_use}>
            <h2>Последовательность действий</h2>
            <div className={styles.steps_use_container}>
                <div className={styles.step_use}>
                    <p>Напишите курсовую работу</p>
                </div>
                <img className={`${styles.arrow_step} ${styles.arrow_step_lr}`} src={arrow_steps_lr} alt="" />
                <div className={styles.step_use}>
                    <p>Пометьте заголовки различными цветами</p>
                </div>
                <img className={`${styles.arrow_step} ${styles.arrow_step_rl}`} src={arrow_steps_rl} alt="" />
                <div className={styles.step_use}>
                    <p>Загрузите курсовую работу</p>
                </div>
                <img className={`${styles.arrow_step} ${styles.arrow_step_lr}`} src={arrow_steps_lr} alt="" />
                <div className={styles.step_use}>
                    <p>Выберите вариант форматирования</p>
                </div>
                <img className={`${styles.arrow_step} ${styles.arrow_step_rl}`} src={arrow_steps_rl} alt="" />
                <div className={styles.step_use}>
                    <p>Выберите вариант оплаты</p>
                </div>
                <img className={`${styles.arrow_step} ${styles.arrow_step_lr}`} src={arrow_steps_lr} alt="" />
                <div className={styles.step_use}>
                    <p>Получите отформатированный документ</p>
                </div>
            </div>
        </section>
    );
};