import React from "react";

export default function AuthButton({
    className = "",
    ...props
}: React.ButtonHTMLAttributes<HTMLButtonElement>) {
    return (
        <button
            {...props}
            className={[
                "mt-1 w-full rounded-[10px] bg-blue-500 py-3 font-semibold text-white",
                "hover:bg-blue-600 active:translate-y-px disabled:opacity-60",
                className,
            ].join(" ")}
        />
    );
}