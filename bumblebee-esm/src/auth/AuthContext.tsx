// src/auth/AuthContext.tsx
// AuthContext (로그인 상태 + me 로딩)
import React, { createContext, useContext, useEffect, useMemo, useState } from "react";
import * as authApi from "../api/authApi";
import { tokenStore } from "./tokenStore";

type AuthState = {
    user: authApi.Me | null;
    isLoading: boolean;
    login: (email: string, password: string) => Promise<void>;
    signup: (email: string, password: string) => Promise<void>;
    logout: () => Promise<void>;
    refreshMe: () => Promise<void>;
};

const AuthContext = createContext<AuthState | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
    const [user, setUser] = useState<authApi.Me | null>(null);
    const [isLoading, setIsLoading] = useState(true);

    async function refreshMe() {
        const access = tokenStore.getAccess();
        if (!access) {
            setUser(null);
            return;
        }
        const u = await authApi.me();
        setUser(u);
    }

    async function login(email: string, password: string) {
        await authApi.login(email, password);
        await refreshMe();
    }

    async function signup(email: string, password: string) {
        await authApi.signup(email, password);
    }

    async function logout() {
        await authApi.logout();
        setUser(null);
    }

    useEffect(() => {
        (async () => {
            try {
                await refreshMe();
            } catch {
                tokenStore.clear();
                setUser(null);
            } finally {
                setIsLoading(false);
            }
        })();
    }, []);

    const value = useMemo(
        () => ({ user, isLoading, login, signup, logout, refreshMe }),
        [user, isLoading]
    );

    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
    const ctx = useContext(AuthContext);
    if (!ctx) throw new Error("useAuth must be used within AuthProvider");
    return ctx;
}