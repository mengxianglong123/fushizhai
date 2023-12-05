import React from 'react'
import "./func.scss"
import {Button} from "antd"
import { RightCircleFilled } from '@ant-design/icons';
import hua from "@/assets/imgs/hua.png"
import bi from "@/assets/imgs/bi.png"
import yan from "@/assets/imgs/yan.png"
import shu from "@/assets/imgs/shu.png"
import zhishu from "@/assets/imgs/zhishu.png"

/**
 * 首页功能划分模块
 * @returns 
 */
export default function Func() {
  return (
    <div id="home-func" className='home-func'>
        {/* 画意轩 */}
        <div className='func-item imgtext'>
            {/* 左侧图片 */}
            <div className='left'>
                <img src={hua} alt="" />
            </div>
            {/* 右侧文件 */}
            <div className='right'>
                <h1 className='title'>画意轩</h1>
                <div className='desc'><span className='iconfont icon-dian'/>AI看图作诗，识画明意，创作更有趣</div>
                <div className='desc'><span className='iconfont icon-dian'/>全格律，多词牌，形式更丰富</div>
                <div className='desc'><span className='iconfont icon-dian'/>自定义提示词，风格自由把控</div>
                <Button type='primary' className='btn' icon={<RightCircleFilled/>} size="large">立即体验</Button>
            </div>
        </div>
        {/* 修诗阁 */}
        <div className='func-item fixpoem'>
			{/* 左侧文字 */}
			<div className='left'>
				<h1 className='title'>修诗阁</h1>
				<div className='desc'><span className='iconfont icon-dian'/>全新智能格律校验，不止校验格律</div>
                <div className='desc'><span className='iconfont icon-dian'/>根据诗词语境，智能给出修改建议</div>
                <div className='desc'><span className='iconfont icon-dian'/>诗词创作的智能化助手，让您的作品更出色</div>
                <Button type='primary' className='btn' icon={<RightCircleFilled/>} size="large">开始校验</Button>
			</div>
			{/* 右侧图片 */}
			<div className='right'>
				<img src={yan} alt="" />
			</div>
        </div>
		{/* 思墨堂 */}
		<div className='func-item simo'>
			{/* 左侧图片 */}
			<div className='left'>
				<img src={bi} alt="" />
			</div>
			{/* 右侧文字 */}
			<div className='right'>
				<h1 className='title'>思墨堂</h1>
				<div className='desc'><span className='iconfont icon-dian'/>思文寻意，墨香四浮</div>
                <div className='desc'><span className='iconfont icon-dian'/>一个思路起点，焕发无限灵感</div>
                <div className='desc'><span className='iconfont icon-dian'/>更丝滑，更优雅的诗词灵感工具</div>
                <Button type='primary' className='btn' icon={<RightCircleFilled/>} size="large">寻找灵感</Button>
			</div>
		</div>
		{/* 译书园 */}
		<div className='func-item translation'>
			{/* 左侧文字 */}
			<div className='left'>
				<h1 className='title'>译书园</h1>
				<div className='desc'><span className='iconfont icon-dian'/>古文翻译，一步到位</div>
                <div className='desc'><span className='iconfont icon-dian'/>饱读近百万句文言文，翻译更专业</div>
                <div className='desc'><span className='iconfont icon-dian'/>高效翻译，古文不再是难题</div>
                <Button type='primary' className='btn' icon={<RightCircleFilled/>} size="large">开始翻译</Button>
			</div>
			{/* 右侧图片 */}
			<div className='right'>
				<img src={shu} alt="" />
			</div>
		</div>
    </div>
  )
}
