import React from 'react'
import "./resultcard.scss"

interface ResultCardProps{
    loading:boolean,
    result:[],
    poem:string
}

export default function ResultCard(props:ResultCardProps) {
    /**
     * 分割诗词原文
     * @param poem 
     */
    const splitPoem = (poem:string) => {
        return poem.split(/,，。？！!/)
    }
    
    return (
        <div>ResultCard</div>
    )
}
