import './App.css'
import {StytchLogin, IdentityProvider,useStytchUser} from '@stytch/react';

function App() {
  const user = useStytchUser();

  const config={
  "products": [
    "oauth",
    "emailMagicLinks"
  ],
  "oauthOptions": {
    "providers": [
      {
        "type": "google"
      }
    ],
    "loginRedirectURL": "https://www.stytch.com/login",
    "signupRedirectURL": "https://www.stytch.com/signup"
  },
  "emailMagicLinksOptions": {
    "loginRedirectURL": "https://www.stytch.com/login",
    "loginExpirationMinutes": 30,
    "signupRedirectURL": "https://www.stytch.com/signup",
    "signupExpirationMinutes": 30
  },
  "otpOptions": {
    "methods": [],
    "expirationMinutes": 5
  },
  "passwordOptions": {
    "loginRedirectURL": "https://www.stytch.com/login",
    "resetPasswordRedirectURL": "https://www.stytch.com/reset-password"
  }
}
  return (
    <div>
      {!user?<StytchLogin config={}/>:<IdentityProvider/>}  
    </div>
  )
}

export default App
