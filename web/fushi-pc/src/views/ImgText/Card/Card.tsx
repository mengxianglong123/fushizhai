import "./card.scss"

interface CardProps {
    loading:boolean,
    result:string
}
/**
 * 画意轩诗词卡片
 * @param props 
 * @returns 
 */
export default function Card(props:CardProps) {

    /**
     * 分割字符
     * @param result 
     * @returns 
     */
    const splitResult = (result:string) => result.split("，")
    
    return (
        <div className="imgtext-card">
            {
                props.loading ?
                <div className="title">生成中 请稍后</div>
                :
                <div className="title">赋诗斋·画意轩</div>
            }
            
            
            {/* 正文内容 */}
            <div className="content">
                {splitResult(props.result).map(item => {
                    return <div key={item} className="content-line">{item}</div>
                })}
            </div>
        </div>
    )
}
