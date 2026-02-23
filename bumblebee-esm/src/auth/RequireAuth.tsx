// src/auth/RequireAuth.tsx
import React from "react";
import { Navigate } from "react-router-dom";
import { useAuthStore } from "../stores/authStore";

export function RequireAuth({ children }: { children: React.ReactNode }) {
    const { user, isLoading } = useAuthStore();
    if (isLoading) return <div style={{ padding: 24 }}>Loading...</div>;
    if (!user) return <Navigate to="/login" replace />;
    return <>{children}</>;
}