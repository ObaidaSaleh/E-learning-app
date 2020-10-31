import React from 'react';
import './App.css';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link,
  useHistory
} from "react-router-dom";

import About from './landing/About/About.js';
import Home from './landing/Home/Home.js';
import SignUp from './landing/SignUp/SignUp/SignUp.js'
import Courses from './courses/Courses/Courses.js';
import Login from './landing/login/Login/Login.js';
import TopBar from './utils/Navigation.js';
import Logout from './landing/login/Logout/Logout.js';

function App() {

  const [loggedIn, setLoggedIn] = React.useState(false);

/*  React.useEffect(() => {
      var token = JSON.parse(localStorage.getItem("jwtAuthToken"))
      if ( token === null) {
        console.log(loggedIn)
      } else {
        console.log(loggedIn)
      }
    }, [loggedIn])*/

  return (
    <Router>
      <div className="header">
        <TopBar loggedIn={loggedIn} />

        {/* A <Switch> looks through its children <Route>s and
            renders the first one that matches the current URL. */}
        <Switch>
          <Route path="/about">
            <About />
          </Route>
          <Route path="/logout">
            <Logout
              setLoggedIn={setLoggedIn}
            />
          </Route>
          <Route path="/login">
            <Login
                setLoggedIn={setLoggedIn}
             />
          </Route>
          <Route path="/create">
            <Courses />
          </Route>
          <Route path="/SignUp">
                <SignUp />
            </Route>
          <Route path="/">
            <Home />
          </Route>

        </Switch>
      </div>
    </Router>
  );
}

export default App;
