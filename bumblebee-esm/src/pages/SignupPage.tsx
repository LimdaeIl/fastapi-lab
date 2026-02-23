import AuthLayout from "../components/auth/AuthLayout";
import AuthForm from "../components/auth/AuthForm";


export default function SignupPage() {
    return (
        <AuthLayout title="Create your account">
            <AuthForm mode="signup" />
        </AuthLayout>
    );
}