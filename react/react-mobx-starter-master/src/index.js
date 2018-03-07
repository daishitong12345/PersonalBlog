import React from 'react';
import ReactDom from 'react-dom';
import {
  BrowserRouter as Router,
  Route,
  Link
} from 'react-router-dom';
import Login from './component/Login';
import Reg from './component/Reg';

const Home = () => (
  <div>
    <h2>Home</h2>
  </div>
);

const About = () => (
  <div>
    <h2>About</h2>
  </div>
);

const App = () => (
  <Router>
    <div>
      <ul>
        <li><Link to="/">主义</Link></li>
        <li><Link to="/login">登录</Link></li>
        <li><Link to="/reg">注册</Link></li>
        <li><Link to="/about">关于</Link></li>
      </ul>
      <Route path="/about" component={About} />
      <Route exact path="/" component={Home} />
      <Route path="/login" component={Login} />
      <Route path="/reg" component={Reg} />
    </div>
  </Router>
);

ReactDom.render(<App />,document.getElementById('root'));