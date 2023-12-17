import React from 'react'
import "./resultcard.scss"
import {Popover} from "antd"
import {CloseCircleOutlined} from "@ant-design/icons"

interface ResultCardProps{
    loading:boolean,
    result:any[],
    poem:string
}

interface CharProps{
    item:string,
    row:number,
    column:number,
    result:any[]
}



function Char(props:CharProps) {
    /**
     * 判断某行某列是否包含错误
     * @param row 
     * @param column 
     * @param result 
     */
    const hasError = (row:number, column:number, result:any[]) => {
        for (let i = 0; i < result.length; i++) {
            if (result[i].row == row && result[i].column == column){
                return result[i]
            }
        }
        return false
    }

    const suggestStyle = {display:"inline-block",border:"1px solid #dcdfe6",width:"25px",height:"25px",textAlign:"center",margin:"5px",fontSize:"16px",
                        padding:"5px", borderRadius:"6px"}

    const {item, row, column, result} = props

    const err = hasError(row, column, result)

    const content = (<div className='suggest'>
                        {/* 平仄错误 */}
                        <div className='suggest-line'>
                            {err?.is_pingze_err ? <div style={{color:"red"}}><CloseCircleOutlined/> 平仄错误</div> : <></>}
                        </div>
                        {/* 韵律错误 */}
                        <div className='suggest-line'>
                            {err?.is_meter_err ? <div style={{color:"red"}}><CloseCircleOutlined/> 韵律错误</div> : <></>}
                        </div>
                        {/* 修改建议 */}
                        <div className='suggest-line'>
                            <div className='suggest-title' style={{fontWeight:"bold"}}>AI修改建议：</div>
                            <div className='suggest-list'>
                                {err?.suggests?.slice(0, 10).map((s:any) => {  // 截取前十条作为修改建议
                                    return <div style={suggestStyle} key={s} className='suggest-item'>{s}</div>
                                })}
                            </div>
                        </div>
                    </div>)
    
    return (
        <div className='fixpoem-char'>
             {
                err == false ?
                <div className='fixpoem-char-item'>{item}</div>
                :
                <Popover content={content} title="智能校验结果">
                    <div className='fixpoem-char-item fixpoem-char-err'>{item}</div>
                </Popover>
            }
        </div>
       
    )
}

export default function ResultCard(props:ResultCardProps) {
    /**
     * 分割诗词原文
     * @param poem 
     */
    const splitPoem = (poem:string) => {
        console.log()
        let poems = poem.split(/[,，。？！!]/)
        if(poems[-1] == "") return poems.slice(0, -1)
        return poems
    }

    

    return (
        <div className='fixpoem-result'>
            <div className='result-title'><span className='iconfont icon-zongcejieguochakan'></span>校验结果</div>
            <div className='result-content'>
                {/* 遍历诗词 */}
                {splitPoem(props.poem).map((line, i) => {
                    return <>
                        {
                            [...line].map((item, j) => {
                                return <Char item={item} row={i} column={j} result={props.result}/>
                            })
                        }
                        {/* 换行 */}
                        <br></br> 
                    </>
                })}
            </div>
        </div>
    )
}
