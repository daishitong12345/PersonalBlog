import React from 'react';
import { Link } from 'react-router-dom';
import '../css/login.css'

const userService = new userService();

export default class Login extends React.Component {
    handleClick(event){
        event.preventDefault()   //取消默认
        //console.log(event.target);
        const fm = event.target.form;
        let email = fm[0].value;
        let pwd = fm[1].value;
        console.log(email,pwd)
    }
    render() {
        return (
            <div className="login-page">
                <div className="form">
                    <form className="login-form">
                        <input type="text" placeholder="邮箱" />
                        <input type="password" placeholder="密码" />
                        <button onClick={this.handleClick.bind(this)} >登录</button>
                        <p className="message">还未注册? <Link to="/reg">请注册</Link></p>
                    </form>
                </div>
            </div>
        );
    }
}