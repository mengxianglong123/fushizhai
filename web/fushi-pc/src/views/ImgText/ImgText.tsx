import NavNormal from "@/components/NavNormal/NavNormal";
import { ImgTextForm } from "@/types/imgtext";
import { Button, Form, Radio, Input, Upload, Select } from 'antd';
import {InboxOutlined} from "@ant-design/icons"
import "./imgtext.scss"
import {useEffect, useState}  from "react"
import {getRhymeRulesByType, getRhymeBookNames} from "@/api/imgtext"

const onFinish = (values: any) => {
    console.log('Success:', values);
}

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
    // 表单数据
    const [form] = Form.useForm();
    const [formData, setFormData] = useState<ImgTextForm>();
    // 规则列表
    const [ruleList, setRuleList] = useState([])
    // 韵书列表
    const [rhymeBooks, setRhymeBooks] = useState([])


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
             {/* 暂时展示导航栏 */}
             <NavNormal/>
            <div className="imgtext-main">
                {/* 标题 */}
                <div className="title">画意轩</div>
                {/* 表单 */}
                <div className="form">
                <Form
                    name="basic"
                    labelCol={{ span: 8 }}
                    wrapperCol={{ span: 16 }}
                    style={{ maxWidth: 600 }}
                    initialValues={{ remember: true }}
                    onFinish={onFinish}
                    onFinishFailed={onFinishFailed}
                    autoComplete="off"
                    onValuesChange={(changedValues, allValues) => { setFormData(allValues) }}
                    form={form}
                       
                >
                    {/* 图片上传 */}
                    <Form.Item<ImgTextForm> label="Upload" valuePropName="fileList" name="imgPath" 
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


                    <Form.Item wrapperCol={{ offset: 8, span: 16 }}>
                        <Button type="primary" htmlType="submit">
                            Submit
                        </Button>
                    </Form.Item>
                </Form>
                </div>
            </div>
        </div>
    )
}
