// utils/storage.js
export function saveUserData(userData) {
    localStorage.setItem("google_id", userData.google_id);
    localStorage.setItem("name", userData.name);
    localStorage.setItem("picture", userData.picture);
    localStorage.setItem("email", userData.email);
}

export function clearUserData() {
    localStorage.removeItem("google_id");
    localStorage.removeItem("name");
    localStorage.removeItem("picture");
    localStorage.removeItem("email");
    localStorage.removeItem("loggedin");

}
