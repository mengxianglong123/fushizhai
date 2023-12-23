import {useEffect, useState} from 'react'
import {getWords} from "@/api/simo"
import { Spin, Tag } from  "antd"
import {SyncOutlined} from "@ant-design/icons"
import "./words.scss"

interface WordsProps{
    searchContent:any
}

// 请求数据数量
const num = 40

export default function Words(props:WordsProps) {
    // 获取搜索内容
    const {searchContent} = props
    // 词汇列表
    const [words, setWords] = useState([])
    // 加载状态
    const [loading, setLoading] = useState(false)

    useEffect(() => {
        refresh()
    }, [])

    /**
     * 刷新数据
     */
    const refresh = () =>  {
        setLoading(true)  // 开始加载
        getWords(searchContent, num).then((res:any) => {
            if (res.code == 200) {
                setWords(res.data)
                setLoading(false) // 停止加载
            }
        })
    }

    return (
        <div className='simo-words'>
            {/* 卡片头部 */}
            <div className='header'>
                {/* 标题 */}
                <div className='title'><span className='iconfont icon-018cidian'></span>词汇</div>
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
                    words.map((item, index) => {
                        return  <Tag  key={index} className='tag' color="blue">{item}</Tag>
                    })
                }
                
            </div>
        </div>
    )
}
