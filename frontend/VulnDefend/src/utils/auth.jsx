
import { redirect } from "react-router-dom"
// const { OAuth2Client } = require("google-auth-library");
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

// const client = new OAuth2Client(process.env.GOOGLE_CLIENT_ID);

export async function verifyGoogleToken(idToken) {
  try {
    const response = await fetch(`${BACKEND_URL}/api/verify_google_token/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ idToken }),
    });

    if (!response.ok) {
      console.log("hehehhhehehhehe")
      // throw new Error(`Server error: ${response.statusText}`);
      return {isLogin:false,user:{}}
    }

    const data = await response.json();
    console.log("User details:", data);

    return data
  } catch (error) {
    console.error("Token verification failed:", error);
  }
}
export async function requireAuth(request) {
  try {
    const pathname = new URL(request.url).pathname;
    const idToken = localStorage.getItem("loggedin");

    // If no token is found, redirect to login with `redirectTo` parameter
    if (!idToken) {
      console.log("No token found. Redirecting to login...");
      throw redirect(`/login?message=You must log in first.&redirectTo=${pathname}`);
    }

    // Verify the token with the backend
    const data = await verifyGoogleToken(idToken);

    // If verification fails or `data.isLogin` is false, redirect to login
    if (!data || !data.isLogin) {
      console.log("Token verification failed. Redirecting to login...");
      throw redirect(`/login?message=You must log in first.&redirectTo=${pathname}`);
    }

    // If verification is successful, allow access
    return null;
  } catch (error) {
    console.error("Error in requireAuth:", error);
    throw redirect(`/login?message=An error occurred. Please log in again`);
  }
}

// Use the function to verify token from the frontend
// app.post('/auth/google', async (req, res) => {
//   const { credential } = req.body;

//   try {
//     const userData = await verifyGoogleToken(credential);
//     // Save or update userData in MongoDB, then send a response
//     res.json(userData);
//   } catch (error) {
//     console.error("Token verification failed", error);
//     res.status(401).json({ error: "Invalid Google token" });
//   }
// });

// async function handleUserLogin(idToken) {
//   const userData = await verifyGoogleToken(idToken);

//   const user = await User.findOneAndUpdate(
//     { googleId: userData.googleId },
//     { ...userData, lastLogin: new Date() },
//     { upsert: true, new: true }
//   );

//   return user;
// }
