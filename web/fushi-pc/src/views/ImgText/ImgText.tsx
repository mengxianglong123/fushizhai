import NavNormal from "@/components/NavNormal/NavNormal";
import { ImgTextForm } from "@/types/imgtext";
import { Button, Form, Radio, Input, Upload, Select, Modal, message } from 'antd';
import {InboxOutlined} from "@ant-design/icons"
import "./imgtext.scss"
import {useEffect, useState}  from "react"
import {getRhymeRulesByType, getRhymeBookNames, getPoemCanRhyme, createRhymePoem} from "@/api/imgtext"
import Card from "./Card/Card";



const onFinishFailed = (errorInfo: any) => {
    console.log('Failed:', errorInfo);
}

const normFile = (e: any) => {
    if (Array.isArray(e)) {
      return e;
    }
    return e?.fileList;
}


/**
 * 画意轩
 * @returns 
 */
export default function ImgText() {
    // 消息提示
    const [messageApi, contextHolder] = message.useMessage();
    // 表单数据
    const [form] = Form.useForm();
    const [formData, setFormData] = useState<ImgTextForm>();
    // 规则列表
    const [ruleList, setRuleList] = useState([])
    // 韵书列表
    const [rhymeBooks, setRhymeBooks] = useState([])
    // 韵脚列表
    const [rhymes, setRhymes] = useState([])
    // 控制对话框是否开启
    const [isModalOpen, setIsModalOpen] = useState(false);
    // 当前选择的韵脚
    const [curRhyme, setCurRhyme] = useState("")
    // 当前生成状态
    const [loading, setLoading] = useState(false)
    // 当前生成结果
    const [result, setResult] = useState("红笺小字，为你写诗")

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
     * 选择韵脚结束后，信息的最终提交
     */
    const handleOk = () => {
        // 判空
        if (curRhyme == "") {
            messageApi.open({
                type: 'error',
                content: '请选择韵脚',
            });
            return
        }
        // 关闭对话框
        setIsModalOpen(false)
        // 开始生成
        setLoading(true)
        // 发送请求进行创作
        createRhymePoem({...formData, rhyme:curRhyme}).then((res:any) => {
            // 生成完成
            setLoading(false)
            if (res.code == 200) {
                setResult(res.data)
            }
        })
    };


    /**
     * 表单成功提交
     * @param values 
     */
    const onFinish = (values: any) => {
        // 1. 提取图片上传路径
        values.imgPath = values.imgPath[0].response.data.path
        // 2. 获取能够押的韵
        getPoemCanRhyme({rhyType:values.rhymeType, rhyName:values.rhymeName, bookName:values.bookName}).then((res:any) => {
            if(res.code === 200){
                setRhymes(res.data)
            }
        })
        // 3.打开对话框，选择韵脚
        setIsModalOpen(true)
        // 4. 将当前收集到的表单值赋值给最终要提交的数据
        setFormData({...values})
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
        <div className="imgtext">
            {/* 选择韵脚(由于条件复杂，故将其调整为第二步) */}
            <Modal title="选择韵脚" 
                    open={isModalOpen}
                    cancelText="取消"
                    okText="开始生成"
                    onOk={handleOk} onCancel={() => setIsModalOpen(false)}>
                <Select 
                    style={{width:220}}
                    options={mapListWithLabel(rhymes)}
                    onChange={(v:string) => setCurRhyme(v)}
                    >

                </Select>
            </Modal>

             {/* 普通导航栏 */}
             <NavNormal/>
            <div className="imgtext-main">
                {/* 标题 */}
                {/* <div className="title">画意轩</div> */}
                {/* 表单 */}
                <div className="form">
                    <Form
                        name="img-text-form"
                        className="img-text-form"
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
                        {/* 图片上传 */}
                        <Form.Item<ImgTextForm> label="图片上传" valuePropName="fileList" name="imgPath" 
                                    getValueFromEvent={normFile} 
                                    rules={[{ required: true, message: '请上传图片' }]}>
                            <Upload.Dragger name="file" 
                                action="http://localhost:5000/file/uploadImg" // TODO 后期更改为动态
                                maxCount={1}
                                accept="image/*">
                                <p className="ant-upload-drag-icon">
                                    <InboxOutlined />
                                </p>
                                <p className="ant-upload-text">点击或者拖拽图片到此处进行文件上传</p>
                                <p className="ant-upload-hint">使用风景图，效果更佳</p>
                            </Upload.Dragger>
                        </Form.Item>

                        {/* 提示词 */}
                        <Form.Item<ImgTextForm>
                            label="提示词"
                            name="addWords"
                        >
                            <Input placeholder="请输入提示词，使用逗号隔开"/>
                        </Form.Item>

                        {/* 韵律类型 */}
                        <Form.Item<ImgTextForm>
                            label="韵律类型"
                            name="rhymeType"
                            rules={[{ required: true, message: '请选择韵律类型' }]}
                            initialValue="0"
                        >
                            <Radio.Group onChange={(e) => handleRuleTypeChange(e)}>
                                <Radio value="0">律诗</Radio>
                                <Radio value="1">词牌</Radio>
                            </Radio.Group>
                        </Form.Item>

                        {/* 规则列表 */}
                        <Form.Item<ImgTextForm>
                            label="韵律规则"
                            name="rhymeName"
                            rules={[{required:true, message:"请选择韵律规则"}]}
                        >
                            <Select
                                style={{ width: 220 }}
                                placeholder="请选择韵律规则"
                                options={mapListWithLabel(ruleList)}
                            />
                        </Form.Item>

                        {/* 韵书 */}
                        <Form.Item<ImgTextForm>
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
                            <Button className="btn" type="primary" htmlType="submit" size="large" style={{width:"600px", height:"45px", marginTop:"15px"}}>
                                提交信息
                            </Button>
                        </Form.Item>
                    </Form>
                </div>
            </div>

            {/* 结果展示栏 */}
            <Card loading={loading} result={result}/>
        </div>
    )
}
