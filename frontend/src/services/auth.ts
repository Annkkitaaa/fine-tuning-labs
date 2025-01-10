import axios from 'axios';

const AUTH_BASE_URL = process.env.REACT_APP_AUTH_URL || 'http://localhost:8000/auth';

export const auth = {
    async login(username: string, password: string) {
        const response = await axios.post(`${AUTH_BASE_URL}/login`, {
            username,
            password
        });
        if (response.data.token) {
            localStorage.setItem('token', response.data.token);
        }
        return response.data;
    },

    async logout() {
        localStorage.removeItem('token');
    },

    getToken() {
        return localStorage.getItem('token');
    },

    isAuthenticated() {
        return !!this.getToken();
    }
};