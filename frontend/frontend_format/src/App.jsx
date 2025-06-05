import { Header } from './components/Header/Header'
import { MainPage } from "./components/layout/MainPage/MainPage"
import { Footer } from './components/Footer/Footer'
import { SupportPage } from './components/layout/SupportPage/SupportPage'
import { ErrorPage } from './components/layout/ErrorPage/ErrorPage'
import { PricePage } from './components/layout/PricePage/PricePage'
import { Routes, Route, useLocation } from "react-router-dom"
import { PersonalAccountPage } from './components/layout/PersonalAccountPage/PersonalAccountPage'
import { HowUsagePage } from './components/layout/HowUsagePage/HowUsagePage'

function App() {
  const location = useLocation();

  const isErrorPage = !['/', '/support', '/price', '/personal_account', '/how_usage'].includes(location.pathname);

  return (
    <>
      {!isErrorPage && <Header/>}
        <Routes>
          <Route path="/" element={<MainPage />}></Route>
          <Route path="/support" element={<SupportPage />}></Route>
          <Route path="/price" element={<PricePage/>}></Route>
          <Route path="/personal_account" element={<PersonalAccountPage/>}></Route>
          <Route path='/how_usage' element={<HowUsagePage/>}></Route>
          {/* <Route path='/'></Route> */}
          <Route path="*" element={<ErrorPage />} />
        </Routes>
      {!isErrorPage && <Footer/>}
    </>
  )
}

export default App