// src/api/http.ts
// axios 인스턴스 + 자동 refresh 인터셉터
import axios, { AxiosError, InternalAxiosRequestConfig } from "axios";
import { tokenStore } from "../auth/tokenStore";

const BASE_URL = "http://127.0.0.1:8000";

export const http = axios.create({
    baseURL: BASE_URL,
    headers: { "Content-Type": "application/json" },
});

// 요청에 access_token 자동 첨부
http.interceptors.request.use((config: InternalAxiosRequestConfig) => {
    const access = tokenStore.getAccess();
    if (access) {
        config.headers = config.headers ?? {};
        config.headers.Authorization = `Bearer ${access}`;
    }
    return config;
});

let refreshPromise: Promise<string> | null = null;

async function refreshAccessToken(): Promise<string> {
    const refresh = tokenStore.getRefresh();
    if (!refresh) throw new Error("No refresh token");

    // 동시 401 폭탄 방지: refresh는 한 번만
    if (!refreshPromise) {
        refreshPromise = axios
            .post(`${BASE_URL}/api/v1/auth/refresh`, { refresh_token: refresh })
            .then((res) => {
                const data = res.data?.data;
                const newAccess = data?.access_token;
                const newRefresh = data?.refresh_token;
                if (!newAccess || !newRefresh) throw new Error("Invalid refresh response");
                tokenStore.setTokens(newAccess, newRefresh);
                return newAccess;
            })
            .finally(() => {
                refreshPromise = null;
            });
    }

    return refreshPromise;
}

// 401이면 refresh 후 재시도
http.interceptors.response.use(
    (res) => res,
    async (error: AxiosError) => {
        const status = error.response?.status;
        const original = error.config as any;

        if (status === 401 && original && !original._retry) {
            original._retry = true;
            try {
                const newAccess = await refreshAccessToken();
                original.headers = original.headers ?? {};
                original.headers.Authorization = `Bearer ${newAccess}`;
                return http.request(original);
            } catch (e) {
                tokenStore.clear();
                return Promise.reject(e);
            }
        }

        return Promise.reject(error);
    }
);
