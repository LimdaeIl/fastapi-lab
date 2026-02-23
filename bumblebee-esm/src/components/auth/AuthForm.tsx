import React, { useMemo, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import AuthInput from "./AuthInput";
import AuthButton from "./AuthButton";
import { useAuthStore } from "../../stores/authStore";

type Mode = "login" | "signup";

const isValidEmail = (email: string) => {
    const v = email.trim();
    if (!v) return false;
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v);
};

const MIN_PW = 7;
const MAX_PW = 72;

const pwTooShort = (pw: string) => pw.length > 0 && pw.length < MIN_PW;
const pwTooLong = (pw: string) => pw.length > MAX_PW;
const pwLenOk = (pw: string) => pw.length >= MIN_PW && pw.length <= MAX_PW;

export default function AuthForm({ mode }: { mode: Mode }) {
    const nav = useNavigate();

    const login = useAuthStore((s) => s.login);
    const signup = useAuthStore((s) => s.signup);

    const isSignup = mode === "signup";

    const title = useMemo(
        () => (isSignup ? "Create your account" : "Welcome to Bumblebee ESM"),
        [isSignup]
    );

    const submitLabel = isSignup ? "Sign up" : "Log in";

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");

    // 즉시 안내용 touched
    const [touchedEmail, setTouchedEmail] = useState(false);
    const [touchedPassword, setTouchedPassword] = useState(false);
    const [touchedConfirm, setTouchedConfirm] = useState(false);

    const [err, setErr] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);

    // 이메일 즉시 에러
    const liveEmailError = useMemo(() => {
        if (!touchedEmail) return null;
        if (!email.trim()) return "Please enter your email.";
        if (!isValidEmail(email)) return "Please enter a valid email address.";
        return null;
    }, [touchedEmail, email]);

    // 비밀번호 길이 즉시 에러 (login/signup 공통)
    const livePwLenError = useMemo(() => {
        if (!touchedPassword) return null;
        if (!password) return "Please enter your password.";
        if (!pwLenOk(password)) return "Password must be 7–72 characters.";
        return null;
    }, [touchedPassword, password]);

    // signup 전용: confirm 관련 실시간 에러 (우선순위: 길이 -> 불일치)
    const liveConfirmError = useMemo(() => {
        if (!isSignup || !touchedConfirm) return null;

        // 길이 안내(둘 중 하나라도 입력했고 7~72 위반이면)
        if (
            pwTooShort(password) ||
            pwTooShort(confirmPassword) ||
            pwTooLong(password) ||
            pwTooLong(confirmPassword)
        ) {
            return "Password must be 7–72 characters.";
        }

        // 둘 다 길이 OK일 때만 불일치
        if (pwLenOk(password) && pwLenOk(confirmPassword) && confirmPassword.length > 0 && password !== confirmPassword) {
            return "Passwords do not match.";
        }

        return null;
    }, [isSignup, touchedConfirm, password, confirmPassword]);

    // 버튼 활성화 조건
    const canSubmit = useMemo(() => {
        if (loading) return false;
        if (!email.trim()) return false;
        if (!isValidEmail(email)) return false;

        if (!pwLenOk(password)) return false;

        if (isSignup) {
            if (!pwLenOk(confirmPassword)) return false;
            if (password !== confirmPassword) return false;
        }
        return true;
    }, [loading, email, password, confirmPassword, isSignup]);

    function validateOnSubmit() {
        if (!email.trim()) return "Please enter your email.";
        if (!isValidEmail(email)) return "Please enter a valid email address.";

        if (!password) return "Please enter your password.";
        if (!pwLenOk(password)) return "Password must be 7–72 characters.";

        if (isSignup) {
            if (!confirmPassword) return "Please confirm your password.";
            if (!pwLenOk(confirmPassword)) return "Password must be 7–72 characters.";
            if (password !== confirmPassword) return "Passwords do not match.";
        }
        return null;
    }

    async function onSubmit(e: React.FormEvent) {
        e.preventDefault();
        setErr(null);

        const v = validateOnSubmit();
        if (v) {
            setErr(v);
            // submit 시에도 즉시 에러 강제 표시
            setTouchedEmail(true);
            setTouchedPassword(true);
            if (isSignup) setTouchedConfirm(true);
            return;
        }

        setLoading(true);
        try {
            if (isSignup) {
                await signup(email, password);
                nav("/login");
            } else {
                await login(email, password);
                nav("/");
            }
        } catch (e: any) {
            setErr(e?.message ?? (isSignup ? "signup failed" : "login failed"));
        } finally {
            setLoading(false);
        }
    }

    // Password input에 줄 에러 표시 우선순위:
    //  - 길이 에러(livePwLenError)가 있으면 그걸 보여줌
    //  - signup에서 confirm 관련 에러가 있고, password도 관련되면 confirm 에러는 confirm 아래에서 보여줌(지금 구조 그대로)
    const passwordFieldError = livePwLenError;

    return (
        <>
            <h2 className="sr-only">{title}</h2>

            <form onSubmit={onSubmit} className="grid gap-3">
                {/*Email: 이제 고정 */}
                <AuthInput
                    label="Email"
                    value={email}
                    onChange={(e) => {
                        if (!touchedEmail) setTouchedEmail(true);
                        setEmail(e.target.value);
                    }}
                    placeholder="email"
                    autoComplete="username"
                    aria-invalid={!!liveEmailError}
                    aria-describedby={liveEmailError ? "email-live-error" : undefined}
                    className={
                        liveEmailError
                            ? "border-red-400/40 focus:border-red-400/70 focus:ring-[rgba(248,113,113,0.22)]"
                            : ""
                    }
                />

                {liveEmailError && (
                    <div id="email-live-error" className="-mt-1 text-sm text-red-400">
                        {liveEmailError}
                    </div>
                )}

                {/* Password: 즉시 7~72 안내 */}
                <AuthInput
                    label="Password"
                    value={password}
                    onChange={(e) => {
                        if (!touchedPassword) setTouchedPassword(true);
                        setPassword(e.target.value);
                    }}
                    placeholder="password"
                    type="password"
                    autoComplete={isSignup ? "new-password" : "current-password"}
                    aria-invalid={!!passwordFieldError}
                    aria-describedby={passwordFieldError ? "pw-len-error" : undefined}
                    className={
                        passwordFieldError
                            ? "border-red-400/40 focus:border-red-400/70 focus:ring-[rgba(248,113,113,0.22)]"
                            : ""
                    }
                />

                {passwordFieldError && (
                    <div id="pw-len-error" className="-mt-1 text-sm text-red-400">
                        {passwordFieldError}
                    </div>
                )}

                {isSignup && (
                    <>
                        <AuthInput
                            label="Confirm password"
                            value={confirmPassword}
                            onChange={(e) => {
                                if (!touchedConfirm) setTouchedConfirm(true);
                                setConfirmPassword(e.target.value);
                            }}
                            placeholder="confirm password"
                            type="password"
                            autoComplete="new-password"
                            aria-invalid={!!liveConfirmError}
                            aria-describedby={liveConfirmError ? "pw-confirm-error" : undefined}
                            className={
                                liveConfirmError
                                    ? "border-red-400/40 focus:border-red-400/70 focus:ring-[rgba(248,113,113,0.22)]"
                                    : ""
                            }
                        />

                        {liveConfirmError && (
                            <div id="pw-confirm-error" className="-mt-1 text-sm text-red-400">
                                {liveConfirmError}
                            </div>
                        )}
                    </>
                )}

                <AuthButton type="submit" disabled={!canSubmit}>
                    {loading ? (isSignup ? "Creating..." : "Logging in...") : submitLabel}
                </AuthButton>

                {err && <div className="mt-1 text-sm text-red-400">{err}</div>}

                <div className="mt-2 flex items-center justify-between text-[13px] text-white/60">
                    {isSignup ? (
                        <>
                            <Link className="text-[rgba(120,190,255,0.95)] hover:underline" to="/login">
                                Already have an account? Log in
                            </Link>
                            <span />
                        </>
                    ) : (
                        <>
                            <Link className="text-[rgba(120,190,255,0.95)] hover:underline" to="/signup">
                                No account? Register
                            </Link>
                            <button
                                type="button"
                                className="text-[rgba(120,190,255,0.95)] hover:underline"
                                onClick={() => { }}
                            >
                                Forgot your password?
                            </button>
                        </>
                    )}
                </div>
            </form>
        </>
    );
}