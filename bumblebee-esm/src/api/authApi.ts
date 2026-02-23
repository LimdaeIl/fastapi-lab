// src/api/authApi.ts
// API 래퍼
import { http } from "./http";
import { tokenStore } from "../auth/tokenStore";

export type Me = { id: number; email: string; role: string };

export async function signup(email: string, password: string) {
    const res = await http.post("/api/v1/auth/signup", { email, password });
    return res.data?.data as { id: number; email: string };
}

export async function login(email: string, password: string) {
    const res = await http.post("/api/v1/auth/login", { email, password });
    const data = res.data?.data as {
        access_token: string;
        refresh_token: string;
        token_type: string;
    };
    tokenStore.setTokens(data.access_token, data.refresh_token);
    return data;
}

export async function me() {
    const res = await http.get("/api/v1/members/me");
    return res.data?.data as Me;
}

export async function logout() {
    const refresh = tokenStore.getRefresh();
    if (refresh) {
        await http.post("/api/v1/auth/logout", { refresh_token: refresh });
    }
    tokenStore.clear();
}