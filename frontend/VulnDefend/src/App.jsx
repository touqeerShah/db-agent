import "./App.css";

import {
  createBrowserRouter,
  createRoutesFromElements,
  Route,
  RouterProvider,
} from "react-router-dom";
import ChatPage, {loader as LoadChat} from "./pages/Chat/Chat"

import ErrorBoundary from './pages/Error';  // Assuming ErrorBoundary is in the same directory
import Layout from "./pages/Layout"
import Login, { loader as loginLoader } from "./pages/Login"
import NotFound, { loader as notFoundloader } from "./pages/NotFound"
import Main, { loader as mainLoader } from "./pages/Main"
// import { requireAuth } from "./utils/auth"
// import { requireAuth } from "./utils";
import { GoogleOAuthProvider } from "@react-oauth/google";
const GOOGLE_CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID;
// import HostVanLayout from "./components/HostVanLayout"
const router = createBrowserRouter(
  createRoutesFromElements(
    <Route element={<Layout />}>

      <Route
        path="/"
        element={<Main />}
        errorElement={<ErrorBoundary />} // Error boundary added
        loader={mainLoader}
      />
      <Route
        path="login"
        element={<GoogleOAuthProvider clientId={GOOGLE_CLIENT_ID}><Login /> </GoogleOAuthProvider>}
        loader={loginLoader}
      // action={loginAction}
      />

      <Route
        path="/chat/:id"
        element={<ChatPage />}
        errorElement={<ErrorBoundary />} // Error boundary added
        loader={LoadChat}
      />;
      <Route
        path="/chat/:id/:chatid"
        element={<ChatPage />}
        errorElement={<ErrorBoundary />}
        loader={LoadChat}
      />
      <Route path="*" element={<NotFound />} loader={notFoundloader} />
    </Route>
  )
);


function App() {
  return (
    <>
      <RouterProvider router={router} />
    </>
  );
}

export default App;
