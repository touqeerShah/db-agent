import { useEffect } from "react";
import { useNavigate, Link, useLoaderData, Await } from "react-router-dom";
import { verifyGoogleToken } from "../utils/auth";
import { defer } from "react-router-dom";

export function loader() {
    const loginResponse = verifyGoogleToken();
    return defer({ loginResponse });
}

export default function NotFound() {
    const navigate = useNavigate();
    const { loginResponse } = useLoaderData();

    useEffect(() => {
        loginResponse.then((data) => {
            if (data.isLoggedIn) {
                navigate(`/chat/${data.user.google_id}`);
            } else {
                navigate("/");
            }
        });
    }, [loginResponse, navigate]);

    return (
        <Await resolve={loginResponse}>
            {() => (
                <div className="not-found-container">
                    <h1>Sorry, the page you were looking for was not found.</h1>
                    <Link to="/" className="link-button">Return to Home</Link>
                </div>
            )}
        </Await>
    );
}
