import React from "react";

function LogoMark() {
    return (
        <div className="relative grid place-items-center size-14" aria-hidden="true">
            <div
                className="size-14 rounded-full"
                style={{
                    background:
                        "conic-gradient(from 220deg, #ffb74a, #ff4fd8, #6ea8ff, #ffb74a)",
                    WebkitMask: "radial-gradient(circle, transparent 56%, #000 57%)",
                    mask: "radial-gradient(circle, transparent 56%, #000 57%)",
                }}
            />
            <div
                className="absolute size-2.5 rounded-full shadow-[0_0_18px_rgba(255,183,74,0.55)]"
                style={{ background: "#ffb74a", transform: "translate(14px,-14px)" }}
            />
        </div>
    );
}

function AuthFooter() {
    return (
        <div className="mt-6 hidden md:flex justify-center gap-2 text-xs text-white/50">
            <span>Documentation</span>
            <span>·</span>
            <span>Support</span>
            <span>·</span>
            <span>Community</span>
            <span>·</span>
            <span>Open Source</span>
        </div>
    );
}

export default function AuthLayout({
    title,
    children,
}: {
    title: string;
    children: React.ReactNode;
}) {
    return (
        <div className="min-h-screen px-4 py-12 text-white">
            {/* background */}
            <div
                className="fixed inset-0 -z-10"
                style={{
                    background: `
            radial-gradient(1200px 800px at 20% 15%, rgba(255, 99, 232, 0.25), transparent 60%),
            radial-gradient(1200px 800px at 80% 20%, rgba(93, 170, 255, 0.25), transparent 60%),
            radial-gradient(900px 700px at 50% 80%, rgba(255, 180, 90, 0.12), transparent 55%),
            linear-gradient(135deg, #0b0f1a, #1a1033 45%, #2b1559)
          `,
                }}
            />
            {/* vignette */}
            <div
                className="fixed inset-0 -z-10 pointer-events-none"
                style={{
                    background:
                        "radial-gradient(circle at 50% 40%, transparent 40%, rgba(0,0,0,0.55) 100%)",
                }}
            />

            {/* ✅ Shell: 가운데 정렬 + 반응형 패딩 */}
            <div className="mx-auto flex min-h-screen w-full max-w-130 flex-col justify-center">
                <div className="rounded-[14px] border border-white/10 bg-[rgba(15,18,28,0.88)] p-6 shadow-[0_24px_80px_rgba(0,0,0,0.55)] backdrop-blur sm:p-7">
                    <div className="mb-5 grid justify-items-center gap-3.5">
                        <LogoMark />
                        <h1 className="m-0 text-[24px] font-semibold tracking-[-0.02em] text-white/90 sm:text-[28px]">
                            {title}
                        </h1>
                    </div>

                    {children}
                </div>

                <AuthFooter />
            </div>
        </div>
    );
}