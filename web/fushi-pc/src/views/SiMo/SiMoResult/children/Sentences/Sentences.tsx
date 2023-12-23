import {useEffect, useState} from 'react'
import {getSentences} from "@/api/simo"
import { Spin, Tag } from  "antd"
import {SyncOutlined} from "@ant-design/icons"
import "./sentences.scss"

interface SentencesProps{
    searchContent:any
}

// 请求数据数量
const num = 30

// 诗词地址
const poemURL = "http://www.menglangpoem.cn/poemDetail/"

export default function Sentences(props:SentencesProps) {
    // 获取搜索内容
    const {searchContent} = props
    // 诗句列表
    const [sentences, setSentences] = useState([])
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
        getSentences(searchContent, num).then((res:any) => {
            if (res.code == 200) {
                setSentences(res.data)
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

    return (
        <div className='simo-sentences'>
            {/* 卡片头部 */}
            <div className='header'>
                {/* 标题 */}
                <div className='title'><span className='iconfont icon-tubiao_shenjijuedingzhihangqingkuang'></span>名句</div>
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
                    sentences.map((item:any, index) => {
                        return  <Tag key={index} className='tag' color="#c04851" onClick={() => toPoem(item.poemId)} style={{backgroundColor:"rgba(255, 225, 225, 0.7)"}}>{item.content}</Tag>
                    })
                }
                
            </div>
        </div>
    )
}
