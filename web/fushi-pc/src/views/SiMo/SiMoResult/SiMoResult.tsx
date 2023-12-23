import {useEffect, useState} from 'react'
import {useParams} from "react-router-dom"
import NavNormal from '@/components/NavNormal/NavNormal'
import logo from "@/assets/imgs/logo.png"
import { Input} from 'antd'
import "./simoResult.scss"
import Words from './children/Words/Words'
import Sentences from './children/Sentences/Sentences'

const { Search } = Input;

export default function SiMoResult() {
    // 接收参数
    const {content} = useParams()
    

    /**
     * 挂载时执行
     */
    useEffect(() => {
        
    },[])

    /**
	 * 触发搜索
	 * @param value 
	 * @returns 
	 */
	const onSearch = (value:any) =>  {
        window.location.href = "/simoResult/" + value
    }
    
    return (
        <div className='simo-result'>
            {/* 通用导航栏 */}
            <NavNormal/>

            {/* 搜索框 */}
            <div className='search'>
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
                        defaultValue={content}
                        
					/>
				</div>
            </div>
            {/* 结果 */}
            <div className='results'>
                {/* 词汇 */}
                <Words searchContent={content}/>
                {/* 诗句 */}
                <Sentences searchContent={content}/>
                {/* 诗词 */}
            </div>
        </div>
    )
}
