import './App.css'
import {ConfigProvider} from 'antd'
import {useRoutes} from "react-router-dom"
import routes from "./router/routes"
import Footer from './components/Footer/Footer'


function App() {
	// 引入路由
	const outlet = useRoutes(routes);
	return (
		<ConfigProvider
			theme={{
				token: {
				// Seed Token，影响范围大，配置主题色
				colorPrimary: '#158bb8'
				},
			}}>
			<div className='app'>
				{outlet}
				{/* 底部 */}
				<Footer/>
			</div>
		</ConfigProvider>

	)
}

export default App
