import {useEffect, useState} from 'react'
import {getSentences} from "@/api/simo"
import { Spin, Tag } from  "antd"
import {SyncOutlined} from "@ant-design/icons"
import "./sentences.scss"

interface SentencesProps{
    searchContent:any
}



export default function Sentences() {
  return (
    <div>Sentences</div>
  )
}
