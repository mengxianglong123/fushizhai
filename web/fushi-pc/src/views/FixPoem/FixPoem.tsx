import "./fixpoem.scss"
import NavNormal from "@/components/NavNormal/NavNormal"
import { Button, Form, Radio, Input, Select,  } from 'antd';
import {useState, useEffect} from "react"
import {getRhymeRulesByType, getRhymeBookNames} from "@/api/imgtext"
import { FixPoemForm } from "@/types/fixpoem";
import { checkRhyme } from "@/api/fixpoem";

const onFinishFailed = (errorInfo: any) => {
    console.log('Failed:', errorInfo);
}

export default function FixPoem() {
    
    // 表单数据
    const [form] = Form.useForm();
    // 规则列表
    const [ruleList, setRuleList] = useState([])
    // 韵书列表
    const [rhymeBooks, setRhymeBooks] = useState([])
    // 校验文本
    const [poem, setPoem] = useState("")
    // 校验结果
    const [result, setResult] = useState([])

    /**
     * 加载完成时执行
     */
    useEffect(() => {
        // 初始化规则列表
        let ruleType = "0" // 初始化默认为词牌
        getRhymeRulesByType(ruleType).then((res:any) => {
            if (res.code === 200) {
                setRuleList(res.data)
            }
        })
        // 获取韵书名称
        getRhymeBookNames().then((res:any) => {
            if (res.code === 200) {
                setRhymeBooks(res.data)
            }
        })
    }, [])

    /**
     * 表单成功提交
     * @param values 
     */
    const onFinish = (values: any) => {
        // 1.清除校验文本的回车和空格
        values.poem = values.poem.replace("\n","").replace(" ","")
        // 2.发送请求，进行格律校验
        checkRhyme(values).then((res:any) => {
            if (res.code === 200) {
                setResult(res.data)
            }
        })
    }

    /**
     * 处理韵律类型发生变化
     * @param e 
     */
    const handleRuleTypeChange = (e:any) => {
        // 获取指定类型下的规则列表
        getRhymeRulesByType(e.target.value).then((res:any) => {
            if (res.code === 200) {
                setRuleList(res.data)
            }
        })   
    }

    /**
     * 将列表转为可以带value属性
     * @param ruleList 
     */
    const mapListWithLabel = (list:never[]) => {
        const newList = list.map(item => ({label:item, value: item}))
        return newList
    }

    return (
        <div className="fixpoem">
            {/* 普通导航栏 */}
            <NavNormal/>
            {/* 主要内容 */}
            <div className="fixpoem-main">
                {/* 左侧表单 */}
                <div className="left">
                    <Form
                        name="fixpoem-form"
                        className="fixpoem-form"
                        // labelCol={{ span: 8 }}
                        // wrapperCol={{ span: 16 }}
                        style={{ maxWidth: 600 }}
                        initialValues={{ remember: true }}
                        onFinish={onFinish}
                        onFinishFailed={onFinishFailed}
                        autoComplete="off"
                        // onValuesChange={(changedValues, allValues) => { setFormData(allValues) }}
                        form={form}
                        layout="vertical"
                        >

                            {/* 校验文本 */}
                            <Form.Item<FixPoemForm>
                                label="校验文本"
                                name="poem"
                                rules={[{ required: true, message: '请输入校验文本' }]}
                            >
                                <Input.TextArea style={{height:"150px"}} placeholder="请输入校验文本"/>
                            </Form.Item>

                            {/* 韵律类型 */}
                            <Form.Item<FixPoemForm>
                                label="韵律类型"
                                name="ruleType"
                                rules={[{ required: true, message: '请选择韵律类型' }]}
                                initialValue="0"
                            >
                                <Radio.Group onChange={(e) => handleRuleTypeChange(e)}>
                                    <Radio value="0">律诗</Radio>
                                    <Radio value="1">词牌</Radio>
                                </Radio.Group>
                            </Form.Item>

                            {/* 规则列表 */}
                            <Form.Item<FixPoemForm>
                                label="韵律规则"
                                name="ruleName"
                                rules={[{required:true, message:"请选择韵律规则"}]}
                            >
                                <Select
                                    style={{ width: 220 }}
                                    placeholder="请选择韵律规则"
                                    options={mapListWithLabel(ruleList)}
                                />
                            </Form.Item>

                            {/* 韵书 */}
                            <Form.Item<FixPoemForm>
                                label="韵书"
                                name="bookName"
                                rules={[{required:true, message:"请选择韵书"}]}
                            >
                                <Select
                                    style={{ width: 220 }}
                                    placeholder="请选择韵书"
                                    options={mapListWithLabel(rhymeBooks)}
                                />
                            </Form.Item>


                            <Form.Item >
                                <Button className="btn" type="primary" htmlType="submit" size="large" style={{ marginTop:"15px"}}>
                                    开始校验
                                </Button>
                            </Form.Item>
                    </Form>
                </div>
                {/* 右侧校验结果 */}
                <div className="right">

                </div>
            </div>

        </div>
    )
}
