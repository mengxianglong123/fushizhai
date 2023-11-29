import './App.css'
import Home from './views/Home/Home'
import {ConfigProvider} from 'antd'
import {useRoutes} from "react-router-dom"
import routes from "./router/routes"


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
			</div>
		</ConfigProvider>

	)
}

export default App
