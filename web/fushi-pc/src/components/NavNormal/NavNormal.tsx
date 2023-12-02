import { useState } from 'react';
import {useNavigate} from "react-router-dom"
import type { MenuProps } from 'antd';
import { Menu } from 'antd';
import logo from "@/assets/imgs/logo-bigger.png"
import "./NavNormal.scss"

const items: MenuProps['items'] = [
	{
		label: '首页',
		key: 'home'
	},
	{
		label: '画意轩',
		key: 'imgtext'
	},
	{
		label: '修诗阁',
		key: 'fixpoem'
	},
	{
		label: '思墨堂',
		key: 'simo'
	},
	{
		label: '译书园',
		key: 'translation'
	}
];

export default function NavNormal() {
    const navigate = useNavigate()
    const [current, _] = useState(sessionStorage.getItem("current_path"));

	/**
	 * 处理点击后路由跳转
	 * @param e 
	 */
    const onClick: MenuProps['onClick'] = (e) => {
        navigate("/" + e.key)
    };

    return (
        <div className='menu-normal'>
            {/* logo */}
            <img className='logo' src={logo} alt="" />
            {/* 跳转链接列表 */}
            <div className='links'>
                <Menu onClick={onClick} selectedKeys={[current ? current : ""]} mode="horizontal" items={items} />
            </div>
            
            {/* github跳转 */}
            <div className='git hover-color'>
                <a className='hover-color' href="https://github.com/mengxianglong123/fushizhai"  target="_blank">
                    <span className='iconfont icon-GitHub'></span>GitHub仓库
                    <span className='iconfont icon-fenxiang'></span>
                </a>
            </div>
           
        </div>
        
    )
}
