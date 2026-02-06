import { AuthedOrRedirect } from "../components/AuthComponents"

const SecretPage = () => {
    return <AuthedOrRedirect>
        <h1>If you can see this, you're logged in.</h1>
    </AuthedOrRedirect>
}

export { SecretPage }