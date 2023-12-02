import { Carousel } from 'antd';
import "./banner.scss"
import banner1 from "@/assets/imgs/banner1.png"
import banner2 from "@/assets/imgs/banner2.jpg"
import banner3 from "@/assets/imgs/banner3.jpg"
import { Button } from 'antd'
import { EditOutlined  } from '@ant-design/icons'
import jumpAndFlicker from '@/utils/jumpAndFlicker';

/**
 * 首页轮播图模块
 * @returns 
 */
export default function Banner() {
    return (
        <div className='home-banner'>
            {/* 遮罩 */}
            <div className='mask'></div>
            {/* 轮播图 */}
            <Carousel effect='fade' className='banners' autoplay pauseOnHover={false}  easing='ease-in-out' speed={2000} autoplaySpeed={5000}>
                <div className='banner-item'>
                    <img src={banner1}/>
                </div>
                <div className='banner-item'>
                    <img src={banner2}/>
                </div>
                <div className='banner-item'>
                    <img src={banner3}/>
                </div>
            </Carousel>
            {/* 中间文字内容 */}
            <div className='content'>
                <h1 className='title'>红笺小字 为你写诗</h1>
                <h2 className='mini-title'>赋诗斋：一个基于AI的智能诗词创作平台</h2>
                {/* <div className='desc'>赋诗斋：一个基于AI的智能诗词创作平台</div> */}
                <Button className='btn' type="primary" icon={<EditOutlined />} size="large" ghost onClick={() => jumpAndFlicker("home-func")}>赋诗一首</Button>
            </div>
        </div>
    )
}
