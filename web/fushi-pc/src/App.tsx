import './App.css'
import Home from './views/Home/Home'
import {ConfigProvider} from 'antd'
function App() {

	return (
		<ConfigProvider
			theme={{
				token: {
				// Seed Token，影响范围大，配置主题色
				colorPrimary: '#158bb8'
				},
			}}>
			<div className='app'>
				{/* 临时展示Home组件 */}
				<Home/> 
			</div>
		</ConfigProvider>

	)
}

export default App
