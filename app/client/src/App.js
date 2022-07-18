import logo from './logo.svg';
import './App.css';

import {useEffect, useState} from 'react';

function App() {
  const [text, setText] = useState(<p>Edit <code>src/App.js</code> and save to reload.</p>)

  useEffect(() => {
    setTimeout(async () => {
      const resp = await fetch('/ping');
      setText(<p>{await resp.text()}</p>);
    }, 1000);
  }, [])

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        {text}
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
