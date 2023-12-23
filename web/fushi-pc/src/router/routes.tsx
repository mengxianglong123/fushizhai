import {Suspense, FC} from "react"
import {lazy} from "react"
import {Spin} from "antd"

// 引入首页
const Home = lazy(() => import("@/views/Home/Home"))
// 引入画意轩
const ImgText = lazy(() => import("@/views/ImgText/ImgText"))
// 引入修诗阁
const FixPoem = lazy(() => import("@/views/FixPoem/FixPoem"))
// 引入思墨堂
const SiMo = lazy(() => import("@/views/SiMo/SiMo"))
// 引入思墨堂结果页
const SiMoResult  = lazy(() => import("@/views/SiMo/SiMoResult/SiMoResult"))
// 引入译书园
const Translation = lazy(() => import("@/views/Translation/Translation"))


/**
 * 将组件使用<Suspense>包起来
 * @param comp 
 * @returns 
 */
const withLoadingComponent = (comp:JSX.Element) => {
    
    // 添加懒加载缓冲
    return  <Suspense fallback={<Spin/>}>
                {comp}
            </Suspense>
}

// 声明前置钩子组件props类型
interface BeforeRouteProps{
    data:{
        children:JSX.Element,
        path:string
    }
}

/**
 * 路由前置钩子
 * @param param0 
 * @returns 
 */
const BeforeRoute:FC<BeforeRouteProps> = ({data}) => {
    // 存储当前路径
    sessionStorage.setItem("current_path", data.path)
    return <>{data.children}</>
}

export default [
    {
        // 首页
        path:"/home",
        element:<BeforeRoute data={{children:withLoadingComponent(<Home/>), path:"home"}}/>
    },
    {
        // 画意轩
        path:"/imgtext",
        element:<BeforeRoute data={{children:withLoadingComponent(<ImgText/>), path:"imgtext"}}/>
    },
    {
        // 修诗阁
        path:"/fixpoem",
        element:<BeforeRoute data={{children:withLoadingComponent(<FixPoem/>), path:"fixpoem"}}/>
    },
    {
        // 思墨堂
        path:"/simo",
        element:<BeforeRoute data={{children:withLoadingComponent(<SiMo/>), path:"simo"}}/>
    },
    {
        // 思墨堂结果页
        path:"/simoResult/:content",
        element:<BeforeRoute data={{children:withLoadingComponent(<SiMoResult/>), path:"simoResult"}}/>
    },
    {
        // 译书园
        path:"/translation",
        element:<BeforeRoute data={{children:withLoadingComponent(<Translation/>), path:"translation"}}/>
    },
    {
        // 无特定则到home页面
        path:"/",
        element:<BeforeRoute data={{children:withLoadingComponent(<Home/>), path:"home"}}/>
    }
]