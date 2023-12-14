# 赋诗斋-PC页面



## 问题记录

### 1. 关于wow.js在React中不生效的解决方案

- 方案一：直接在项目地index.html中因为并初始化wow(可以把依赖放到public目录下)
- 方案二：使用`react-wow` ：https://github.com/skyvow/react-wow/

### 2. ts项目中，路由配置文件的后缀必须是`.tsx`不能是ts，否则无法正常声明



### 3. React在ts环境下实现函数组件父传子

https://blog.csdn.net/m0_46234046/article/details/134104681



普通父传子：

父组件

```react
    // 当前生成状态
    const [loading, setLoading] = useState(false)
    // 当前生成结果
    const [result, setResult] = useState("红笺小字，为你写诗")
    {/* 结果展示栏,每个变量需要单独传递 */}
    <Card loading={loading} result={result}/>
```

子组件

```react
interface CardProps {
    loading:boolean,
    result:string
}
export default function Card(props:CardProps) {
    
    return (
        <div>{props.result}</div>
    )
}
```

