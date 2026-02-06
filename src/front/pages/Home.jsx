import React, { useEffect } from "react"
import { Signup, Login } from "../components/Auth.jsx";
import { AOrB, AuthedOrNone, UnauthedOrNone } from "../components/AuthComponents.jsx";

import useGlobalReducer from "../hooks/useGlobalReducer.jsx";
import { Link } from "react-router-dom";


export const Home = () => {

	const { store, dispatch } = useGlobalReducer()

	return (
		<div className="text-center mt-5">
			<div className="row">
				<div className="col col-6 offset-3">
					<UnauthedOrNone>
						<Login />
					</UnauthedOrNone>
				</div>
			</div>
			<div className="row">
				<div className="col col-3 offset-3">
					<AOrB
						loggedInComponent={<div>
							<p>You're logged in!</p>
							<button className="btn btn-danger" onClick={() => dispatch({
								type: "update_token",
								token: null,
							})}>
								Click to logout
							</button>
						</div>}
						loggedOutComponent={<p>You're not logged in...</p>}
					/>
				</div>
				<div className="col col-3">
					<AuthedOrNone>
						<p>If this is showing up, you're logged in.</p>
						<p><Link to="/secret">See the secret page here!</Link></p>
					</AuthedOrNone>
				</div>
			</div>
		</div >
	);
}; 