import {useEffect, useState} from 'react'
import {getPoems} from "@/api/simo"
import { Spin, Tag } from  "antd"
import {SyncOutlined} from "@ant-design/icons"
import "./poem.scss"

interface PoemsProps{
    searchContent:any
}

// 请求数据数量
const num = 30

// 诗词地址
const poemURL = "http://www.menglangpoem.cn/poemDetail/"

export default function Poems(props:PoemsProps) {
    // 获取搜索内容
    const {searchContent} = props
    // 诗词列表
    const [poems, setPoems] = useState([])
    // 加载状态
    const [loading, setLoading] = useState(false)

    /**
     * 挂载后执行
     */
    useEffect(() => {
        refresh()
    }, [])

    /**
     * 刷新数据
     */
    const refresh = () =>  {
        setLoading(true)  // 开始加载
        getPoems(searchContent, num).then((res:any) => {
            if (res.code == 200) {
                setPoems(res.data)
                setLoading(false) // 停止加载
            }
        })
    }

    /**
     * 跳转至
     * @param id 
     */
    const toPoem = (id:number) => {
        window.open(poemURL + id)
    }

    /**
     * 移除字符串的em标签
     * @param s 
     */
    const removeEmTag = (s:string) =>  {
        return s.replace(/<em>/g,"").replace(/<\/em>/g,"")
    }


    return (
        <div className='simo-poems'>
            {/* 卡片头部 */}
            <div className='header'>
                {/* 标题 */}
                <div className='title'><span className='iconfont icon-gushu'></span>诗词</div>
                {/* 更新按钮 */}
                <div className='refresh' onClick={refresh}>
                    {
                        loading ?
                        <SyncOutlined className='icon' spin />
                        :
                        <SyncOutlined className='icon' />
                    }
                    
                    换一批
                </div>
            </div>
            {/* 内容列表 */}
            <div  className='content-list'>
                {
                    loading == true ? 
                    // 加载进度
                    <Spin className='loading-item' size="large"/>
                    :
                    // 结果渲染
                    poems.map((item:any, index) => {
                        return  <Tag key={index} className='tag' style={{backgroundColor:"rgba(153,119,170, 0.2)"}} onClick={() => toPoem(item.id)}>《{removeEmTag(item.title)}》 --{removeEmTag(item.dynasty)}·{removeEmTag(item.poetName)}</Tag>
                    })
                }
                
            </div>
        </div>
    )
}
