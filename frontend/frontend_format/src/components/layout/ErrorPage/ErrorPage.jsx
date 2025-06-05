import { Link } from "react-router-dom"
import styles from './ErrorPage.module.css'
import error from '../../../assets/error.svg'

export const ErrorPage = () => {
    return (
      <section className={styles.error_page}>
        <div className={styles.error_area}>
          <img className={styles.error_img} src={error} alt="" />
          <h2>Ошибка 404</h2>
          <h3>Такой страницы не существует!</h3>
          <div className={styles.text}>
            <p>Перейдите на главную страницу для дальнейшего использования.</p>
          </div>
          <button><Link to="/">Перейти на главную</Link></button>
        </div>
      </section>
    );
  }