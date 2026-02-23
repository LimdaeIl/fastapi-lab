import React from "react";

type Props = React.InputHTMLAttributes<HTMLInputElement> & {
    label: string;
};

export default function AuthInput({ label, className = "", ...props }: Props) {
    return (
        <label className="grid gap-2">
            <span className="text-xs text-white/65">{label}</span>
            <input
                {...props}
                className={[
                    "w-full rounded-[10px] border border-white/10 bg-white/5 px-3 py-3 text-white/90",
                    "outline-none placeholder:text-white/35",
                    "focus:border-[rgba(88,166,255,0.75)] focus:ring-4 focus:ring-[rgba(88,166,255,0.22)]",
                    className,
                ].join(" ")}
            />
        </label>
    );
}