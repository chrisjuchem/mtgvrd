import {Link, NavLink} from 'react-router-dom';

import './nav.scss';
import UserDropdown from './userDropdown';
import {useLogin} from '../../contexts/login';
import LoginButton from './loginButton';

const NAV_LINKS = [
  ['Foo', '/foo'],
  ['Home', '/'],
  ['Foo2', '/foo'],
];

const NavBar = () => {
  const {userInfo, loading} = useLogin();

  return (
    <div className="nav">
      {/* TODO: skip to content button */}

      <Link to={'/'} className="navLink" tabIndex={2}>
        <div className={'homeLink'}>MTGVRD</div>
      </Link>

      {NAV_LINKS.map(([display, path], i) => (
        <NavLink key={display} to={path} className="navLink" tabIndex={i + 3}>
          {display}
        </NavLink>
      ))}

      <div className="separator" />

      {!loading && (userInfo ? <UserDropdown {...userInfo} /> : <LoginButton provider="discord" />)}
    </div>
  );
};

export default NavBar;
