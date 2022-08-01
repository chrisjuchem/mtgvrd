import discordLogo from './discordLogo.svg';

const LOGOS = {
  discord: discordLogo,
};

const LoginButton = ({provider}) => (
  <a
    href={`/login/${provider}/redirect?back_to=${window.location.pathname}`}
    className={`button loginButton ${provider}`}
    tabIndex={99}
  >
    <img src={LOGOS[provider]} className="socialIcon" />
    Login with {provider.charAt(0).toUpperCase() + provider.slice(1)}
  </a>
);

export default LoginButton;
