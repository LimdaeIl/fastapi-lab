import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import AuthLayout from "../components/auth/AuthLayout";
import { useAuthStore } from "../stores/authStore";

export default function SignupPage() {
    const signup = useAuthStore((s) => s.signup);
    const nav = useNavigate();

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [err, setErr] = useState<string | null>(null);

    async function onSubmit(e: React.FormEvent) {
        e.preventDefault();
        setErr(null);
        try {
            await signup(email, password);
            nav("/login");
        } catch (e: any) {
            setErr(e?.message ?? "signup failed");
        }
    }

    return (
        <AuthLayout title="Create your account">
            <form onSubmit={onSubmit} className="grid gap-3">
                <div className="grid gap-2">
                    <div className="text-xs text-white/65">Email</div>
                    <input
                        className="w-full rounded-[10px] border border-white/10 bg-white/5 px-3 py-3 text-white/90 outline-none placeholder:text-white/35 focus:border-[rgba(88,166,255,0.75)] focus:ring-4 focus:ring-[rgba(88,166,255,0.22)]"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="email"
                        autoComplete="username"
                    />
                </div>

                <div className="grid gap-2">
                    <div className="text-xs text-white/65">Password</div>
                    <input
                        className="w-full rounded-[10px] border border-white/10 bg-white/5 px-3 py-3 text-white/90 outline-none placeholder:text-white/35 focus:border-[rgba(88,166,255,0.75)] focus:ring-4 focus:ring-[rgba(88,166,255,0.22)]"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="password"
                        type="password"
                        autoComplete="new-password"
                    />
                </div>

                <button
                    className="mt-1 w-full rounded-[10px] bg-blue-500 py-3 font-semibold text-white hover:bg-blue-600 active:translate-y-px"
                    type="submit"
                >
                    Sign up
                </button>

                {err && <div className="text-sm text-red-400 mt-1">{err}</div>}

                <div className="mt-2 flex items-center justify-between text-[13px] text-white/60">
                    <Link className="text-[rgba(120,190,255,0.95)] hover:underline" to="/login">
                        Already have an account? Log in
                    </Link>
                    <span />
                </div>
            </form>
        </AuthLayout>
    );
}