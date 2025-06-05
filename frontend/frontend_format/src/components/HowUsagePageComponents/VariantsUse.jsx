import styles from '../layout/HowUsagePage/HowUsagePage.module.css'
import standard_variant_img from '../../assets/standard_variant.png'
import castom_variant_img from '../../assets/castom_variant.png'

export const VariantsUse = () => {
    return (
        <section className={styles.variants_use}>
            <div className={styles.variants_use_container}>
                <h2>Воспользуйтесь готовым шаблоном</h2>
                <div className={styles.standard_div}>
                    <img src={standard_variant_img} alt="" />
                    <p>* Вы можете воспользоваться "шаблонами", созданными другими пользователями для своих институтов.</p>
                </div>
                <h2>Или создайте свой</h2>
                <div className={styles.castom_div}>
                    <img src={castom_variant_img} alt="" />
                    <p>* Вы можете создать свой "шаблон", который будет подходить именно вам. Созданный "шаблон" будет доступен вам для дальнейшего использования.</p>
                </div>
            </div>
        </section>
    );
};