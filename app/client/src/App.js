import {BrowserRouter, Route, Routes} from 'react-router-dom';
import logo from './logo.svg';
import './App.scss';
import NavBar from './components/nav/nav';
import {LoginProvider} from './contexts/login';
import Footer from './components/footer/footer';

const TempHomePage = () => (
  <div className="page">
    <img src={logo} className="App-logo" alt="logo" style={{height: '40vmin'}} />
    <a className="App-link" href="https://reactjs.org" target="_blank" rel="noopener noreferrer">
      Learn React
    </a>
    <div>TEST</div>
    <div>TEST</div>
    <div>TEST</div>
    <div>TEST</div>
    <div>TEST</div>
    <div>TEST</div>
    <div>TEST</div>
    <div>TEST</div>
    <div>TEST</div>
    <div>TEST</div>
    <div>TEST</div>
    <div>TEST</div>
    <div>TEST</div>
    <div>TEST</div>
    <div>TEST</div>
    <div>TEST</div>
    <div>TEST</div>
    <div>TEST</div>
    <div>TEST</div>
    <div>TEST</div>
    <div>TEST</div>
    <div>TEST</div>
    <div>TEST</div>
    <div>TEST</div>
    <div>TEST</div>
    <div>TEST</div>
    <div>TEST</div>
    <div>TEST</div>
    <div>TEST</div>
    <div>TEST</div>
    <div>TEST</div>
    <div>TEST</div>
    <div>TEST</div>
    <div>TEST</div>
  </div>
);

function App() {
  return (
    <BrowserRouter>
      <LoginProvider>
        <NavBar />

        <div className="app">
          <div className="content">
            <Routes>
              <Route path="foo" element={<div className="page"> FOO </div>} />
              <Route index element={<TempHomePage />} />
            </Routes>
          </div>
          <Footer />
        </div>
      </LoginProvider>
    </BrowserRouter>
  );
}

export default App;
