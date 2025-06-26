import { useState } from 'react';
import styles from '../layout/SupportPage/SupportPage.module.css'

export const SupportPageMainContent = () => {

    const [questionText, setQuestionText] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();
        console.log("Ваш вопрос:", questionText);
        setQuestionText("");

        let bodyData = {};
        
        bodyData = {
            question: questionText,
        };

        try {
            const response = await fetch('api/get_user_question/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    // 'X-CSRFToken': csrfToken, // добавь, если понадобится CSRF токен
                },
                credentials: 'include',  // Очень важно для куки!
                body: JSON.stringify(bodyData)
            });

            const data = await response.json();
            if (!response.ok) {
                console.log("Ошибка сервера");
            }
            else {
                console.log("Ответ сервера:", data);
            }
        }
        catch (err){
            console.log(err);
        }
    };

    const make_change = (e) => {
        console.log(e.target.value);
        setQuestionText(e.target.value);
    };

    

    return (
        <section className={styles.support_page_main_content}>
            <div className={styles.support_area}>
                <div className={styles.faq_area}>
                    <div className={styles.faq_area_header}>
                        <h2>Часто задаваемые вопросы</h2>
                    </div>
                    <div className={styles.faq}>
                        <ul>
                            <li>Получится ли оформить мою работу?</li>
                            <li>Сколько будет стоить форматирование работы?</li>
                            <li>Когда будет готова моя работа?</li>
                            <li>Как с вами связаться?</li>
                            <li>Где и как я получу работу?</li>
                            <li>Как создать шаблон для моего оформления?</li>
                            <li>Почему в списке нет моего института?</li>
                        </ul>
                    </div>
                </div>
                <div className={styles.message_form_container}>
                    <div className={styles.h3_form}>
                        <h3>Напишите вопрос, который хотите задать</h3>
                        <h3>Мы постараемся ответить максимально быстро</h3>
                    </div>
                    <form onSubmit={handleSubmit}>
                        {/* <input type="text" name="question_text" id="question_text" placeholder='Какой у вас вопрос?' required value={questionText} onChange={make_change}/> */}
                        <textarea name="question_text" id="question_text" placeholder='Какой у вас вопрос?' required value={questionText} onChange={make_change}></textarea>
                        <button type="submit">Отправить</button>
                    </form>
                </div>
            </div>
        </section>
    );
};