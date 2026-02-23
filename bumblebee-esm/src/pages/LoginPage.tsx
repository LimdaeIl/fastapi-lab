import AuthLayout from "../components/auth/AuthLayout";
import AuthForm from "../components/auth/AuthForm";


export default function LoginPage() {
  return (
    <AuthLayout title="Welcome to Bumblebee ESM">
      <AuthForm mode="login" />
    </AuthLayout>
  );
}
