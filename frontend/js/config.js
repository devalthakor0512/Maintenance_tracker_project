const API_BASE_URL = "http://127.0.0.1:8000";

const getAuthHeaders = () => {
    const token = localStorage.getItem("access_token");
    return {
        "Content-Type": "application/json",
        "Authorization": token ? `Bearer ${token}` : ""
    };
};

const checkAuth = () => {
    if (!localStorage.getItem("access_token")) {
        window.location.href = "login.html";
    }
};

const logout = () => {
    localStorage.removeItem("access_token");
    window.location.href = "login.html";
};
