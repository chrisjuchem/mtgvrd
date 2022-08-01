import React, {useContext} from 'react';
import useFetch from '../util/useFetch';

const LoginCtx = React.createContext({});

const LoginProvider = ({children}) => {
  const [userInfo, loading, setUserInfo, refreshUserInfo] = useFetch('/api/users/me');

  return (
    <LoginCtx.Provider
      value={{
        userInfo,
        loading,
        setUserInfo,
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
