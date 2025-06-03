import Header from "../components/Header/Header"
import Banner from "../components/Banner/Banner"
import Architecture from "../components/Architecture/Architecture"
import LunchFlow from "../components/LunchFlow/LunchFlow"
import Features from "../components/Features/Features"
import AnalyticsInsights from "../components/AnalyticsInsights/AnalyticsInsights"
import Tools from "../components/Tools/Tools"
import Team from "../components/Team/Team"
import Footer from "../components/Footer/Footer"
import { defer, useLoaderData, Await } from "react-router-dom"
import { verifyGoogleToken } from "../utils/auth"

export function loader() {
    const idToken = localStorage.getItem("loggedin");
    if (!idToken) {
        console.log("Not found idToken")
        return defer({
            loginResponse: {
                isLogin: false,
                googleId: "",
            }
        })
    }
    const loginResponse = verifyGoogleToken(idToken)
    return defer({ loginResponse: loginResponse })
}
export default function Main() {
    const dataPromise = useLoaderData()
    // console.log(dataPromise)
    return (
        <>
            <Await resolve={dataPromise.loginResponse}>
                {(loginResponse) => <Header loginResponse={loginResponse} />}
            </Await>
            <Banner />
            <Architecture />
            <LunchFlow />
            <Features />
            <AnalyticsInsights />
            <Tools />
            <Team />
            <Footer />
        </>
    )
}