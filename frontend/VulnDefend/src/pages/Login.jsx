import { useEffect } from "react";
import { useLoaderData, useNavigate } from "react-router-dom";
import { GoogleLogin } from "@react-oauth/google";
import { verifyGoogleToken } from "../utils/auth";
import { saveUserData, clearUserData } from "../utils/storage";
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;


export function loader({ request }) {
  const url = new URL(request.url);
  return {
    message: url.searchParams.get("message"),
    redirectTo: url.searchParams.get("redirectTo") || "/",
  };
}

const Login = () => {
  const { message, redirectTo } = useLoaderData();
  const navigate = useNavigate();

  useEffect(() => {
    const checkLogin = async () => {
      const idToken = localStorage.getItem("loggedin");

      // Redirect to login if no token is found
      if (!idToken) {
        console.log("No token found, please log in.");
        return;
      }

      try {
        // Verify the token
        const data = await verifyGoogleToken(idToken);
        console.log("Already login")
        if (data && data.isLogin) {
          // Store user data if verification is successful
          saveUserData({
            google_id: data.user.google_id,
            name: data.user.name,
            picture: data.user.picture,
            email: data.user.email,
          });
          // Call the create_user API to register the user on backend
          await fetch(`${BACKEND_URL}/api/create_user`, {
            method: "POST",
            headers: {
              "Authorization": `Bearer ${idToken}`,
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              google_id: data.user.google_id,
              name: data.user.name,
              picture: data.user.picture,
              email: data.user.email,
              role: "admin"  // Optional or based on logic
            }),
          });

          // Navigate to `redirectTo` path or default to `/chat/:id`
          if (redirectTo === "/" || redirectTo === "") {
            navigate(`/chat/${data.user.google_id}`);
          } else {
            navigate(redirectTo);
          }
        } else {
          console.error("User verification failed.");
          // clearUserData();

          navigate(`/login?message=Verification failed`);
        }
      } catch (error) {
        console.error("Verification error:", error);
        clearUserData();
        navigate(`/login?message=Verification error`);
      }
    };

    checkLogin();
  }, [redirectTo, navigate]);

  const handleGoogleLoginSuccess = async (credentialResponse) => {
    console.log("Google Login Successful", credentialResponse);

    const idToken = credentialResponse.credential;
    localStorage.setItem("loggedin", idToken);  // Save token in local storage

    try {
      // Verify the Google token with the backend
      const data = await verifyGoogleToken(idToken);

      if (data && data.isLogin) {
        // Store user data if needed
        localStorage.setItem("google_id", data.user.google_id);
        localStorage.setItem("name", data.user.name);
        localStorage.setItem("picture", data.user.picture);
        localStorage.setItem("email", data.user.email);

        // Navigate to the `redirectTo` path after successful login
        console.log("redirectTo:", redirectTo);
        if (redirectTo === "/" || redirectTo === "") {
          navigate(`/chat/${data.user.google_id}`);
        } else {
          navigate(redirectTo);
        }
      } else {
        console.error("User verification failed.");
        navigate(`/login?message=Verification failed`);
      }
    } catch (error) {
      console.error("Verification error:", error);
      navigate(`/login?message=Verification error`);
    }
  };

  const handleGoogleLoginFailure = (error) => {
    console.error("Google Login Failed", error);
    navigate(`/login?message=Login failed`);
  };

  return (
    <div className="login-container">
      <h2>Welcome Back</h2>
      {message && <p className="error-message">{message}</p>}
      <p>Please sign in to continue</p>
      <GoogleLogin
        onSuccess={handleGoogleLoginSuccess}
        onError={handleGoogleLoginFailure}
      />
    </div>
  );
};

export default Login;
