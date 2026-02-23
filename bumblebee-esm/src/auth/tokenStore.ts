// src/auth/tokenStore.ts
// 토큰 저장소 (localStorage)
const ACCESS_KEY = "access_token";
const REFRESH_KEY = "refresh_token";

export const tokenStore = {
    getAccess() {
        return localStorage.getItem(ACCESS_KEY);
    },
    getRefresh() {
        return localStorage.getItem(REFRESH_KEY);
    },
    setTokens(access: string, refresh: string) {
        localStorage.setItem(ACCESS_KEY, access);
        localStorage.setItem(REFRESH_KEY, refresh);
    },
    clear() {
        localStorage.removeItem(ACCESS_KEY);
        localStorage.removeItem(REFRESH_KEY);
    },
};
