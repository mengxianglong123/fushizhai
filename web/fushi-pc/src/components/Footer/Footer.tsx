import qrcode  from "@/assets/imgs/qrcode.jpg"
import moment from "moment"
import "./footer.scss"

export default function Footer() {
	return (
		<div  className='footer'>
			{/* 信息 */}
			<div className='info'>
				{/* 友情链接 */}
				<div className='links'>
					<div className='title'>友情链接</div>
					<div  className='link-list'>
						<a href="http://www.menglangpoem.cn/" target='_blank'>孟郎诗词网</a>
						<a href="https://www.gushiwen.cn/" target='_blank'>古诗文网</a>
						<a href="https://www.shicimingju.com/" target='_blank'>诗词名句网</a>
						<a href="https://www.sou-yun.cn/index.aspx" target='_blank'>搜韵网</a>
					</div>
				</div>
				{/* 媒体信息 */}
				<div className='media'>
					{/* 公众号 */}
					<div className='wechat'>
						{/* 图片 */}
						<img src={qrcode} alt="" />
						{/* 文字 */}
						<div className="text">孟郎诗词网公众号</div>
					</div>
				</div>
			</div>
			{/* 版权 */}
			<div className="copyright">
				Copyright © 2019 - {moment().year()} | 
				<a className="link-item" href="https://beian.miit.gov.cn" target="_blank"> 冀ICP备18037093号 </a>
				 | 孟郎诗词版权所有
			</div>
		</div>
	)
}
