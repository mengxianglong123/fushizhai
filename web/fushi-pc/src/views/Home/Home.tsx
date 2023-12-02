import Banner from './children/Banner/Banner'
import NavNormal from '@/components/NavNormal/NavNormal'
import NavTrans from '@/components/NavTrans/NavTrans'
import Func from './children/Func/Func'
import {useEffect, useState} from "react"
import "./home.scss"


/**
 * 首页
 * @returns 
 */
export default function Home() {
    // 定义状态，用于控制当前显示的导航栏类型
    let [navType, setNavType] = useState(0)

    /**
     * 监听页面滚动
     */
    const scrollChange = () => {
        // 监听滚动条距离顶部距离，缓动超过80像素换为透明导航栏
        if (document.documentElement.scrollTop > 80) setNavType(1)
        else setNavType(0)
    }

    useEffect(() => {
        // 滚动条滚动时触发
        window.addEventListener('scroll', scrollChange, true)
        scrollChange()
        return () => {
            window.removeEventListener('scroll', scrollChange, false)
        }
    }, [])


    return (
        <div  className='home'>
            {/* 暂时展示导航栏 */}
            {navType === 0 ? <NavTrans/> : <NavNormal/>}
            {/* 满屏轮播图展示 */}
            <Banner/>
            {/* 各个功能模块 */}
            <Func/>
        </div>
    )
}
