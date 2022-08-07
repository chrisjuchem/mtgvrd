import React, {useContext} from 'react';
import useFetch from '../util/useFetch';

const LoginCtx = React.createContext({});

const LoginProvider = ({children}) => {
  const [checkInfo, loading, _setCheckInfo, refreshUserInfo] = useFetch('/login/check');
  const {logged_in: loggedIn, ...userInfo} = checkInfo || {};

  return (
    <LoginCtx.Provider
      value={{
        loading,
        loggedIn,
        userInfo,
        refreshUserInfo,
      }}
    >
      {children}
    </LoginCtx.Provider>
  );
};

const useLogin = () => useContext(LoginCtx);
const useLoginInfo = () => useContext(LoginCtx).userInfo;

export {useLogin, useLoginInfo, LoginProvider};
