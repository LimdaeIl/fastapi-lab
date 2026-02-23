// src/stores/authStore.ts
import { create } from "zustand";
import * as authApi from "../api/authApi";
import { tokenStore } from "../auth/tokenStore";

type AuthStore = {
    user: authApi.Me | null;
    isLoading: boolean;
    error: string | null;

    init: () => Promise<void>;
    refreshMe: () => Promise<void>;
    login: (email: string, password: string) => Promise<void>;
    signup: (email: string, password: string) => Promise<void>;
    logout: () => Promise<void>;
};

export const useAuthStore = create<AuthStore>((set, get) => ({
    user: null,
    isLoading: true,
    error: null,

    init: async () => {
        set({ isLoading: true, error: null });
        try {
            await get().refreshMe();
        } catch (e: any) {
            tokenStore.clear();
            set({ user: null, error: e?.message ?? "init failed" });
        } finally {
            set({ isLoading: false });
        }
    },

    refreshMe: async () => {
        const access = tokenStore.getAccess();
        if (!access) {
            set({ user: null });
            return;
        }
        const u = await authApi.me();
        set({ user: u });
    },

    login: async (email, password) => {
        set({ error: null });
        await authApi.login(email, password);
        await get().refreshMe();
    },

    signup: async (email, password) => {
        set({ error: null });
        await authApi.signup(email, password);
    },

    logout: async () => {
        set({ error: null });
        await authApi.logout();
        set({ user: null });
    },
}));