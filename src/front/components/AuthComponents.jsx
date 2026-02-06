import { useEffect } from "react";
import useGlobalReducer from "../hooks/useGlobalReducer";
import { useNavigate } from "react-router-dom";

const AOrB = ({ loggedInComponent, loggedOutComponent }) => {
    const { store } = useGlobalReducer();

    return <>{store.token ? loggedInComponent : loggedOutComponent}</>
}

const AuthedOrNone = ({ children }) => {
    return <AOrB
        loggedInComponent={children}
        loggedOutComponent=""
    />
}

const UnauthedOrNone = ({ children }) => {
    return <AOrB
        loggedInComponent=""
        loggedOutComponent={children}
    />
}

const AuthedOrRedirect = ({ children, to = "/" }) => {
    const { store } = useGlobalReducer();
    const nav = useNavigate();

    useEffect(() => {
        if (!store.token) {
            nav(to);
        }
    }, [])

    return <>{children}</>
}

export {
    AOrB,
    AuthedOrNone,
    UnauthedOrNone,
    AuthedOrRedirect,
}
