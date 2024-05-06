import logo from './logo.svg';
import './App.css';
import Home from './app/Home';
import Search from './app/Search';
import { BrowserRouter as Router, Link } from 'react-router-dom';
import { Routes, Route } from 'react-router-dom';
import { MyContext } from './MyContext';
import { useState } from 'react';

function App() {
  const [tweetText, setTweetText] = useState("");

  return (
    <div>
        <MyContext.Provider value={{ tweetText, setTweetText }}>
          <Router>
            <Routes>
              <Route exact path= "/" element={<Home/>} />
              <Route path= "/search" element={<Search/>} />
            </Routes>
          </Router>
        </MyContext.Provider>
    </div>
  );
}

export default App;