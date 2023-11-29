import Banner from './children/Banner/Banner'
import NavTrans from '@/components/NavTrans/NavTrans'

/**
 * 首页
 * @returns 
 */
export default function Home() {
    return (
        <div  className='home'>
            {/* 暂时展示导航栏 */}
            <NavTrans/>
            {/* 满屏轮播图展示 */}
            <Banner/>
        </div>
    )
}
