import NavNormal from "@/components/NavNormal/NavNormal"
import logo from "@/assets/imgs/logo.png"
import { Input } from 'antd';
import "./simo.scss"
import {useNavigate} from "react-router-dom"

const { Search } = Input;


/**
 * 思墨堂
 * @returns 
 */
export default function SiMo() {
	const navigate = useNavigate()

	/**
	 * 触发搜索
	 * @param value 
	 * @returns 
	 */
	const onSearch = (value:any) =>  {
		if (value == "")  return
		// 跳转到结果页面
		navigate("/simoResult/" + value)
	}

	return (
		<div className="simo">
			{/* 导航栏 */}
			<NavNormal/>
			{/* 思墨搜索 */}
			<div className="search">
				{/* 上方logo */}
				<div className="top">
					{/* 图片 */}
					<img src={logo} alt="" />
					{/* 名称 */}
					<span>思墨堂</span>
				</div>
				{/* 搜索框 */}
				<div className="search-input">
					<Search
					placeholder="请输入灵感火花"
					allowClear
					enterButton="寻意思墨"
					size="large"
					className="input"
					onSearch={onSearch}
					/>
				</div>
			</div>
		</div>
	)
}
