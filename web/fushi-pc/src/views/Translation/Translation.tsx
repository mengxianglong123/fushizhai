import NavNormal from '@/components/NavNormal/NavNormal'
import "./translation.scss"
import { Button, Form, Input } from 'antd';
import {useState} from "react"
import {translate} from "@/api/translation"



  
const onFinishFailed = (errorInfo: any) => {
    console.log('Failed:', errorInfo);
};

/**
 * 古文翻译-译书园
 * @returns 
 */
export default function Translation() {

    // 翻译结果
    const [result, setResult] = useState("古文翻译，一键到位")

    const onFinish = (values: any) => {
        // 开始翻译
        setResult("翻译中，请稍后...")
        translate(values).then((res:any) => {
            if (res.code == 200) {
                // 翻译结束
                setResult(res.data)
            }
        })
    };

    return (
        <div className='translation page-full'>
            {/* 导航栏 */}
            <NavNormal/>
            {/* 卡片 */}
            <div className='card'>
                {/* 左侧输入框 */}
                <div className='left'>
                    <Form
                        name="basic"
                       
                        onFinish={onFinish}
                        onFinishFailed={onFinishFailed}
                        autoComplete="off"
                    >
                        <Form.Item
                        name="text"
                        rules={[{ required: true, message: '请输入古文原文' }]}
                        >
                            <Input.TextArea className='input' placeholder='请输入古文原文' maxLength={128} count={{max:128, show:true}} bordered={false} style={{resize:"none", boxShadow:"none"}}/>
                        </Form.Item>

                        <Form.Item>
                            <Button type="primary" htmlType="submit"  className='btn' shape="round"  size='large'>
                                立即翻译
                            </Button>
                        </Form.Item>
                    </Form>
                </div>

                {/* 右侧翻译结果 */}
                <div className='right'>
                    {result}
                </div>
            </div>
        </div>
    )
}
